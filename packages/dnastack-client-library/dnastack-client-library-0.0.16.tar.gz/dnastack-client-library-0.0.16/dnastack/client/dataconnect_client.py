from os import write
import sys
from dnastack.constants import *
from datetime import datetime
from requests.exceptions import SSLError
import click
import json
from requests import HTTPError
from dnastack.client.utils import handle_client_results, get_dataconnect_client
from typing import Optional
import io
import csv


def query(
    dataconnect_url,
    q,
    download=False,
    use_json=False,
    raw=False,
    oauth_token: Optional[str] = None,
):
    dataconnect_client = get_dataconnect_client(dataconnect_url, oauth_token)

    try:
        results = dataconnect_client.search_table(q)
    except:
        sys.exit(1)

    if use_json or not raw:
        output = json.dumps(
            list(handle_client_results(results, dataconnect_url)), indent=4
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        for res in handle_client_results(results, search_url):
            data_row = map(lambda x: str(x).replace(",", "\,"), res.values())
            writer.writerow(data_row)
        output = output.getvalue()

    if download:
        # TODO: be able to specify output file
        download_file = f"{downloads_directory}/query{str(datetime.now())}{'.json' if use_json or not raw else '.csv'}"
        with open(download_file, "w") as fs:
            fs.write(output)
    else:
        return output


def get_tables(dataconnect_url, oauth_token: Optional[str] = None):
    dataconnect_client = get_dataconnect_client(dataconnect_url, oauth_token)

    try:
        tables_iterator = dataconnect_client.get_table_list()
    except HTTPError:
        click.echo(HTTPError.response)
        sys.exit(1)

    return json.dumps(
        list(handle_client_results(tables_iterator, dataconnect_url)), indent=4
    )


def get_table(dataconnect_url, table_name, oauth_token: Optional[str] = None):
    dataconnect_client = get_dataconnect_client(dataconnect_url, oauth_token)

    try:
        table_info = dataconnect_client.get_table_info(table_name)
    except SSLError:
        click.secho(
            f"Unable to retrieve SSL certificate from {dataconnect_url}", fg="red"
        )
        sys.exit(1)
    except HTTPError as error:
        if "404" in str(error.response):
            click.secho(f"Invalid table name: {table_name}.", fg="red")
        else:
            click.echo(error.response)
        sys.exit(1)

    # formatting response to remove unnecessary fields
    results = table_info.to_dict()
    results["name"] = table_info["name"]["$id"]
    results["description"] = table_info["description"]["$id"]

    return json.dumps(results, indent=4)
