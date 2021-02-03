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

import jwt
import pytest

from elastic_enterprise_search import AppSearch, UnauthorizedError


@pytest.fixture()
def app_search():
    yield AppSearch(
        "http://localhost:3002", http_auth="private-k3ra4bqu12vgnhe3wibdw69f"
    )


@pytest.mark.vcr()
def test_list_engines(app_search):
    resp = app_search.list_engines()

    assert resp.status == 200
    assert resp == {
        "meta": {
            "page": {"current": 1, "total_pages": 1, "total_results": 1, "size": 25}
        },
        "results": [
            {"name": "national-parks-demo", "type": "default", "language": None}
        ],
    }


@pytest.mark.vcr()
def test_list_documents(app_search):
    resp = app_search.list_documents(
        engine_name="national-parks-demo", page_size=2, current_page=3
    )
    assert resp.status == 200
    assert resp == {
        "meta": {
            "page": {"current": 3, "total_pages": 30, "total_results": 59, "size": 2}
        },
        "results": [
            {
                "nps_link": "https://www.nps.gov/zion/index.htm",
                "title": "Zion",
                "date_established": "1919-11-19T06:00:00+00:00",
                "world_heritage_site": "false",
                "states": ["Utah"],
                "description": "Located at the junction of the Colorado Plateau, Great Basin, and Mojave Desert, this park contains sandstone features such as mesas, rock towers, and canyons, including the Virgin River Narrows. The various sandstone formations and the forks of the Virgin River create a wilderness divided into four ecosystems: desert, riparian, woodland, and coniferous forest.",
                "visitors": 4295127.0,
                "id": "park_zion",
                "location": "37.3,-113.05",
                "square_km": 595.8,
                "acres": 147237.02,
            },
            {
                "nps_link": "https://www.nps.gov/yell/index.htm",
                "title": "Yellowstone",
                "date_established": "1872-03-01T06:00:00+00:00",
                "world_heritage_site": "true",
                "states": ["Wyoming", "Montana", "Idaho"],
                "description": "Situated on the Yellowstone Caldera, the park has an expansive network of geothermal areas including boiling mud pots, vividly colored hot springs such as Grand Prismatic Spring, and regularly erupting geysers, the best-known being Old Faithful. The yellow-hued Grand Canyon of the Yellowstone River contains several high waterfalls, while four mountain ranges traverse the park. More than 60 mammal species including gray wolves, grizzly bears, black bears, lynxes, bison, and elk, make this park one of the best wildlife viewing spots in the country.",
                "visitors": 4257177.0,
                "id": "park_yellowstone",
                "location": "44.6,-110.5",
                "square_km": 8983.2,
                "acres": 2219790.71,
            },
        ],
    }


@pytest.mark.vcr()
def test_delete_documents(app_search):
    resp = app_search.delete_documents(
        engine_name="national-parks-demo",
        document_ids=[
            "park_yellowstone",
            "park_zion",
        ],
    )
    assert resp.status == 200
    assert resp == [
        {"id": "park_yellowstone", "deleted": True},
        {"id": "park_zion", "deleted": True},
    ]


