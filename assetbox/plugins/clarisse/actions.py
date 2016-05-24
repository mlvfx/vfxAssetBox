"""
Clarisse Actions, commands and functions used in Isotropix Clarisse.
"""
from assetbox.base.plugins.actions import BaseAction
import os


class AbcImport(BaseAction):
    """Action to import an Alembic file."""

    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


class PngImport(BaseAction):
    """Action to import a png and create a TextureMapFile."""

    NAME = 'PNG Import'
    FILETYPE = 'png'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            name, ext = os.path.splitext(os.path.basename(path))
            texture_file = ix.create_object(str(name), 'TextureMapFile')
            texture_file.get_attribute('filename').set_string(str(path))
            print 'Created TextureMapFile: {0}'.format(name)


class VdbImport(BaseAction):
    """Action to import a volume vdb."""

    NAME = 'VDB Import'
    FILETYPE = 'vdb'

    def execute(self, path, **kwargs):
        if self.valid_filetype(path):
            import ix
            ix.import_scene(str(path))


def register_actions(*args):
    """Register all the actions into the host app."""
    return [AbcImport(), PngImport(), VdbImport()]
