#!/usr/bin/env bash
#
# Launch one App Search node via the Docker image,
# to form a cluster suitable for running the REST API tests.
#
# Export the STACK_VERSION variable, eg. '8.0.0-SNAPSHOT'.

# Version 1.1.0
# - Initial version of the run-app-search.sh script
# - Refactored .buildkite version

script_path=$(dirname $(realpath -s $0))
source $script_path/functions/imports.sh
set -euo pipefail

CONTAINER_NAME=${CONTAINER_NAME-app-search}
APP_SEARCH_SECRET_SESSION_KEY=${APP_SEARCH_SECRET_SESSION_KEY-int_test_secret}

echo -e "\033[34;1mINFO:\033[0m Take down node if called twice with the same arguments (DETACH=true) or on seperate terminals \033[0m"
cleanup_node $CONTAINER_NAME

http_port=3002
url=http://127.0.0.1:${http_port}

# Pull the container, retry on failures up to 5 times with
# short delays between each attempt. Fixes most transient network errors.
docker_pull_attempts=0
until [ "$docker_pull_attempts" -ge 5 ]
do
   docker pull docker.elastic.co/enterprise-search/enterprise-search:"$STACK_VERSION" && break
   docker_pull_attempts=$((docker_pull_attempts+1))
   echo "Failed to pull image, retrying in 10 seconds (retry $docker_pull_attempts/5)..."
   sleep 10
done

echo -e "\033[34;1mINFO:\033[0m Starting container $CONTAINER_NAME \033[0m"
set -x
docker run \
  --name "$CONTAINER_NAME" \
  --network "$network_name" \
  --env "elasticsearch.host=$elasticsearch_url" \
  --env "elasticsearch.username=elastic" \
  --env "elasticsearch.password=$elastic_password" \
  --env "ENT_SEARCH_DEFAULT_PASSWORD=$elastic_password" \
  --env "secret_management.encryption_keys=[$APP_SEARCH_SECRET_SESSION_KEY]" \
  --env "enterprise_search.listen_port=$http_port" \
  --env "log_level=info" \
  --env "hide_version_info=false" \
  --env "worker.threads=2" \
  --env "allow_es_settings_modification=true" \
  --env "JAVA_OPTS=-Xms1g -Xmx2g" \
  --env "elasticsearch.ssl.enabled=true" \
  --env "elasticsearch.ssl.verify=true" \
  --env "elasticsearch.ssl.certificate=/usr/share/app-search/config/certs/testnode.crt" \
  --env "elasticsearch.ssl.certificate_authority=/usr/share/app-search/config/certs/ca.crt" \
  --env "elasticsearch.ssl.key=/usr/share/app-search/config/certs/testnode.key" \
  --volume $ssl_cert:/usr/share/app-search/config/certs/testnode.crt \
  --volume $ssl_key:/usr/share/app-search/config/certs/testnode.key \
  --volume $ssl_ca:/usr/share/app-search/config/certs/ca.crt \
  --publish "$http_port":3002 \
  --detach="$DETACH" \
  --health-cmd="curl --insecure --fail ${url} || exit 1" \
  --health-interval=30s \
  --health-retries=50 \
  --health-timeout=10s \
  --rm \
  docker.elastic.co/enterprise-search/enterprise-search:"$STACK_VERSION";

if wait_for_container "$CONTAINER_NAME" "$network_name"; then
  echo -e "\033[32;1mSUCCESS:\033[0m Running on: ${url}\033[0m"
fi
