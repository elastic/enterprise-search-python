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

"""A command line tool for building and verifying releases
Can be used for building both 'elasticsearch' and 'elasticsearchX' dists.
Only requires 'name' in 'setup.py' and the directory to be changed.
"""

import contextlib
import os
import re
import shlex
import shutil
import sys
import tempfile

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp_dir = None


@contextlib.contextmanager
def set_tmp_dir():
    global tmp_dir
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)
    tmp_dir = None


def run(*argv, expect_exit_code=0):
    global tmp_dir
    if tmp_dir is None:
        os.chdir(base_dir)
    else:
        os.chdir(tmp_dir)

    cmd = " ".join(shlex.quote(x) for x in argv)
    print("$ " + cmd)
    exit_code = os.system(cmd)
    if exit_code != expect_exit_code:
        print(
            "Command exited incorrectly: should have been %d was %d"
            % (expect_exit_code, exit_code)
        )
        exit(exit_code or 1)


def test_dist(dist):
    with set_tmp_dir() as tmp_dir:

        # Build the venv and install the dist
        run("python", "-m", "venv", os.path.join(tmp_dir, "venv"))
        venv_python = os.path.join(tmp_dir, "venv/bin/python")
        run(venv_python, "-m", "pip", "install", "-U", "pip", "mypy")
        run(venv_python, "-m", "pip", "install", dist)

        # Test the namespace and top-level clients
        run(venv_python, "-c", "import elastic_enterprise_search")
        for client in ("EnterpriseSearch", "AppSearch", "WorkplaceSearch"):
            run(venv_python, "-c", f"from elastic_enterprise_search import {client}")

        # Uninstall and ensure that clients aren't available
        run(venv_python, "-m", "pip", "uninstall", "--yes", "elastic-enterprise-search")

        run(venv_python, "-c", "import elastic_enterprise_search", expect_exit_code=256)
        for client in ("EnterpriseSearch", "AppSearch", "WorkplaceSearch"):
            run(
                venv_python,
                "-c",
                f"from elastic_enterprise_search import {client}",
                expect_exit_code=256,
            )


def main():
    run("rm", "-rf", "build/", "dist/*", "*.egg-info", ".eggs")

    # Grab the major version to be used as a suffix.
    version_path = os.path.join(base_dir, "elastic_enterprise_search/_version.py")
    with open(version_path) as f:
        version = re.search(
            r"^__version__\s+=\s+[\"\']([^\"\']+)[\"\']", f.read(), re.M
        ).group(1)

    # If we're handed a version from the build manager we
    # should check that the version is correct or write
    # a new one.
    if len(sys.argv) >= 2:
        # 'build_version' is what the release manager wants,
        # 'expect_version' is what we're expecting to compare
        # the package version to before building the dists.
        build_version = expect_version = sys.argv[1]

        # '-SNAPSHOT' means we're making a pre-release.
        if "-SNAPSHOT" in build_version:
            # If there's no +dev already (as is the case on dev
            # branches like 7.x, master) then we need to add one.
            if not version.endswith("+dev"):
                version = version + "+dev"
            expect_version = expect_version.replace("-SNAPSHOT", "")
            if expect_version.endswith(".x"):
                expect_version = expect_version[:-2]

            # For snapshots we ensure that the version in the package
            # at least *starts* with the version. This is to support
            # build_version='7.x-SNAPSHOT'.
            if not version.startswith(expect_version):
                print(
                    "Version of package (%s) didn't match the "
                    "expected release version (%s)" % (version, build_version)
                )
                exit(1)

        # A release that will be tagged, we want
        # there to be no '+dev', etc.
        elif expect_version != version:
            print(
                "Version of package (%s) didn't match the "
                "expected release version (%s)" % (version, build_version)
            )
            exit(1)

    # Ensure that the version within 'elasticsearch/_version.py' is correct.
    with open(version_path) as f:
        version_data = f.read()
    version_data = re.sub(
        r"__version__ = \"[^\"]+\"",
        '__version__ = "%s"' % version,
        version_data,
    )
    with open(version_path, "w") as f:
        f.truncate()
        f.write(version_data)

    # Build the sdist/wheels
    run("python", "setup.py", "sdist", "bdist_wheel")

    # Test everything that got created
    dists = os.listdir(os.path.join(base_dir, "dist"))
    assert len(dists) == 2
    for dist in dists:
        test_dist(os.path.join(base_dir, "dist", dist))

    run("git", "checkout", "--", "elastic_enterprise_search/")

    # After this run 'python -m twine upload dist/*'
    print(
        "\n\n"
        "===============================\n\n"
        "    * Releases are ready! *\n\n"
        "$ python -m twine upload dist/*\n\n"
        "==============================="
    )


if __name__ == "__main__":
    main()
