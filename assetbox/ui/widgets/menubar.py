"""
The main menu bar for the assetbox interface.
"""
from PySide import QtGui

from assetbox.base import prefs
from assetbox.ui.widgets import filebrowser


class QAssetMenus(QtGui.QMenuBar):
    """
    A menubar holding all the actions for assetbox.
    """
    def __init__(self, parent=None):
        """Initialise the widget. Create the menus and actions."""
        super(QAssetMenus, self).__init__()

        parent.setMenuBar(self)

        file_menu = self.addMenu('Edit')
        set_projects_action = QtGui.QAction('Set Projects Folder',
                                            self,
                                            triggered=self.set_projects_folder)
        file_menu.addAction(set_projects_action)

    def set_projects_folder(self):
        """Sets the primary folder where projects are found."""
        browser = filebrowser.QFileBrowser(parent=self,
                                           text='Set Projects Folder')
        dir_ = browser.get_folder()

        # Setup the preferences.
        self.preferences = prefs.PreferenceHelper()
        self.preferences.load_config()
        self.preferences.set_attr('project', 'projects_folder', dir_)

        return dir_
