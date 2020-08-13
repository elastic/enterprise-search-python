# -*- coding: utf-8 -*-
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

import re
import ssl
import gzip
import io
from mock import Mock, patch
import urllib3
from urllib3._collections import HTTPHeaderDict
import warnings
from platform import python_version

from elastic_enterprise_search import (
    TransportError,
    Conflict,
    BadRequest,
    NotFound,
)
from elastic_enterprise_search import (
    __version__,
    RequestsHttpConnection,
    Urllib3HttpConnection,
)
import pytest


def gzip_decompress(data):
    buf = gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb")
    return buf.read()


class TestUrllib3Connection(object):
    def _get_mock_connection(self, connection_params={}, response_body=b"{}"):
        con = Urllib3HttpConnection(**connection_params)

        def _dummy_urlopen(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = HTTPHeaderDict({})
            dummy_response.status = 200
            dummy_response.data = response_body
            _dummy_urlopen.call_args = (args, kwargs)
            return dummy_response

        con.pool.urlopen = _dummy_urlopen
        return con

    def test_ssl_context(self):
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError Exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            pytest.skip(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of ptyhon"
            )

        con = Urllib3HttpConnection(use_ssl=True, ssl_context=context)
        assert len(con.pool.conn_kw.keys()) == 1
        assert isinstance(con.pool.conn_kw["ssl_context"], ssl.SSLContext)
        assert con.use_ssl

    def test_opaque_id(self):
        con = Urllib3HttpConnection(opaque_id="app-1")
        assert con.headers["x-opaque-id"] == "app-1"

    def test_no_http_compression(self):
        con = self._get_mock_connection()
        assert not con.http_compress
        assert "accept-encoding" not in con.headers

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        assert not req_body
        assert "accept-encoding" not in kwargs["headers"]
        assert "content-encoding" not in kwargs["headers"]

    def test_http_compression(self):
        con = self._get_mock_connection({"http_compress": True})
        assert con.http_compress
        assert con.headers["accept-encoding"] == "gzip"

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        assert "content-encoding" not in con.headers

        con.perform_request("GET", "/", body=b"{}")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        assert gzip_decompress(req_body) == b"{}"
        assert kwargs["headers"]["accept-encoding"] == "gzip"
        assert kwargs["headers"]["content-encoding"] == "gzip"

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        assert not req_body
        assert kwargs["headers"]["accept-encoding"] == "gzip"
        assert "content-encoding" not in kwargs["headers"]

    def test_default_user_agent(self):
        con = Urllib3HttpConnection()
        assert con._get_default_user_agent() == "enterprise-search-python/%s (Python %s)" % (
            __version__,
            python_version(),
        )

    def test_timeout_set(self):
        con = Urllib3HttpConnection(timeout=42)
        assert 42 == con.timeout

    def test_keep_alive_is_on_by_default(self):
        con = Urllib3HttpConnection()
        assert {
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
            assert 1 == len(w)
            assert (
                "Connecting to https://localhost:3002 using SSL with verify_certs=False is insecure"
                == str(w[0].message)
            )

        assert isinstance(con.pool, urllib3.HTTPSConnectionPool)

    def nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            assert 0 == len(w)

        assert isinstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_doesnt_use_https_if_not_specified(self):
        con = Urllib3HttpConnection()
        assert isinstance(con.pool, urllib3.HTTPConnectionPool)

    def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            Urllib3HttpConnection(ssl_context=ctx)
            assert 0 == len(w)

    def test_warns_if_using_non_default_ssl_kwargs_with_ssl_context(self):
        for kwargs in (
            {"ssl_show_warn": False},
            {"ssl_show_warn": True},
            {"verify_certs": True},
            {"verify_certs": False},
            {"ca_certs": "/path/to/certs"},
            {"ssl_show_warn": True, "ca_certs": "/path/to/certs"},
        ):
            kwargs["ssl_context"] = ssl.create_default_context()

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                Urllib3HttpConnection(**kwargs)

                assert 1 == len(w)
                assert (
                    "When using `ssl_context`, all other SSL related kwargs are ignored"
                    == str(w[0].message)
                )

    @patch("elastic_enterprise_search.transport.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b'{"example": "body"}')

        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list

        assert '> {"example": "body"}' == req[0][0] % req[0][1:]
        assert "< {}" == resp[0][0] % resp[0][1:]

    def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = self._get_mock_connection(response_body=buf)
        status, headers, data = con.perform_request("GET", "/")
        assert u"你好\uda6a" == data


class TestRequestsConnection(object):
    def _get_mock_connection(
        self, connection_params={}, status_code=200, response_body=b"{}"
    ):
        con = RequestsHttpConnection(**connection_params)

        def _dummy_send(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = {}
            dummy_response.status_code = status_code
            dummy_response.content = response_body
            dummy_response.request = args[0]
            dummy_response.cookies = {}
            _dummy_send.call_args = (args, kwargs)
            return dummy_response

        con.session.send = _dummy_send
        return con

    def _get_request(self, connection, *args, **kwargs):
        if "body" in kwargs:
            kwargs["body"] = kwargs["body"].encode("utf-8")

        status, headers, data = connection.perform_request(*args, **kwargs)
        assert 200 == status
        assert "{}" == data

        timeout = kwargs.pop("timeout", connection.timeout)
        args, kwargs = connection.session.send.call_args
        assert timeout == kwargs["timeout"]
        assert 1 == len(args)
        return args[0]

    def test_timeout_set(self):
        con = RequestsHttpConnection(timeout=42)
        assert 42 == con.timeout

    def test_opaque_id(self):
        con = RequestsHttpConnection(opaque_id="app-1")
        assert con.headers["x-opaque-id"] == "app-1"

    def test_no_http_compression(self):
        con = self._get_mock_connection()

        assert not con.http_compress
        assert "content-encoding" not in con.session.headers

        con.perform_request("GET", "/")

        req = con.session.send.call_args[0][0]
        assert "content-encoding" not in req.headers
        assert "accept-encoding" not in req.headers

    def test_http_compression(self):
        con = self._get_mock_connection({"http_compress": True},)

        assert con.http_compress

        # 'content-encoding' shouldn't be set at a session level.
        # Should be applied only if the request is sent with a body.
        assert "content-encoding" not in con.session.headers

        con.perform_request("GET", "/", body=b"{}")

        req = con.session.send.call_args[0][0]
        assert req.headers["content-encoding"] == "gzip"
        assert req.headers["accept-encoding"] == "gzip"

        con.perform_request("GET", "/")

        req = con.session.send.call_args[0][0]
        assert "content-encoding" not in req.headers
        assert req.headers["accept-encoding"] == "gzip"

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = self._get_mock_connection(
                {"use_ssl": True, "url_prefix": "url", "verify_certs": False}
            )
            assert 1 == len(w)
            assert (
                "Connecting to https://localhost:3002 using SSL with verify_certs=False is insecure"
                == str(w[0].message)
            )

        request = self._get_request(con, "GET", "/")

        assert "https://localhost:3002/url/" == request.url
        assert "GET" == request.method
        assert None is request.body

    def nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = self._get_mock_connection(
                {
                    "use_ssl": True,
                    "url_prefix": "url",
                    "verify_certs": False,
                    "ssl_show_warn": False,
                }
            )
            assert 0 == len(w)

        request = self._get_request(con, "GET", "/")

        assert "https://localhost:3002/url/" == request.url
        assert "GET" == request.method
        assert None is request.body

    def test_merge_headers(self):
        con = self._get_mock_connection(
            connection_params={"headers": {"h1": "v1", "h2": "v2"}}
        )
        req = self._get_request(con, "GET", "/", headers={"h2": "v2p", "h3": "v3"})
        assert req.headers["h1"] == "v1"
        assert req.headers["h2"] == "v2p"
        assert req.headers["h3"] == "v3"

    def test_default_headers(self):
        con = self._get_mock_connection()
        req = self._get_request(con, "GET", "/")
        assert req.headers["content-type"] == "application/json"
        assert req.headers["user-agent"] == con._get_default_user_agent()

    def test_custom_headers(self):
        con = self._get_mock_connection()
        req = self._get_request(
            con,
            "GET",
            "/",
            headers={
                "content-type": "application/x-ndjson",
                "user-agent": "custom-agent/1.2.3",
            },
        )
        assert req.headers["content-type"] == "application/x-ndjson"
        assert req.headers["user-agent"] == "custom-agent/1.2.3"

    def test_repr(self):
        con = self._get_mock_connection({"host": "elasticsearch.com", "port": 443})
        assert "<RequestsHttpConnection: http://elasticsearch.com:443>" == repr(con)

    def test_conflict_error_is_returned_on_409(self):
        con = self._get_mock_connection(status_code=409)
        with pytest.raises(Conflict):
            con.perform_request("GET", "/", {}, "")

    def test_not_found_error_is_returned_on_404(self):
        con = self._get_mock_connection(status_code=404)
        with pytest.raises(NotFound):
            con.perform_request("GET", "/", {}, "")

    def test_request_error_is_returned_on_400(self):
        con = self._get_mock_connection(status_code=400)
        with pytest.raises(BadRequest):
            con.perform_request("GET", "/", {}, "")

    @patch("elastic_enterprise_search.transport.connection.base.logger")
    def test_head_with_404_doesnt_get_logged(self, logger):
        con = self._get_mock_connection(status_code=404)
        with pytest.raises(NotFound):
            con.perform_request("HEAD", "/", {}, "")
        assert 0 == logger.warning.call_count

    @patch("elastic_enterprise_search.transport.connection.base.tracer")
    @patch("elastic_enterprise_search.transport.connection.base.logger")
    def test_failed_request_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(
            response_body=b'{"answer": 42}', status_code=500
        )
        with pytest.raises(TransportError):
            con.perform_request(
                "GET", "/", {"param": 42}, "{}".encode("utf-8"),
            )

        # trace request
        assert 1 == tracer.info.call_count
        # trace response
        assert 1 == tracer.debug.call_count
        # log url and duration
        assert 1 == logger.warning.call_count
        assert re.match(
            r"^GET http://localhost:3002/\?param=42 \[status:500 request:0.[0-9]{3}s\]",
            logger.warning.call_args[0][0] % logger.warning.call_args[0][1:],
        )

    @patch("elastic_enterprise_search.transport.connection.base.tracer")
    @patch("elastic_enterprise_search.transport.connection.base.logger")
    def test_success_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body=b"""{"answer": "that's it!"}""")
        con.perform_request(
            "GET",
            "/",
            {"param": 42},
            """{"question": "what's that?"}""".encode("utf-8"),
        )

        # trace request
        assert 1 == tracer.info.call_count
        assert (
            """curl -H 'Content-Type: application/json' -XGET 'http://localhost:3002/?pretty&param=42' -d '{\n  "question": "what\\u0027s that?"\n}'"""
            == tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )
        # trace response
        assert 1 == tracer.debug.call_count
        assert re.match(
            r'#\[200\] \(0.[0-9]{3}s\)\n#{\n#  "answer": "that\\u0027s it!"\n#}',
            tracer.debug.call_args[0][0] % tracer.debug.call_args[0][1:],
        )

        # log url and duration
        assert 1 == logger.info.call_count
        assert re.match(
            r"GET http://localhost:3002/\?param=42 \[status:200 request:0.[0-9]{3}s\]",
            logger.info.call_args[0][0] % logger.info.call_args[0][1:],
        )
        # log request body and response
        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list
        assert '> {"question": "what\'s that?"}' == req[0][0] % req[0][1:]
        assert '< {"answer": "that\'s it!"}' == resp[0][0] % resp[0][1:]

    @patch("elastic_enterprise_search.transport.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b'{"example": "body"}')

        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list
        assert '> {"example": "body"}' == req[0][0] % req[0][1:]
        assert "< {}" == resp[0][0] % resp[0][1:]

    def test_defaults(self):
        con = self._get_mock_connection()
        request = self._get_request(con, "GET", "/")

        assert "http://localhost:3002/" == request.url
        assert "GET" == request.method
        assert None is request.body

    def test_params_properly_encoded(self):
        con = self._get_mock_connection()
        request = self._get_request(
            con, "GET", "/", params={"param": "value with spaces"}
        )

        assert "http://localhost:3002/?param=value+with+spaces" == request.url
        assert "GET" == request.method
        assert None is request.body

    def test_body_attached(self):
        con = self._get_mock_connection()
        request = self._get_request(con, "GET", "/", body='{"answer": 42}')

        assert "http://localhost:3002/" == request.url
        assert "GET" == request.method
        assert '{"answer": 42}'.encode("utf-8") == request.body

    @patch("elastic_enterprise_search.transport.connection.base.tracer")
    def test_url_prefix(self, tracer):
        con = self._get_mock_connection({"url_prefix": "/some-prefix/"})
        request = self._get_request(
            con, "GET", "/_search", body='{"answer": 42}', timeout=0.1
        )

        assert "http://localhost:3002/some-prefix/_search" == request.url
        assert "GET" == request.method
        assert '{"answer": 42}'.encode("utf-8") == request.body

        # trace request
        assert 1 == tracer.info.call_count
        assert (
            "curl -H 'Content-Type: application/json' -XGET 'http://localhost:3002/_search?pretty' -d '{\n  \"answer\": 42\n}'"
            == tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )

    def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = self._get_mock_connection(response_body=buf)
        status, headers, data = con.perform_request("GET", "/")
        assert u"你好\uda6a" == data
