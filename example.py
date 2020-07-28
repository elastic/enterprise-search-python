from elastic_enterprise_search import EnterpriseSearch


ent = EnterpriseSearch(
    host="77f027a04727422a9dddffc4da29743a.ent-search.us-central1.gcp.cloud.es.io",
    use_ssl=True,
    # Translates to 'Authorization: Basic ...' in headers
    http_auth=("elastic", "<password>"),
)
print(ent.get_version())

# Can set HTTP auth on sub-clients via properties:
ent.workplace_search.http_auth = "<content source access token>"
print(ent.workplace_search.list_all_permissions())
ent.workplace_search.index_documents(
    content_source_key="<content source key>",
    body=[{"id": "1", "title": "", "url": ""}],
)

# You can instantiate clients on their own if needed as well:
from elastic_enterprise_search import AppSearch

app_search = AppSearch(host="localhost", port=3002, http_auth="<app search token>")
resp = app_search.search(engine_name="engine", body={"query": "give me documents!"})
