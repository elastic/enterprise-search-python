#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from .connection import Urllib3HttpConnection
from .connection_pool import ConnectionPool, DummyConnectionPool, EmptyConnectionPool
from .serializer import JSONSerializer, Deserializer, DEFAULT_SERIALIZERS
from .response import Response, Request
from ..exceptions import (
    ConnectionError,
    ConnectionTimeout,
    TransportError,
)
from ..utils import urlparse, unquote, string_types


class Transport(object):
    """
    Encapsulation of transport-related to logic. Handles instantiation of the
    individual connections as well as creating a connection pool to hold them.

    Main interface is the `perform_request` method.
    """

    DEFAULT_CONNECTION_CLASS = Urllib3HttpConnection

    def __init__(
        self,
        hosts,
        connection_class=None,
        connection_pool_class=ConnectionPool,
        serializer=JSONSerializer(),
        serializers=None,
        default_mimetype="application/json",
        max_retries=3,
        retry_on_status=(502, 503, 504),
        retry_on_timeout=False,
        **kwargs
    ):
        """
        :arg hosts: list of dictionaries, each containing keyword arguments to
            create a `connection_class` instance
        :arg connection_class: subclass of :class:`~elastic_enterprise_search.Connection` to use
        :arg connection_pool_class: subclass of :class:`~elastic_enterprise_search.ConnectionPool` to use
        :arg serializer: serializer instance
        :arg serializers: optional dict of serializer instances that will be
            used for deserializing data coming from the server. (key is the mimetype)
        :arg default_mimetype: when no mimetype is specified by the server
            response assume this mimetype, defaults to `'application/json'`
        :arg max_retries: maximum number of retries before an exception is propagated
        :arg retry_on_status: set of HTTP status codes on which we should retry
            on a different node. defaults to ``(502, 503, 504)``
        :arg retry_on_timeout: should timeout trigger a retry on different
            node? (default `False`)

        Any extra keyword arguments will be passed to the `connection_class`
        when creating and instance unless overridden by that connection's
        options provided as part of the hosts parameter.
        """
        hosts = _normalize_hosts(hosts)
        if connection_class is None:
            connection_class = self.DEFAULT_CONNECTION_CLASS

        # serialization config
        _serializers = DEFAULT_SERIALIZERS.copy()
        # if a serializer has been specified, use it for deserialization as well
        _serializers[serializer.mimetype] = serializer
        # if custom serializers map has been supplied, override the defaults with it
        if serializers:
            _serializers.update(serializers)
        # create a deserializer with our config
        self.deserializer = Deserializer(_serializers, default_mimetype)

        self.max_retries = max_retries
        self.retry_on_timeout = retry_on_timeout
        self.retry_on_status = retry_on_status

        # data serializer
        self.serializer = serializer

        # store all strategies...
        self.connection_pool_class = connection_pool_class
        self.connection_class = connection_class

        # ...save kwargs to be passed to the connections
        self.kwargs = kwargs
        self.hosts = hosts

        # Start with an empty pool specifically for `AsyncTransport`.
        # It should never be used, will be replaced on first call to
        # .set_connections()
        self.connection_pool = EmptyConnectionPool()

        if hosts:
            # ...and instantiate them
            self.set_connections(hosts)
            # retain the original connection instances for sniffing
            self.seed_connections = list(self.connection_pool.connections[:])
        else:
            self.seed_connections = []

    def add_connection(self, host):
        """
        Create a new :class:`~elastic_enterprise_search.Connection` instance and add it to the pool.

        :arg host: kwargs that will be used to create the instance
        """
        self.hosts.append(host)
        self.set_connections(self.hosts)

    def set_connections(self, hosts):
        """
        Instantiate all the connections and create new connection pool to hold them.
        Tries to identify unchanged hosts and re-use existing
        :class:`~elastic_enterprise_search.Connection` instances.

        :arg hosts: same as `__init__`
        """
        # construct the connections
        def _create_connection(host):
            # if this is not the initial setup look at the existing connection
            # options and identify connections that haven't changed and can be
            # kept around.
            if hasattr(self, "connection_pool"):
                for (connection, old_host) in self.connection_pool.connection_opts:
                    if old_host == host:
                        return connection

            # previously unseen params, create new connection
            kwargs = self.kwargs.copy()
            kwargs.update(host)
            return self.connection_class(**kwargs)

        connections = map(_create_connection, hosts)

        connections = list(zip(connections, hosts))
        if len(connections) == 1:
            self.connection_pool = DummyConnectionPool(connections)
        else:
            # pass the hosts dicts to the connection pool to optionally extract parameters from
            self.connection_pool = self.connection_pool_class(
                connections, **self.kwargs
            )

    def get_connection(self):
        """
        Retrieve a :class:`~elastic_enterprise_search.Connection` instance from the
        :class:`~elastic_enterprise_search.ConnectionPool` instance.
        """
        return self.connection_pool.get_connection()

    def mark_dead(self, connection):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process.

        :arg connection: instance of :class:`~elastic_enterprise_search.Connection` that failed
        """
        # mark as dead even when sniffing to avoid hitting this host during the sniff process
        self.connection_pool.mark_dead(connection)

    def perform_request(self, method, url, headers=None, params=None, body=None):
        """
        Perform the actual request. Retrieve a connection from the connection
        pool, pass all the information to it's perform_request method and
        return the data.

        If an exception was raised, mark the connection as failed and retry (up
        to `max_retries` times).

        If the operation was successful and the connection used was previously
        marked as dead, mark it as live, resetting it's failure count.

        :arg method: HTTP method to use
        :arg url: absolute url (without host) to target
        :arg headers: dictionary of headers, will be handed over to the
            underlying :class:`~elastic_enterprise_search.Connection` class
        :arg params: dictionary of query parameters, will be handed over to the
            underlying :class:`~elastic_enterprise_search.Connection` class for serialization
        :arg body: body of the request, will be serialized using serializer and
            passed to the connection
        :returns: Deserialized response body
        """
        method, params, body, ignore, timeout = self._resolve_request_args(
            method, params, body
        )
        request = Request(method=method, path=url, headers=headers, params=params)

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                status_code, headers_response, data = connection.perform_request(
                    method,
                    url,
                    params,
                    body,
                    headers=headers,
                    ignore=ignore,
                    timeout=timeout,
                )

            except TransportError as e:
                if method == "HEAD" and e.status_code == 404:
                    return Response(request=request, status_code=404, content=False)

                retry = False
                if isinstance(e, ConnectionTimeout):
                    retry = self.retry_on_timeout
                elif isinstance(e, ConnectionError):
                    retry = True
                elif e.status_code in self.retry_on_status:
                    retry = True

                if retry:
                    try:
                        # only mark as dead if we are retrying
                        self.mark_dead(connection)
                    except TransportError:
                        # If sniffing on failure, it could fail too. Catch the
                        # exception not to interrupt the retries.
                        pass
                    # raise exception on last retry
                    if attempt == self.max_retries:
                        raise
                else:
                    raise

            else:
                # connection didn't fail, confirm it's live status
                self.connection_pool.mark_live(connection)

                if method == "HEAD":
                    return Response(
                        request=request,
                        status_code=status_code,
                        content=200 <= status_code < 300,
                    )

                if data:
                    data = self.deserializer.loads(
                        data, headers_response.get("content-type")
                    )

                # After the body is deserialized put the data
                # into one of the typed responses
                return Response(request=request, status_code=status_code, content=data)

    def close(self):
        """
        Explicitly closes connections
        """
        self.connection_pool.close()

    def _resolve_request_args(self, method, params, body):
        """Resolves parameters for .perform_request()"""
        if body is not None:
            body = self.serializer.dumps(body)

        if body is not None:
            try:
                body = body.encode("utf-8", "surrogatepass")
            except (UnicodeDecodeError, AttributeError):
                # bytes/str - no need to re-encode
                pass

        ignore = ()
        timeout = None
        if params:
            timeout = params.pop("request_timeout", None)
            ignore = params.pop("ignore", ())
            if isinstance(ignore, int):
                ignore = (ignore,)

        return method, params, body, ignore, timeout


def _normalize_hosts(hosts):
    """
    Helper function to transform hosts argument to
    :class:`~elasticsearch.Elasticsearch` to a list of dicts.
    """
    # if hosts are empty, just defer to defaults down the line
    if hosts is None:
        return [{}]

    # passed in just one string
    if isinstance(hosts, string_types):
        hosts = [hosts]

    out = []
    # normalize hosts to dicts
    for host in hosts:
        if isinstance(host, string_types):
            if "://" not in host:
                host = "//%s" % host

            parsed_url = urlparse(host)
            h = {"host": parsed_url.hostname}

            if parsed_url.port:
                h["port"] = parsed_url.port

            if parsed_url.scheme == "https":
                h["port"] = parsed_url.port or 443
                h["use_ssl"] = True

            if parsed_url.username or parsed_url.password:
                h["http_auth"] = "%s:%s" % (
                    unquote(parsed_url.username),
                    unquote(parsed_url.password),
                )

            if parsed_url.path and parsed_url.path != "/":
                h["url_prefix"] = parsed_url.path

            out.append(h)
        else:
            out.append(host)
    return out