@pytest.mark.vcr()
def test_index_documents(app_search):
    resp = app_search.index_documents(
        engine_name="national-parks-demo",
        documents=[
            {
                "nps_link": "https://www.nps.gov/zion/index.htm",
                "title": "Zion",
                "date_established": "1919-11-19T06:00:00+00:00",
                "world_heritage_site": "false",
                "states": ["Utah"],
                "description": "Located at the junction of the Colorado Plateau, Great Basin, and Mojave Desert, this park contains sandstone features such as mesas, rock towers, and canyons, including the Virgin River Narrows. The various sandstone formations and the forks of the Virgin River create a wilderness divided into four ecosystems: desert, riparian, woodland, and coniferous forest.",
                "visitors": 4295127.0,
                "id": "park_zion",
                "location": "37.3,-113.05",
                "square_km": 595.8,
                "acres": 147237.02,
            },
            {
                "nps_link": "https://www.nps.gov/yell/index.htm",
                "title": "Yellowstone",
                "date_established": "1872-03-01T06:00:00+00:00",
                "world_heritage_site": "true",
                "states": ["Wyoming", "Montana", "Idaho"],
                "description": "Situated on the Yellowstone Caldera, the park has an expansive network of geothermal areas including boiling mud pots, vividly colored hot springs such as Grand Prismatic Spring, and regularly erupting geysers, the best-known being Old Faithful. The yellow-hued Grand Canyon of the Yellowstone River contains several high waterfalls, while four mountain ranges traverse the park. More than 60 mammal species including gray wolves, grizzly bears, black bears, lynxes, bison, and elk, make this park one of the best wildlife viewing spots in the country.",
                "visitors": 4257177.0,
                "id": "park_yellowstone",
                "location": "44.6,-110.5",
                "square_km": 8983.2,
                "acres": 2219790.71,
            },
        ],
    )
    assert resp.status == 200
    assert resp == [
        {"id": "park_zion", "errors": []},
        {"id": "park_yellowstone", "errors": []},
    ]


@pytest.mark.vcr()
def test_search(app_search):
    resp = app_search.search(
        engine_name="national-parks-demo", body={"query": "tree", "page": {"size": 2}}
    )
    assert resp.status == 200
    assert resp == {
        "meta": {
            "alerts": [],
            "warnings": [],
            "page": {"current": 1, "total_pages": 12, "total_results": 23, "size": 2},
            "engine": {"name": "national-parks-demo", "type": "default"},
            "request_id": "4999a4ef-b750-4bef-aea2-87f54d9c87b3",
        },
        "results": [
            {
                "nps_link": {"raw": "https://www.nps.gov/grsm/index.htm"},
                "title": {"raw": "Great Smoky Mountains"},
                "date_established": {"raw": "1934-06-15T05:00:00+00:00"},
                "world_heritage_site": {"raw": "true"},
                "states": {"raw": ["Tennessee", "North Carolina"]},
                "description": {
                    "raw": "The Great Smoky Mountains, part of the Appalachian Mountains, span a wide range of elevations, making them home to over 400 vertebrate species, 100 tree species, and 5000 plant species. Hiking is the park's main attraction, with over 800 miles (1,300 km) of trails, including 70 miles (110 km) of the Appalachian Trail. Other activities include fishing, horseback riding, and touring nearly 80 historic structures."
                },
                "visitors": {"raw": 11312786.0},
                "_meta": {
                    "id": "park_great-smoky-mountains",
                    "engine": "national-parks-demo",
                    "score": 16969184.0,
                },
                "id": {"raw": "park_great-smoky-mountains"},
                "location": {"raw": "35.68,-83.53"},
                "square_km": {"raw": 2114.2},
                "acres": {"raw": 522426.88},
            },
            {
                "nps_link": {"raw": "https://www.nps.gov/yose/index.htm"},
                "title": {"raw": "Yosemite"},
                "date_established": {"raw": "1890-10-01T05:00:00+00:00"},
                "world_heritage_site": {"raw": "true"},
                "states": {"raw": ["California"]},
                "description": {
                    "raw": "Yosemite features sheer granite cliffs, exceptionally tall waterfalls, and old-growth forests at a unique intersection of geology and hydrology. Half Dome and El Capitan rise from the park's centerpiece, the glacier-carved Yosemite Valley, and from its vertical walls drop Yosemite Falls, one of North America's tallest waterfalls at 2,425 feet (739 m) high. Three giant sequoia groves, along with a pristine wilderness in the heart of the Sierra Nevada, are home to a wide variety of rare plant and animal species."
                },
                "visitors": {"raw": 5028868.0},
                "_meta": {
                    "id": "park_yosemite",
                    "engine": "national-parks-demo",
                    "score": 7543302.0,
                },
                "id": {"raw": "park_yosemite"},
                "location": {"raw": "37.83,-119.5"},
                "square_km": {"raw": 3082.7},
                "acres": {"raw": 761747.5},
            },
        ],
    }


