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
    run("rm", "-rf", "build/", "dist/", "*.egg-info", ".eggs")

    with open(os.path.join(base_dir, "elastic_enterprise_search/_version.py")) as f:
        version = re.search(
            r"^__version__\s+=\s+[\"\']([^\"\']+)[\"\']", f.read(), re.M
        ).group(1)

    expect_version = sys.argv[1].replace("-alpha", "a").replace("-beta", "b")
    if expect_version != version:
        raise ValueError(
            "Expected version %r, package has version %r" % (expect_version, version)
        )

    # Build the sdist/wheels
    run("python", "setup.py", "sdist", "bdist_wheel")

    # Test everything that got created
    for dist in os.listdir(os.path.join(base_dir, "dist")):
        test_dist(os.path.join(base_dir, "dist", dist))

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
