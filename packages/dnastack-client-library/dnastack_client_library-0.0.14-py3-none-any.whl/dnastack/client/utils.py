import sys

import click
import requests
from requests.exceptions import SSLError, HTTPError
from search_python_client.search import SearchClient, DrsClient
from typing import Optional
import json


def handle_client_results(results, dataconnect_url):
    try:
        yield from results
    except SSLError:
        click.secho(
            f"There was an error retrieving the SSL certificate from {dataconnect_url}",
            fg="red",
        )
        sys.exit(1)
    except HTTPError as e:
        error_res = requests.get(e.response.url)
        error_json = json.loads(error_res.text)
        error_msg = error_json["errors"][0]["title"]
        click.secho(
            f"There was an error querying from {dataconnect_url}: {error_msg}", fg="red"
        )
        sys.exit(1)


def get_dataconnect_client(dataconnect_url, oauth_token: Optional[str] = None):
    # TODO get new token if expired
    if oauth_token:
        dataconnect_client = SearchClient(dataconnect_url, wallet=oauth_token)
    else:
        dataconnect_client = SearchClient(dataconnect_url)

    return dataconnect_client


def get_drs_client(drs_url, oauth_token: Optional[str] = None):
    # TODO get new token if expired
    if oauth_token:
        drs_client = DrsClient(drs_url, wallet=oauth_token)
    else:
        drs_client = DrsClient(drs_url)

    return drs_client
