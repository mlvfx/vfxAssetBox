"""
Base actions to be use as a template, and to store generic actions.
"""
import os
from assetbox.base.constants import ActionType
from PySide import QtGui


def filename_input(title='Name Input', outputtext='Text: '):
    """
    Decorator to add a file dialog input.

    Args:
        title (str): title of the file dialog.
        outputtext (str): hint text about what we are doing.

    Returns:
        str: the path found in the dialog.
    """
    def name_decorate(func):
        def func_wrapper(self, path):
            text, ok = QtGui.QInputDialog.getText(None, title, outputtext+path)
            if ok and text:
                output_path = '{0}/{1}'.format(path, text)
                return func(self, output_path)
        return func_wrapper
    return name_decorate


def confirm_dialog(title='Confirm', message='Text:'):
    """
    Decorator to add a confirmation dialog.

    Args:
        title (str): title of the confirm dialog.
        message (str): hint text about what we are doing.

    Returns:
        str: the path confirmed in the dialog.
    """
    def dialog_decorate(func):
        def func_wrapper(self, path):
            confirm = QtGui.QMessageBox.question(None,
                                                 title,
                                                 message,
                                                 QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                 QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.Yes:
                return func(self, path)
            else:
                return func(self, '')
        return func_wrapper
    return dialog_decorate


class BaseAction(object):
    """Base Action template, a skeleton for an action."""

    NAME = 'BaseAction'
    FILETYPE = 'abc'
    ACTIONTYPE = ActionType.Menu

    def __init__(self):
        pass

    def valid_filetype(self, path, *args):
        """Check the asset selected is valid."""
        name, ext = os.path.splitext(path)

        return ext.replace('.', '') == self.FILETYPE

    def execute(self):
        """Run the command."""
        raise NotImplementedError


class Delete(BaseAction):
    """Delete command that mimics the operating systems delete."""

    NAME = 'Delete'
    FILETYPE = 'abc'

    @confirm_dialog('Confirm Deletion', 'Are you sure you want to delete this?')
    def execute(self, path, **kwargs):
        """Run the command."""
        if self.valid_filetype(path):
            #TODO: remove from list widget and support multiple file types
            os.remove(path)


def register_actions(*args):
    """Register all the base actions into the host app."""
    return [Delete()]
