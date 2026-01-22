# libs/toolBar.py
"""Custom toolbar and button classes for labelImg++."""

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


# Icon size for toolbar buttons (Feather icons are 24x24)
ICON_SIZE = 22


class ToolBar(QToolBar):
    """Custom toolbar with modern styling support."""

    def __init__(self, title):
        super(ToolBar, self).__init__(title)
        layout = self.layout()
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setContentsMargins(0, 0, 0, 0)
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def addAction(self, action):
        if isinstance(action, QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = ToolButton()
        btn.setDefaultAction(action)
        btn.setToolButtonStyle(self.toolButtonStyle())
        self.addWidget(btn)
        return btn


class ToolButton(QToolButton):
    """Custom toolbar button - allows natural sizing for text."""

    def __init__(self):
        super(ToolButton, self).__init__()
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def sizeHint(self):
        hint = super(ToolButton, self).sizeHint()
        width = max(hint.width(), 70)
        height = max(hint.height(), 40)
        return QSize(width, height)

    def minimumSizeHint(self):
        return QSize(65, 38)


class DropdownToolButton(QToolButton):
    """Toolbar button with dropdown menu for grouping related actions."""

    def __init__(self, text, icon=None, actions=None):
        super(DropdownToolButton, self).__init__()
        self.setText(text)
        if icon:
            self.setIcon(icon)
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setPopupMode(QToolButton.InstantPopup)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Create menu for dropdown actions
        self.dropdown_menu = QMenu(self)
        if actions:
            for action in actions:
                if action is None:
                    self.dropdown_menu.addSeparator()
                else:
                    self.dropdown_menu.addAction(action)
        self.setMenu(self.dropdown_menu)

    def add_action(self, action):
        """Add an action to the dropdown menu."""
        if action is None:
            self.dropdown_menu.addSeparator()
        else:
            self.dropdown_menu.addAction(action)

    def sizeHint(self):
        hint = super(DropdownToolButton, self).sizeHint()
        width = max(hint.width(), 70)
        height = max(hint.height(), 40)
        return QSize(width, height)

    def minimumSizeHint(self):
        return QSize(65, 38)
