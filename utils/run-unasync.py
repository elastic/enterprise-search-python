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
from pathlib import Path

import unasync


def main():
    # Unasync all the generated async code
    additional_replacements = {
        # We want to rewrite to 'Transport' instead of 'SyncTransport', etc
        "AsyncTransport": "Transport",
        "AsyncAppSearch": "AppSearch",
        "AsyncEnterpriseSearch": "EnterpriseSearch",
        "AsyncWorkplaceSearch": "WorkplaceSearch",
        "_AsyncAppSearch": "_AppSearch",
        "_AsyncEnterpriseSearch": "_EnterpriseSearch",
        "_AsyncWorkplaceSearch": "_WorkplaceSearch",
    }
    rules = [
        unasync.Rule(
            fromdir="/elastic_enterprise_search/_async/client/",
            todir="/elastic_enterprise_search/_sync/client/",
            additional_replacements=additional_replacements,
        ),
    ]

    filepaths = []
    for root, _, filenames in os.walk(
        Path(__file__).absolute().parent.parent / "elastic_enterprise_search/_async"
    ):
        for filename in filenames:
            if filename.rpartition(".")[-1] in (
                "py",
                "pyi",
            ):
                filepaths.append(os.path.join(root, filename))

    unasync.unasync_files(filepaths, rules)


if __name__ == "__main__":
    main()
