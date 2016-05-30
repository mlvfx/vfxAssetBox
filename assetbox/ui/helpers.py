"""
Helpers related to the interface.
"""
import QtCore


def clean_layouts(layout):
    """
    Pass in a layout and tidy the margins for the interface.

    Args:
        layout: QLayout object.
    """
    # Margin size.
    m = 3
    layout.setContentsMargins(m, m, m, m)
    layout.setAlignment(QtCore.Qt.AlignTop)