@pytest.mark.vcr()
def test_not_authorized(app_search):
    app_search.http_auth = None
    with pytest.raises(UnauthorizedError) as e:
        app_search.list_engines()
    assert e.value.status == 401
    assert e.value.message == {"error": "You need to sign in before continuing."}
    assert e.value.errors == ()

    resp = app_search.list_engines(ignore_status=401)
    assert resp.status == 401
    assert resp == {"error": "You need to sign in before continuing."}


@pytest.mark.vcr()
def test_meta_engine(app_search):
    # Create some source engines
    resp = app_search.create_engine(
        engine_name="source-engine-1",
        type="default",
        language="en",
    )
    assert resp.status == 200
    assert resp == {
        "document_count": 0,
        "language": "en",
        "name": "source-engine-1",
        "type": "default",
    }

    resp = app_search.create_engine(
        engine_name="source-engine-2",
    )
    assert resp.status == 200
    assert resp == {
        "document_count": 0,
        "language": None,
        "name": "source-engine-2",
        "type": "default",
    }

    # Create a meta engine
    resp = app_search.create_engine(
        engine_name="meta-engine",
        type="meta",
        source_engines=["source-engine-1", "source-engine-2"],
    )
    assert resp.status == 200
    assert resp == {
        "document_count": 0,
        "name": "meta-engine",
        "source_engines": ["source-engine-1", "source-engine-2"],
        "type": "meta",
    }

    # Delete some source engines
    resp = app_search.delete_engine(engine_name="source-engine-2")
    assert resp.status == 200
    assert resp == {"deleted": True}

    resp = app_search.delete_engine(engine_name="source-engine-1")
    assert resp.status == 200
    assert resp == {"deleted": True}

    # See the meta engine has no source engines
    resp = app_search.get_engine(engine_name="meta-engine")
    assert resp.status == 200
    assert resp == {
        "document_count": 0,
        "name": "meta-engine",
        "source_engines": [],
        "type": "meta",
    }

    # Use the add_meta_engine_source() API
    app_search.create_engine(engine_name="source-engine-added")
    resp = app_search.add_meta_engine_source(
        engine_name="meta-engine", source_engines=["source-engine-added"]
    )
    assert resp.status == 200
    assert resp == {
        "document_count": 0,
        "name": "meta-engine",
        "source_engines": ["source-engine-added"],
        "type": "meta",
    }


@pytest.mark.vcr()
def test_query_suggestions(app_search):
    resp = app_search.query_suggestion(
        engine_name="national-parks-demo",
        query="ca",
        fields=["title", "states"],
    )
    assert resp.status == 200
    assert resp == {
        "meta": {"request_id": "15a4ce10-1d5b-49d0-a83f-f4cf35b0e45e"},
        "results": {
            "documents": [
                {"suggestion": "cave"},
                {"suggestion": "capitol"},
                {"suggestion": "capitol reef"},
                {"suggestion": "canyon"},
                {"suggestion": "california"},
                {"suggestion": "canyonlands"},
                {"suggestion": "carlsbad caverns"},
                {"suggestion": "cascades"},
                {"suggestion": "carolina"},
                {"suggestion": "canyon of"},
            ]
        },
    }


