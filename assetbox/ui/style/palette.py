from PySide import QtGui


def load_theme(widget):
    app = widget
    app.setPalette(palette(app))


def palette(app):
    palette = QtGui.QPalette(app.palette())

    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(100, 100, 100))
    palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(200, 200, 200))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(34, 34, 34))
    palette.setColor(QtGui.QPalette.Background, QtGui.QColor(29, 31, 29))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(80, 80, 81))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(171, 176, 182))
    palette.setColor(QtGui.QPalette.Foreground, QtGui.QColor(20, 20, 21))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(171, 176, 182))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(114, 114, 114))
    palette.setColor(QtGui.QPalette.Light, QtGui.QColor(74, 74, 74))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(154, 174, 182))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(29, 29, 29))
    palette.setColor(QtGui.QPalette.LinkVisited, QtGui.QColor(165, 76, 21))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(20, 20, 20))
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(40, 40, 41))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(154, 154, 162))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(114, 110, 102))

    return palette
