import requests as req


def get_collections(collections_url):
    return req.get(collections_url).json()


def get_collection_tables(collections_url, collection_name):
    collection_tables_url = f"{collections_url}/{collection_name}/search/tables"
    return req.get(collection_tables_url).json()


def query_collection(collections_url, collection_name, query):
    collection_query_url = f"{collections_url}/{collection_name}/search/search"
    return req.post(collection_query_url, json={"query": query}).json()
