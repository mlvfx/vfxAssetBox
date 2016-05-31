"""
Vfx AssetBox is a cross-platform multi-software asset toolkit.

Managing assets across software can be difficult, vfxAssetBox helps
to manage models, textures, and anything else when working on small-scale to
large projects.

Software currently supported includes Maya, Modo, Mari, Clarisse, Nuke,
and anything that supports PySide.

"""
import os
from functools import partial
import time

from PySide import QtGui

# import assetbox.ui.contact_sheet as contact_sheet
# reload(contact_sheet)

from assetbox.ui.panels import breadcrumb
from assetbox.ui.widgets import menubar
from assetbox.ui.panels import path_line, asset_list, action_buttons, folder_tree, project_selector
import assetbox.ui.qthelpers as qthelpers
reload(breadcrumb)

from assetbox.base.constants import ActionType

import assetbox.ui.style.palette as palette
reload(palette)

from assetbox.base.assets import Location, Asset
from assetbox.base import helpers
from assetbox.base import prefs

import logging

LOGGER = logging.getLogger(__name__)


class AssetBoxWindow(QtGui.QMainWindow):
    host = None
    actions = []
    filetypes = []

    def __init__(self, parent=None):
        super(AssetBoxWindow, self).__init__(parent)
        self.setWindowTitle("VFX AssetBox")
        self.resize(700, 500)

        self.setWindowIcon(QtGui.QIcon('G:/Scripts/vfxAssetBox/icons/icon.32x32.png'))

        # with open('G:/Scripts/vfxAssetManager/ui/style/darkorange.stylesheet', 'r') as file:
        #     style_sheet = file.read()
        # self.setStyleSheet(style_sheet)
        # palette.load_theme(self)
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Gtk'))

        # Default values.
        self.current_locations = {'project': '', 'project_folder': '',
                                  'variant': '', 'variant_folder': '',
                                  'asset': '', 'asset_folder': ''}

        # Main layout widgets.
        main_widget = QtGui.QWidget()
        self. main_layout = QtGui.QHBoxLayout()
        qthelpers.clean_layouts(self.main_layout)
        main_widget.setLayout(self.main_layout)

        # Set the main layout.
        self.setCentralWidget(main_widget)

        # Setup the menubar.
        self.menubar = menubar.QAssetMenus(parent=self)

        # Setup the preferences.
        self.prefs = prefs.PreferenceHelper()
        self.prefs.load_config()
        self.projects_folder = self.prefs.get_attr('project', 'projects_folder')
        self.default_project = self.prefs.get_attr('project', 'default_project')

        # Settings likely do not exist, create the projects folder.
        if not self.projects_folder:
            self.projects_folder = self.menubar.set_projects_folder()

        # Setup the variants vbox.
        self.variants = self._variant_layout()
        qthelpers.clean_layouts(self.variants)
        self.projects_combo = project_selector.QProjectCombo(parent=self.variants,
                                                             project=self.default_project)
        self.variants.addWidget(QtGui.QLabel('Folders:'))
        self.folder_tree = folder_tree.QFolderTree(parent=self.variants)

        # Setup the assets vbox.
        self.assets = self._asset_layout()
        self.breadcrumb = breadcrumb.QBreadcrumb(parent=self)
        self.assets.addWidget(self.breadcrumb)
        self.asset_list = asset_list.QAssetListWidget(parent=self.assets)
        self.asset_list.list_widget().customContextMenuRequested.connect(self.selected_asset_rightclicked)
        self.asset_list.list_widget().itemClicked.connect(self.selected_asset)

        # self.texture_widget = contact_sheet.QdContactSheet()
        # self.assets.addWidget(self.texture_widget)
        self.actionbuttons = action_buttons.QActionButtons(parent=self.assets)
        self.path_line = path_line.QPath(parent=self.assets)

        # Initial population.
        self.projects_combo.populate_projects(self.projects_folder)
        self._populate_variants()

        # Signal for project changes.
        self.projects_combo.combobox().currentIndexChanged.connect(self._populate_variants)
        self.folder_tree.itemClicked.connect(self._populate_assets)

    def selected_asset(self, item):
        """
        Triggers when an asset is selected in the asset tree,
        provides information to the info section

        Args:
            item(Asset): pass in an Asset object
        """
        self.path_line.set_text(item.get_path())

    def selected_asset_rightclicked(self, QPos):
        """
        Action used when an asset is rightclicked

        Args:
            QPos(QPosition): location where the right click happened
        """
        item = self.asset_list.list_widget().itemAt(QPos)
        if item is not None:
            if item.get_actions():
                menu = QtGui.QMenu("Context Menu", self)
                for action in item.get_actions():
                    if action.actiontype == ActionType.Menu:
                        _partial = partial(self.rightclick_action_run,
                                           action,
                                           item.get_path())
                        qaction = QtGui.QAction(action.name,
                                                self,
                                                triggered=_partial)
                        menu.addAction(qaction)
                menu.exec_(self.asset_list.list_widget().mapToGlobal(QPos))

    def rightclick_action_run(self, action, path):
        action.execute(path=path)
        # TODO: remove this hack to check for deletion
        time.sleep(2)  # wait till deletion is done
        if not os.path.isfile(path):
            self.asset_list.list_widget().takeItem(self.asset_list.list_widget().currentRow())

    def add_buttons(self):
        valid_actions = [a for a in self.actions if a.actiontype == 2]
        for action in valid_actions:
            _partial = partial(self.get_path, action)
            self.actionbuttons.add_button(name=action.name, action=_partial)

    def get_path(self, action):
        asset = action.execute(path=self.asset_list.path())
        if not asset:
            return False

        name = os.path.basename(asset)
        if os.path.isfile(asset):
            asset_obj = Asset(None, name, asset)
            valid_actions = [a for a in self.actions
                             if a.filetype == asset_obj.filetype]
            asset_obj.add_actions(valid_actions)

            self.asset_list.add_item(asset_obj)
            self.asset_list.list_widget().scrollToItem(asset_obj)

    def _populate_variants(self):
        self.set_default_project()
        self.folder_tree.clear()

        self.current_locations['project'] = self.projects_combo.text()
        self.current_locations['project_folder'] = helpers.join_path(self.projects_folder, self.current_locations['project'])

        self.folder_directoy = {}
        root_dir = self.current_locations['project_folder'].rstrip(os.sep)
        start = root_dir.rfind(os.sep) + 1

        parent_item = self.folder_tree

        for root, dirnames, filenames in os.walk(root_dir):
            folders = root[start:].split(os.sep)

            try:
                if not folders[-2] == root_dir:
                    parent_item = self.folder_directoy.get(folders[-2])
                else:
                    parent_item = self.folder_tree
            except IndexError:
                parent_item = self.folder_tree

            if not folders[-1] == root_dir:
                self.folder_directoy[folders[-1]] = Location(parent=parent_item,
                                                             name=folders[-1],
                                                             path=root)

    def _populate_assets(self, item):
        item.setExpanded(True)
        self.breadcrumb._hide_all()
        self.breadcrumb.set_breadcrumb_label(item)
        self.asset_list.set_path(item.get_path())

        self.asset_list.clear()
        self.path_line.set_text(item.get_path())

        for ft in self.filetypes:
            for asset in helpers.get_files(item.get_path(), pattern='*.%s' % ft):
                name = os.path.basename(asset)
                if os.path.isfile(asset):
                    asset_obj = Asset(None, name, asset)
                    valid_actions = [a for a in self.actions if a.filetype == asset_obj.filetype]
                    asset_obj.add_actions(valid_actions)

                    self.asset_list.add_item(asset_obj)

        images = helpers.get_files(item.get_path(), pattern='*.png')
        images.sort()
        # self.texture_widget.load(images)

    def _variant_layout(self):
        variant_widget = QtGui.QWidget()
        variant_widget.setFixedWidth(200)
        variant_vlayout = QtGui.QVBoxLayout(variant_widget)
        qthelpers.clean_layouts(variant_vlayout)

        self.main_layout.addWidget(variant_widget)

        return variant_vlayout

    def _asset_layout(self):
        asset_widget = QtGui.QWidget()
        asset_layout = QtGui.QVBoxLayout(asset_widget)
        qthelpers.clean_layouts(asset_layout)

        self.main_layout.addWidget(asset_widget)

        return asset_layout

    def set_default_project(self):
        """Set the default project from current."""
        project = self.projects_combo.text()
        self.prefs.load_config()
        self.prefs.set_attr('project', 'default_project', project)

    def closeEvent(self, event):
        pass
        # self.prefs.config.set('ui', 'view_mode', 'list')
        # self.prefs.save_config()