@pytest.mark.vcr()
def test_multi_search(app_search):
    resp = app_search.multi_search(
        engine_name="national-parks-demo",
        body={
            "queries": [
                {"query": "rock", "page": {"size": 1}},
                {"query": "lake", "page": {"size": 1}},
            ]
        },
    )
    assert resp.status == 200
    assert resp == [
        {
            "meta": {
                "alerts": [],
                "warnings": [],
                "page": {
                    "current": 1,
                    "total_pages": 15,
                    "total_results": 15,
                    "size": 1,
                },
                "engine": {"name": "national-parks-demo", "type": "default"},
            },
            "results": [
                {
                    "nps_link": {"raw": "https://www.nps.gov/romo/index.htm"},
                    "title": {"raw": "Rocky Mountain"},
                    "date_established": {"raw": "1915-01-26T06:00:00+00:00"},
                    "world_heritage_site": {"raw": "false"},
                    "states": {"raw": ["Colorado"]},
                    "description": {
                        "raw": "Bisected north to south by the Continental Divide, this portion of the Rockies has ecosystems varying from over 150 riparian lakes to montane and subalpine forests to treeless alpine tundra. Wildlife including mule deer, bighorn sheep, black bears, and cougars inhabit its igneous mountains and glacial valleys. Longs Peak, a classic Colorado fourteener, and the scenic Bear Lake are popular destinations, as well as the historic Trail Ridge Road, which reaches an elevation of more than 12,000 feet (3,700 m)."
                    },
                    "visitors": {"raw": 4517585.0},
                    "_meta": {
                        "id": "park_rocky-mountain",
                        "engine": "national-parks-demo",
                        "score": 6776379.0,
                    },
                    "id": {"raw": "park_rocky-mountain"},
                    "location": {"raw": "40.4,-105.58"},
                    "square_km": {"raw": 1075.6},
                    "acres": {"raw": 265795.2},
                }
            ],
        },
        {
            "meta": {
                "alerts": [],
                "warnings": [],
                "page": {
                    "current": 1,
                    "total_pages": 17,
                    "total_results": 17,
                    "size": 1,
                },
                "engine": {"name": "national-parks-demo", "type": "default"},
            },
            "results": [
                {
                    "nps_link": {"raw": "https://www.nps.gov/romo/index.htm"},
                    "title": {"raw": "Rocky Mountain"},
                    "date_established": {"raw": "1915-01-26T06:00:00+00:00"},
                    "world_heritage_site": {"raw": "false"},
                    "states": {"raw": ["Colorado"]},
                    "description": {
                        "raw": "Bisected north to south by the Continental Divide, this portion of the Rockies has ecosystems varying from over 150 riparian lakes to montane and subalpine forests to treeless alpine tundra. Wildlife including mule deer, bighorn sheep, black bears, and cougars inhabit its igneous mountains and glacial valleys. Longs Peak, a classic Colorado fourteener, and the scenic Bear Lake are popular destinations, as well as the historic Trail Ridge Road, which reaches an elevation of more than 12,000 feet (3,700 m)."
                    },
                    "visitors": {"raw": 4517585.0},
                    "_meta": {
                        "id": "park_rocky-mountain",
                        "engine": "national-parks-demo",
                        "score": 6776381.5,
                    },
                    "id": {"raw": "park_rocky-mountain"},
                    "location": {"raw": "40.4,-105.58"},
                    "square_km": {"raw": 1075.6},
                    "acres": {"raw": 265795.2},
                }
            ],
        },
    ]


def test_create_signed_search_key():
    private_key = "private-"
    signed_key = AppSearch.create_signed_search_key(
        api_key=private_key,
        api_key_name="api-key-name",
        search_fields={"first_name": {}},
        filters={"status": "available"},
        facets=None,
    )
    assert isinstance(signed_key, str)
    assert jwt.decode(signed_key, private_key, algorithms="HS256") == {
        "api_key_name": "api-key-name",
        "facets": None,
        "filters": {"status": "available"},
        "search_fields": {"first_name": {}},
    }


def test_array_type_check(app_search):
    with pytest.raises(TypeError) as e:
        app_search.create_engine(
            engine_name="test-engine", type="meta", source_engines="source-engine"
        )
    assert str(e.value) == "Parameter 'source_engines' must be a tuple or list"
