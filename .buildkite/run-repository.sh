#!/usr/bin/env bash
#
# Called by entry point `run-test` use this script to add your repository specific test commands
#
# Once called Elasticsearch is up and running
#
# Its recommended to call `imports.sh` as defined here so that you get access to all variables defined there
#
# Any parameters that test-matrix.yml defines should be declared here with appropiate defaults

script_path=$(dirname $(realpath -s $0))
source $script_path/functions/imports.sh
set -euo pipefail

echo -e "\033[34;1mINFO:\033[0m VERSION: ${STACK_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m TEST_SUITE: ${TEST_SUITE}\033[0m"
echo -e "\033[34;1mINFO:\033[0m RUNSCRIPTS: ${RUNSCRIPTS}\033[0m"
echo -e "\033[34;1mINFO:\033[0m URL: ${elasticsearch_url}\033[0m"

echo -e "\033[34;1mINFO:\033[0m pinging Elasticsearch ..\033[0m"
curl --insecure --fail $external_elasticsearch_url/_cluster/health?pretty

# Unquote this block for 7.x branches to enable compatibility mode.
# See: knowledgebase/jenkins-es-compatibility-mode.md
# if [[ "$STACK_VERSION" == "8.0.0-SNAPSHOT" && -z "${ELASTIC_CLIENT_APIVERSIONING+x}" ]]; then
#   export STACK_VERSION="7.x-SNAPSHOT"
#   export ELASTIC_CLIENT_APIVERSIONING="true"
# fi

if [[ "$RUNSCRIPTS" = *"enterprise-search"* ]]; then
  enterprise_search_url="http://localhost:3002"
  echo -e "\033[34;1mINFO:\033[0m pinging Enterprise Search ..\033[0m"
  curl -I --fail $enterprise_search_url
fi

echo -e "\033[32;1mSUCCESS:\033[0m successfully started the ${STACK_VERSION} stack.\033[0m"

echo -e "\033[34;1mINFO:\033[0m STACK_VERSION ${STACK_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_VERSION ${PYTHON_VERSION}\033[0m"

echo ":docker: :python: :elastic-enterprise-search: Build elastic/enterprise-search-python image"

docker build \
  --file .buildkite/Dockerfile \
  --tag elastic/enterprise-search-python \
  --build-arg PYTHON_VERSION="$PYTHON_VERSION" \
  .

echo ":docker: :python: :elastic-enterprise-search: Run elastic/enterprise-search-python container"

mkdir -p "$(pwd)/junit"
docker run \
  --network ${network_name} \
  --name enterprise-search-python \
  --rm \
  -e ENTERPRISE_SEARCH_PASSWORD="$elastic_password" \
  -v "$(pwd)/junit:/junit" \
  elastic/enterprise-search-python \
  bash -c "nox -s test-$PYTHON_VERSION; [ -f ./junit/${BUILDKITE_JOB_ID:-}-junit.xml ] && mv ./junit/${BUILDKITE_JOB_ID:-}-junit.xml /junit || echo 'No JUnit artifact found'"
