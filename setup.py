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
import re

from setuptools import find_packages, setup

base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, "elastic_enterprise_search/_version.py")) as f:
    version = re.search(r"__version__\s+=\s+\"([^\"]+)\"", f.read()).group(1)

# Remove all raw HTML from README for long description
with open(os.path.join(base_dir, "README.md")) as f:
    lines = f.read().split("\n")
    last_html_index = 0
    for i, line in enumerate(lines):
        if line == "</p>":
            last_html_index = i + 1
    long_description = "\n".join(lines[last_html_index:])

packages = [
    package
    for package in find_packages()
    if package.startswith("elastic_enterprise_search")
]


setup(
    name="elastic-enterprise-search",
    description="Python Elastic Enterprise Search Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    author="Elastic",
    author_email="support@elastic.co",
    maintainer="Seth Michael Larson",
    maintainer_email="seth.larson@elastic.co",
    url="https://github.com/elastic/enterprise-search-python",
    project_urls={
        "Source Code": "https://github.com/elastic/enterprise-search-python",
        "Issue Tracker": "https://github.com/elastic/enterprise-search-python/issues",
    },
    packages=packages,
    install_requires=[
        "elastic-transport>=0.dev0,<1.dev0",
        "PyJWT",
        "python-dateutil",
        "six>=1.12",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    extras_require={
        "develop": [
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "pytest-vcr",
            "pytest-freezegun",
            "mock",
            "requests",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
