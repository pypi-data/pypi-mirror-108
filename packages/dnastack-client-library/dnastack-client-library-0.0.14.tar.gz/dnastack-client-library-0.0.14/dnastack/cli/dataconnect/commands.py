from .tables import commands as tables_commands
from dnastack.cli.utils import assert_config, get_config
from dnastack.client import *
from dnastack.cli.auth.utils import get_oauth_token


@click.group()
@click.pass_context
def dataconnect(ctx):
    assert_config(ctx, "data-connect-url", str)


@dataconnect.command()
@click.pass_context
@click.argument("q")
@click.option("-d", "--download", is_flag=True)
@click.option("-j", "--use-json", "--json", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
def query(ctx, q, download, use_json, raw):
    click.echo(
        dataconnect_client.query(
            get_config(ctx, "data-connect-url", str),
            q,
            download,
            use_json,
            raw,
            get_config(ctx, "oauth_token", dict, False),
        )
    )


dataconnect.add_command(tables_commands.tables)
