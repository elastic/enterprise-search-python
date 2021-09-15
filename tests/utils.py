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


def pop_nested_json(from_, nested_key):
    """Utility function that pops a nested+dotted JSON key"""
    key_parts = nested_key.split(".")
    if len(key_parts) > 1:
        for i, key_part in enumerate(key_parts[:-1]):
            if key_part == "*":
                assert isinstance(from_, list)
                for item in from_:
                    pop_nested_json(item, ".".join(key_parts[i + 1 :]))
                break
            else:
                from_ = from_[key_part]
        else:
            from_.pop(key_parts[-1])
    else:
        from_.pop(nested_key)
