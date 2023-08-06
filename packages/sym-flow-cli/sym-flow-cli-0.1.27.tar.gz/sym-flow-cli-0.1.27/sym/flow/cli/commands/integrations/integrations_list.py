import datetime

import click
from dateutil.parser import isoparse
from tabulate import tabulate

from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="list", short_help="View all integrations")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def integrations_list(options: GlobalOptions) -> None:
    """View all Sym Integrations currently set up for your organization.

    Sym Integrations can be added or removed via Terraform. For more details,
    see https://docs.symops.com/docs/integrations
    """

    click.echo(get_integration_data(options.api_url))


def get_local_timezone():
    # NB: The reason we are doing this instead of just datetime.datetime.now().astimezone().tzinfo
    # is because you can't call astimezone() on a naive datetime object prior to Python 3.6
    return (
        datetime.datetime.now(datetime.timezone(datetime.timedelta(0)))
        .astimezone()
        .tzinfo
    )


def get_integration_data(api_url: str) -> str:
    api = SymAPI(url=api_url)
    integration_data = api.get_integrations()

    local_tz = get_local_timezone()
    result = []
    try:
        for integration in integration_data:
            updated_at = isoparse(str(integration["updated_at"])).astimezone(local_tz)
            updated_at = updated_at.strftime("%d %b %Y %I:%M%p")
            result.append([integration["slug"], integration["type"], updated_at])
    except KeyError as err:
        raise SymAPIRequestError(
            "Not all required data was returned by the Sym API", api.get_last_request_id()
        ) from err
    return tabulate(result, headers=["Name", "Type", "Last Updated"])
