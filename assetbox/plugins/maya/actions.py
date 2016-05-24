"""
Maya Actions, commands and functions used in Autodesk Maya.
"""
from assetbox.base.plugins.actions import BaseAction, filename_input
import os


class AbcImport(BaseAction):
    """Action to import an Alembic file."""

    NAME = 'ABC Import'
    FILETYPE = 'abc'

    def execute(self, path, **kwargs):
        """Run the command."""
        if self.valid_filetype(path):
            import maya.cmds as cmds
            cmds.AbcImport(str(path))


class PngImport(BaseAction):
    """Action to import a png and create a Maya File node."""

    NAME = 'PNG Import'
    FILETYPE = 'png'

    def execute(self, path, **kwargs):
        """Run the command."""
        if self.valid_filetype(path):
            import maya.mel as mel
            mel.eval('importImageFile "%s" "false" "false" `optionVar -query createTexturesWithPlacement`;' % str(path))


class AbcExportStatic(BaseAction):
    """Exports an alembic file, based on frame 0."""

    NAME = 'Alembic Static Export'
    FILETYPE = 'abc'
    ACTIONTYPE = 2

    @filename_input('Export Alembic', 'Output Path: ')
    def execute(self, path, **kwargs):
        """Run the command."""
        import maya.cmds as cmds
        selection = cmds.ls(sl=True)
        if selection:
            output_path = '{0}.abc'.format(path).replace("\\", "/")

            path = os.path.dirname(os.path.abspath(output_path))
            if not os.path.isdir(path):
                print 'No found file: %s' % path
                return None

            selection_command = '-root ' + ' -root '.join(selection)
            file_output = '-file {0}'.format(output_path)
            options_str = '-uvWrite -worldSpace -dataFormat ogawa'
            frame_str = '-frameRange 0 0'
            job_command = '{0} {1} {2} {3}'.format(frame_str,
                                                   options_str,
                                                   selection_command,
                                                   file_output)

            cmds.AbcExport(j=job_command)

            return output_path
        else:
            return None


class AbcExport(BaseAction):
    """Exports an alembic file, based on the scene frame range."""

    NAME = 'Alembic Export'
    FILETYPE = 'abc'
    ACTIONTYPE = 2

    @filename_input('Export Alembic', 'Output Path: ')
    def execute(self, path, **kwargs):
        """Run the command."""
        import maya.cmds as cmds
        selection = cmds.ls(sl=True)
        if selection:
            output_path = '{0}.abc'.format(path).replace("\\", "/")

            path = os.path.dirname(os.path.abspath(output_path))
            if not os.path.isdir(path):
                print 'No found file: %s' % path
                return None

            selection_command = '-root ' + ' -root '.join(selection)
            file_output = '-file {0}'.format(output_path)
            options_str = '-uvWrite -worldSpace -dataFormat ogawa'
            frame_str = '-frameRange {0} {1}'.format(cmds.playbackOptions(q=True, min=True),
                                                     cmds.playbackOptions(q=True, max=True))

            job_command = '{0} {1} {2} {3}'.format(frame_str,
                                                   options_str,
                                                   selection_command,
                                                   file_output)

            cmds.AbcExport(j=job_command)

            return output_path
        else:
            return None


def register_actions(*args):
    """Register all the actions into the host app."""
    return [AbcImport(), PngImport(), AbcExportStatic(), AbcExport()]
