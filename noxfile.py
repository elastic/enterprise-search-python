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

from os.path import abspath, dirname, join

import nox

SOURCE_FILES = (
    "noxfile.py",
    "setup.py",
    "elastic_enterprise_search/",
    "utils/",
    "tests/",
)


@nox.session()
def format(session):
    session.run("python", "-m", "pip", "install", "--pre", "black<22", "isort")
    session.run(
        "black", "--target-version=py27", "--target-version=py37", *SOURCE_FILES
    )
    session.run("isort", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session
def lint(session):
    session.run(
        "python", "-m", "pip", "install", "--pre", "black<22", "isort", "flake8"
    )
    session.run(
        "black",
        "--check",
        "--target-version=py27",
        "--target-version=py37",
        *SOURCE_FILES
    )
    session.run("isort", "--check", *SOURCE_FILES)
    session.run("flake8", "--ignore=E501,W503,E203", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)


def tests_impl(session):
    junit_xml = join(
        abspath(dirname(__file__)),
        "junit/enterprise-search-python-junit.xml",
    )
    session.install("git+https://github.com/elastic/elastic-transport-python@7.x")
    session.install(".[develop]")
    session.run(
        "pytest",
        "--junitxml=%s" % junit_xml,
        "--cov=elastic_enterprise_search",
        *(session.posargs or ("tests/",)),
        env={"PYTHONWARNINGS": "always::DeprecationWarning"}
    )
    session.run("coverage", "report", "-m")


@nox.session(python=["2.7", "3.6", "3.7", "3.8", "3.9"])
def test(session):
    tests_impl(session)
