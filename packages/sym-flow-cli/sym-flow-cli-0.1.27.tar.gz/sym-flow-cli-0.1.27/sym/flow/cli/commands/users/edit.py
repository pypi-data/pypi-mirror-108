import csv

import click

from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.csv import set_connectors
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(
    name="edit",
    short_help="Edit your Users in a CSV",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("csv_path", type=click.Path(writable=True))
def users_edit(options: GlobalOptions, csv_path: str) -> None:
    """Generates a CSV containing all Sym Users in your Organization and their identities for configured Sym Integrations.

    \b
    Example:
        `symflow users edit my-users.csv
    """

    api = SymAPI(url=options.api_url)
    users = api.get_users()
    integrations = api.get_integrations()
    fields = ["email"] + [x["name"] for x in integrations]

    with open(csv_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for user in users:
            writer.writerow(
                dict(
                    {
                        i["integration"]["name"]: i["identifier"]
                        for i in user["identities"]
                    },
                    **{"email": user["email"]},
                )
            )
    set_connectors(csv_path, integrations)
