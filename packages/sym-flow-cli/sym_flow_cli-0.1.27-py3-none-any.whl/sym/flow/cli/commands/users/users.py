import click
from sym.shared.cli.helpers.sym_group import SymGroup

from sym.flow.cli.commands.users.edit import users_edit
from sym.flow.cli.commands.users.list import users_list
from sym.flow.cli.commands.users.template import users_template
from sym.flow.cli.commands.users.update import users_update
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.group(name="users", cls=SymGroup, short_help="Perform operations on Sym Users")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users(options: GlobalOptions) -> None:
    """Operations on Users"""


users.add_command(users_list)
users.add_command(users_edit)
users.add_command(users_update)
users.add_command(users_template)
