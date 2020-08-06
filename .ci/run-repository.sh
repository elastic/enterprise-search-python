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

set -e

echo -e "\033[34;1mINFO:\033[0m STACK_VERSION ${STACK_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_VERSION ${PYTHON_VERSION}\033[0m"

echo -e "\033[1m>>>>> Build [elastic/enterprise-search-python container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

docker build \
       --file .ci/Dockerfile \
       --tag elastic/enterprise-search-python \
       --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
       .

echo -e "\033[1m>>>>> Run [elastic/enterprise-search-python container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

mkdir -p junit
docker run \
  --network ${network_name} \
  --name enterprise-search-python \
  --rm \
  --volume `pwd`:/code/enterprise-search-python \
  elastic/enterprise-search-python \
  nox -s test-${PYTHON_VERSION}
