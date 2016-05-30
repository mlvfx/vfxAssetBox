"""
Launches the main interface for assetbox.
"""
from assetbox.base import host_manager
import assetbox.ui.main_window
reload(assetbox.ui.main_window)

import logging

LOGGER = logging.getLogger(__name__)


def launch(*args):
    """
    Open the interface.
    """
    global vfx_assetbox

    hm = host_manager.HostManager()
    host = hm.get_hostapp()
    actions = hm.get_actions()
    filetypes = hm.get_filetypes()

    try:
        vfx_assetbox.close()
    except:
        pass

    if not host:
        LOGGER.warning('No HOST found.')
        print 'No HOST found.'
        return

    host.start_QApp()
    vfx_assetbox = assetbox.ui.main_window.AssetBoxWindow()
    vfx_assetbox.host = host
    vfx_assetbox.actions = actions
    vfx_assetbox.filetypes = filetypes
    vfx_assetbox.add_buttons()
    vfx_assetbox.show()

    # app = QtGui.QApplication.instance()
    # app.setStyle("Plastique")


if __name__ == '__main__':
    launch()

if __name__ == '__builtin__':
    launch()
