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

import os
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
    session.install("black", "isort", "flynt", "unasync")

    session.run("python", "utils/run-unasync.py")
    session.run("isort", "--profile=black", *SOURCE_FILES)
    session.run("flynt", *SOURCE_FILES)
    session.run("black", "--target-version=py36", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session
def lint(session):
    session.install("flake8", "black", "isort")
    session.run("black", "--check", "--target-version=py36", *SOURCE_FILES)
    session.run("isort", "--check", *SOURCE_FILES)
    session.run("flake8", "--ignore=E501,W503,E203", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)


def tests_impl(session):
    job_id = os.environ.get("BUILDKITE_JOB_ID", None)
    if job_id is not None:
        junit_xml = join(
            abspath(dirname(__file__)),
            f"junit/{job_id}-junit.xml",
        )
    else:
        junit_xml = join(
            abspath(dirname(__file__)),
            "junit/enterprise-search-python-junit.xml",
        )

    session.install(
        "git+https://github.com/elastic/elastic-transport-python", silent=False
    )
    session.install(".[develop]", silent=False)
    session.run(
        "pytest",
        f"--junitxml={junit_xml}",
        "--cov=elastic_enterprise_search",
        "-ra",  # report all except passes
        *(session.posargs or ("tests/",)),
        env={"PYTHONWARNINGS": "always::DeprecationWarning"},
    )
    session.run("coverage", "report", "-m")


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"])
def test(session):
    tests_impl(session)
