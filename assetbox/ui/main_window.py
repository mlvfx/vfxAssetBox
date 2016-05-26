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

from PySide import QtCore
from PySide import QtGui

# import assetbox.ui.contact_sheet as contact_sheet
# reload(contact_sheet)

from assetbox.ui import breadcrumb
reload(breadcrumb)

from assetbox.base.constants import ActionType

import assetbox.ui.style.palette as palette
reload(palette)

from assetbox.base.assets import Location, Asset
from assetbox.base import helpers
from assetbox.base import prefs

PROJECTS_FOLDER = 'G:/'
PUBLISH_FOLDER = 'published'
DEFAULT_PROJECT = 'EelCreek'

import logging

LOGGER = logging.getLogger(__name__)


class AssetBoxWindow(QtGui.QMainWindow):
    HOST = None
    ACTIONS = []
    FILETYPES = []

    def __init__(self, parent=None):
        super(AssetBoxWindow, self).__init__(parent)
        self.setWindowTitle("VFX AssetBox")
        self.resize(700, 500)

        # Setup the preferences.
        self.preferences = prefs.PreferenceHelper()
        self.preferences.load_config()

        self.setWindowIcon(QtGui.QIcon('G:/Scripts/vfxAssetBox/icons/icon.32x32.png'))

        # with open('G:/Scripts/vfxAssetManager/ui/style/darkorange.stylesheet', 'r') as file:
        #     style_sheet = file.read()
        # self.setStyleSheet(style_sheet)
        palette.load_theme(self)
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Gtk'))

        # Default values
        self.current_locations = {'project': '', 'project_folder': '',
                                  'project_pub_folder': '',
                                  'variant': '', 'variant_folder': '',
                                  'asset': '', 'asset_folder': ''}

        # Main layout widgets
        main_widget = QtGui.QWidget()
        self. main_layout = QtGui.QHBoxLayout()
        self._clean_layouts(self.main_layout)
        main_widget.setLayout(self.main_layout)

        # Set the main layout
        self.setCentralWidget(main_widget)

        # Setup the variants vbox
        self.variants = self._variant_layout()
        self.variants.addWidget(QtGui.QLabel('Projects:'))
        self.projects_combo = QtGui.QComboBox()
        self.variants.addWidget(self.projects_combo)
        self.variants.addWidget(QtGui.QLabel('Folders:'))
        self.folder_tree_widget = self._tree_widget(parent=self.variants)

        # Setup the assets vbox
        self.assets = self._asset_layout()
        self.breadcrumb = breadcrumb.QBreadcrumb(parent=self)
        self.assets.addWidget(self.breadcrumb)

        self.list_addons = QtGui.QWidget()
        self.list_addons_layout = QtGui.QHBoxLayout(self.list_addons)
        self._clean_layouts(self.list_addons_layout)
        self.assets.addWidget(self.list_addons)

        self.list_addons_layout.addWidget(QtGui.QLabel('Assets:'))
        self.search_lineedit = QtGui.QLineEdit('')
        self.search_lineedit.setPlaceholderText('Search...')
        self.search_lineedit.textChanged.connect(self._search_filter_results)
        self.list_addons_layout.addWidget(self.search_lineedit)
        self.horizontal_slider = QtGui.QSlider()
        self.horizontal_slider.setMinimum(4)
        self.horizontal_slider.setMaximum(18)
        self.horizontal_slider.setValue(8)
        self.horizontal_slider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_slider.valueChanged.connect(self._adjust_list_fontsize)
        self.list_addons_layout.addWidget(self.horizontal_slider)
        self.asset_list_widget = self._list_widget(parent=self.assets)

        # self.texture_widget = contact_sheet.QdContactSheet()
        # self.assets.addWidget(self.texture_widget)
        self.actionbuttons = self._buttons_widget(parent=self.assets)
        self.path_layout = self._path_layout(parent=self.assets)

        # Initial population
        self._populate_projects()
        self._populate_variants()

        # Signal for project changes
        self.projects_combo.currentIndexChanged.connect(self._populate_variants)

    def selected_asset(self, item):
        """
        Triggers when an asset is selected in the asset tree,
        provides information to the info section

        Args:
            item(Asset): pass in an Asset object
        """
        # print item.get_path()
        self.path_line.setText(item.get_path())

    def selected_asset_rightclicked(self, QPos):
        """
        Action used when an asset is rightclicked

        Args:
            QPos(QPosition): location where the right click happened
        """
        item = self.asset_list_widget.itemAt(QPos)
        if item is not None:
            if item.get_actions():
                menu = QtGui.QMenu("Context Menu", self)
                for action in item.get_actions():
                    if action.ACTIONTYPE == ActionType.Menu:
                        _partial = partial(self.rightclick_action_run,
                                           action,
                                           item.get_path())
                        qaction = QtGui.QAction(action.NAME,
                                                self,
                                                triggered=_partial)
                        menu.addAction(qaction)
                menu.exec_(self.asset_list_widget.mapToGlobal(QPos))

    def rightclick_action_run(self, action, path):
        action.execute(path=path)
        # TODO: remove this hack to check for deletion
        time.sleep(2)  # wait till deletion is done
        if not os.path.isfile(path):
            self.asset_list_widget.takeItem(self.asset_list_widget.currentRow())

    def add_buttons(self):
        valid_actions = [a for a in self.ACTIONS if a.ACTIONTYPE == 2]
        for action in valid_actions:
            button = QtGui.QPushButton(action.NAME)
            _partial = partial(self.get_path, action)
            button.clicked.connect(_partial)
            self.actionbuttons.addWidget(button)

    def get_path(self, action):
        asset = action.execute(path=self.asset_list_widget.path)
        name = os.path.basename(asset)
        if os.path.isfile(asset):
            asset_obj = Asset(None, name, asset)
            valid_actions = [a for a in self.ACTIONS if a.FILETYPE == asset_obj.FILETYPE]
            asset_obj.add_actions(valid_actions)

            self._add_item_to_listwidget(asset_obj)
            self.asset_list_widget.scrollToItem(asset_obj)
            # self.asset_list_widget.addItem(asset_obj)

    def get_projects(self, filepath):
        projects = os.listdir(filepath)
        return [p for p in projects if not helpers.FolderHelper().is_hidden(helpers.join_path(filepath, p))]

    def _populate_projects(self):
        for p in self.get_projects(PROJECTS_FOLDER):
            self.projects_combo.addItem(p)

        index = self.projects_combo.findText(DEFAULT_PROJECT, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.projects_combo.setCurrentIndex(index)

    def _populate_variants(self):
        self.folder_tree_widget.clear()

        self.current_locations['project'] = self.projects_combo.currentText()
        self.current_locations['project_folder'] = helpers.join_path(PROJECTS_FOLDER, self.current_locations['project'])
        self.current_locations['project_pub_folder'] = helpers.join_path(self.current_locations['project_folder'], PUBLISH_FOLDER)

        self.folder_directoy = {}
        root_dir = self.current_locations['project_folder'].rstrip(os.sep)
        start = root_dir.rfind(os.sep) + 1

        parent_item = self.folder_tree_widget

        for root, dirnames, filenames in os.walk(root_dir):
            folders = root[start:].split(os.sep)

            try:
                if not folders[-2] == root_dir:
                    parent_item = self.folder_directoy.get(folders[-2])
                else:
                    parent_item = self.folder_tree_widget
            except IndexError:
                parent_item = self.folder_tree_widget

            if not folders[-1] == root_dir:
                self.folder_directoy[folders[-1]] = Location(parent=parent_item,
                                                             name=folders[-1],
                                                             path=root)
            # print self.folder_directoy

    def _populate_assets(self, item):
        item.setExpanded(True)
        self.breadcrumb._hide_all()
        self.breadcrumb.set_breadcrumb_label(item)
        self.asset_list_widget.path = item.get_path()

        self.asset_list_widget.clear()
        self.path_line.setText(item.get_path())

        for ft in self.FILETYPES:
            for asset in helpers.get_files(item.get_path(), pattern='*.%s' % ft):
                name = os.path.basename(asset)
                if os.path.isfile(asset):
                    asset_obj = Asset(None, name, asset)
                    valid_actions = [a for a in self.ACTIONS if a.FILETYPE == asset_obj.FILETYPE]
                    asset_obj.add_actions(valid_actions)

                    self._add_item_to_listwidget(asset_obj)

        images = helpers.get_files(item.get_path(), pattern='*.png')
        images.sort()
        # self.texture_widget.load(images)

    def _tree_widget(self, parent):
        tree_browser_widget = QtGui.QTreeWidget()
        tree_browser_widget.itemClicked.connect(self._populate_assets)
        tree_browser_widget.setHeaderHidden(True)
        parent.addWidget(tree_browser_widget)

        return tree_browser_widget

    def _list_widget(self, parent):
        list_widget = QtGui.QListWidget()
        list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(self.selected_asset_rightclicked)
        list_widget.itemClicked.connect(self.selected_asset)
        list_widget.path = ''
        parent.addWidget(list_widget)

        return list_widget

    def _buttons_widget(self, parent):
        button_widget = QtGui.QWidget()
        button_vlayout = QtGui.QHBoxLayout(button_widget)
        self._clean_layouts(button_vlayout)
        parent.addWidget(button_widget)

        return button_vlayout

    def _variant_layout(self):
        variant_widget = QtGui.QWidget()
        variant_widget.setFixedWidth(200)
        variant_vlayout = QtGui.QVBoxLayout(variant_widget)
        self._clean_layouts(variant_vlayout)

        # create_variant_button = QtGui.QPushButton('Create Variant')

        self.main_layout.addWidget(variant_widget)

        return variant_vlayout

    def _asset_layout(self):
        asset_widget = QtGui.QWidget()
        asset_layout = QtGui.QVBoxLayout(asset_widget)
        self._clean_layouts(asset_layout)

        self.main_layout.addWidget(asset_widget)

        return asset_layout

    def _path_layout(self, parent):
        path_widget = QtGui.QWidget()
        path_layout = QtGui.QHBoxLayout(path_widget)
        self._clean_layouts(path_layout)

        path_layout.addWidget(QtGui.QLabel('Path:'))
        self.path_line = QtGui.QLineEdit('...')
        self.path_line.setReadOnly(True)
        path_layout.addWidget(self.path_line)

        parent.addWidget(path_widget)

        return path_layout

    def _search_filter_results(self, text):
        items = []
        for index in xrange(self.asset_list_widget.count()):
            items.append(self.asset_list_widget.item(index))

        if not items:
            return

        for item in items:
            if text in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def _adjust_list_fontsize(self, value):
        items = []
        for index in xrange(self.asset_list_widget.count()):
            items.append(self.asset_list_widget.item(index))

        if not items:
            return

        family = items[0].font().family()

        font = QtGui.QFont(family, value)
        for item in items:
            item.setFont(font)

    def _add_item_to_listwidget(self, item):
        family = item.font().family()
        value = self.horizontal_slider.value()
        font = QtGui.QFont(family, value)
        item.setFont(font)

        self.asset_list_widget.addItem(item)

    def _clean_layouts(self, layout):
        m = 3
        layout.setContentsMargins(m, m, m, m)
        layout.setAlignment(QtCore.Qt.AlignTop)

    def closeEvent(self, event):
        self.preferences.config.set('ui', 'view_mode', 'list')
        self.preferences.save_config()
