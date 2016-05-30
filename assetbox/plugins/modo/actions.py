"""
Modo Actions, commands and functions used in The Foundry Modo.
"""
from assetbox.base.plugins.actions import BaseAction


class AbcImport(BaseAction):
    """Action to import an Alembic file.

    TODO: update to work properly in Modo.
    """

    name = 'ABC Import'
    filetype = 'abc'

    def execute(self, path, **kwargs):
        """Run the command."""
        if self.valid_filetype(path):
            print path


def register_actions(*args):
    """Register all the actions into the host app."""
    return [AbcImport()]
