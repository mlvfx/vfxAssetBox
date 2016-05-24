"""
Houdini Actions, commands and functions used in Sidefx Houdini.
"""
from assetbox.base.plugins.actions import BaseAction
import os


class AbcImport(BaseAction):
    """Action to import an Alembic file."""

    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import hou
            name, ext = os.path.splitext((os.path.basename(path)))
            obj = hou.node("/obj")
            abc_node = obj.createNode('alembicarchive', 'abc_%s' % name)
            abc_node.parm('fileName').set(path)
            abc_node.parm('buildHierarchy').pressButton()

            # abc_node.setCurrent()
            abc_node.moveToGoodPosition()
            abc_node.setSelected(True, clear_all_selected=True, show_asset_if_selected=True)


def register_actions(*args):
    """Register all the actions into the host app."""
    return [AbcImport()]
