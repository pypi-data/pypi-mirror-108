import click
from tabulate import tabulate

from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(
    name="list",
    short_help="List your Users",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_list(options: GlobalOptions) -> None:
    """Prints a table view of Sym Users in your Organization and their corresponding identities to STDOUT.

    To view in CSV format or modify users, use `symflow users edit`.
    """

    api = SymAPI(url=options.api_url)
    users = api.get_users()
    integrations = api.get_integrations()
    fields = ["email"] + [x["name"] for x in integrations]

    rows = []
    for user in users:
        row_data = dict(
            {i["integration"]["name"]: i["identifier"] for i in user["identities"]},
            **{"email": user["email"]},
        )
        rows.append([row_data.get(f, "") for f in fields])

    click.echo(tabulate(rows, headers=fields) + "\n")
