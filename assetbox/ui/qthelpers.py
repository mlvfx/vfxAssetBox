"""
Helpers related to the Qt interface.
"""
from PySide import QtCore


def clean_layouts(layout, margin=3):
    """
    Pass in a layout and tidy the margins for the interface.

    Args:
        layout: QLayout object.
    """
    # Margin size.
    layout.setContentsMargins(margin, margin, margin, margin)
    layout.setAlignment(QtCore.Qt.AlignTop)
