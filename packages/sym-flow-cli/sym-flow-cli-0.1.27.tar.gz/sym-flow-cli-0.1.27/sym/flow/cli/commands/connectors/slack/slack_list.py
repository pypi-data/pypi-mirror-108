import click
from tabulate import tabulate

from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.api import ConnectorType, SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="list", short_help="List Sym Slack App installations")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def slack_list(options: GlobalOptions) -> None:
    """Lists out information about what Slack workspaces the Sym Slack App is
    installed in.
    """

    click.echo(get_slack_connectors_table(options.api_url))


def get_slack_connectors_table(api_url: str):
    """Returns tabulated Slack connectors or raises SymAPIRequestError."""
    api = SymAPI(url=api_url)
    connectors = api.get_connectors(ConnectorType.SLACK.value)

    rows = []
    try:
        for connector in connectors:
            settings = connector["settings"]
            rows.append([settings["team_name"], settings["team_id"]])
    except KeyError as err:
        raise SymAPIRequestError(
            "Failed to parse data received from the Sym API", api.get_last_request_id()
        ) from err

    return tabulate(rows, headers=["Workspace Name", "Workspace ID"])
