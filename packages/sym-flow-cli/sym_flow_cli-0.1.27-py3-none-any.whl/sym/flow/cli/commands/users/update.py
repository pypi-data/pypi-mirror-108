import click

from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(name="update", short_help="Upload a CSV with new User Identities")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument(
    "csv_path",
    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False),
)
def users_update(options: GlobalOptions, csv_path: str) -> None:
    """Upload data from a CSV to update Sym Users in your Organization. This can be used to create or modify Sym Users and identities such as AWS SSO IDs.

    \b
    Example:
        `symflow users update my-users.csv`
    """

    with open(csv_path) as f:
        result = SymAPI(url=options.api_url).update_users(f.read())
    click.secho(f"Successfully updated {len(result)} Users!")
