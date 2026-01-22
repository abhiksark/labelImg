# libs/toolBar.py
"""Custom toolbar and button classes for labelImg++."""

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


# Base icon size for toolbar buttons (Feather icons are 24x24)
BASE_ICON_SIZE = 22
# Minimum and maximum icon sizes for scaling
MIN_ICON_SIZE = 16
MAX_ICON_SIZE = 48


def get_dpi_scale_factor():
    """Get the DPI scale factor for the primary screen.

    Returns:
        float: Scale factor (1.0 for standard 96 DPI, higher for HiDPI displays)
    """
    app = QApplication.instance()
    if app is None:
        return 1.0

    # Try to get the primary screen
    try:
        screen = app.primaryScreen()
        if screen:
            # Get logical DPI (accounts for user scaling settings)
            logical_dpi = screen.logicalDotsPerInch()
            # Standard DPI is 96 on most systems
            return logical_dpi / 96.0
    except AttributeError:
        # Qt4 fallback
        pass

    return 1.0


def calculate_icon_size(base_size=BASE_ICON_SIZE):
    """Calculate appropriate icon size based on DPI.

    Args:
        base_size: Base icon size at standard DPI

    Returns:
        int: Scaled icon size clamped to min/max bounds
    """
    scale = get_dpi_scale_factor()
    scaled_size = int(base_size * scale)
    return max(MIN_ICON_SIZE, min(MAX_ICON_SIZE, scaled_size))


class ToolBar(QToolBar):
    """Custom toolbar with modern styling and DPI-aware icons."""

    def __init__(self, title):
        super(ToolBar, self).__init__(title)
        layout = self.layout()
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setContentsMargins(0, 0, 0, 0)
        self._icon_size = calculate_icon_size()
        self.setIconSize(QSize(self._icon_size, self._icon_size))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # Track tool buttons for icon size updates
        self._tool_buttons = []

    def addAction(self, action):
        if isinstance(action, QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = ToolButton(self._icon_size)
        btn.setDefaultAction(action)
        btn.setToolButtonStyle(self.toolButtonStyle())
        self.addWidget(btn)
        self._tool_buttons.append(btn)
        return btn

    def addWidget(self, widget):
        """Override to track widgets that support icon sizing."""
        super(ToolBar, self).addWidget(widget)
        if isinstance(widget, (ToolButton, DropdownToolButton)):
            if widget not in self._tool_buttons:
                self._tool_buttons.append(widget)

    def update_icon_size(self, size=None):
        """Update icon size for toolbar and all buttons.

        Args:
            size: New icon size, or None to recalculate from DPI
        """
        if size is None:
            size = calculate_icon_size()

        self._icon_size = size
        self.setIconSize(QSize(size, size))

        # Update all tracked buttons
        for btn in self._tool_buttons:
            if hasattr(btn, 'update_icon_size'):
                btn.update_icon_size(size)
            else:
                btn.setIconSize(QSize(size, size))

    def showEvent(self, event):
        """Recalculate icon size when toolbar becomes visible."""
        super(ToolBar, self).showEvent(event)
        # Recalculate in case screen/DPI changed
        new_size = calculate_icon_size()
        if new_size != self._icon_size:
            self.update_icon_size(new_size)


class ToolButton(QToolButton):
    """Custom toolbar button with DPI-aware sizing."""

    def __init__(self, icon_size=None):
        super(ToolButton, self).__init__()
        self._icon_size = icon_size or calculate_icon_size()
        self.setIconSize(QSize(self._icon_size, self._icon_size))
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def update_icon_size(self, size):
        """Update the icon size."""
        self._icon_size = size
        self.setIconSize(QSize(size, size))
        self.updateGeometry()

    def sizeHint(self):
        hint = super(ToolButton, self).sizeHint()
        # Width based on text (don't shrink below 70), height scales with icon
        scale = self._icon_size / BASE_ICON_SIZE
        width = max(hint.width(), 70)
        height = max(hint.height(), int(40 * max(1.0, scale)))
        return QSize(width, height)

    def minimumSizeHint(self):
        # Minimum width for text, height scales with icon
        scale = self._icon_size / BASE_ICON_SIZE
        return QSize(65, int(38 * max(1.0, scale)))


class DropdownToolButton(QToolButton):
    """Toolbar button with dropdown menu and DPI-aware sizing."""

    def __init__(self, text, icon=None, actions=None, icon_size=None):
        super(DropdownToolButton, self).__init__()
        self._icon_size = icon_size or calculate_icon_size()
        self.setText(text)
        if icon:
            self.setIcon(icon)
        self.setIconSize(QSize(self._icon_size, self._icon_size))
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

    def update_icon_size(self, size):
        """Update the icon size."""
        self._icon_size = size
        self.setIconSize(QSize(size, size))
        self.updateGeometry()

    def sizeHint(self):
        hint = super(DropdownToolButton, self).sizeHint()
        # Width based on text (don't shrink below 70), height scales with icon
        scale = self._icon_size / BASE_ICON_SIZE
        width = max(hint.width(), 70)
        height = max(hint.height(), int(40 * max(1.0, scale)))
        return QSize(width, height)

    def minimumSizeHint(self):
        # Minimum width for text, height scales with icon
        scale = self._icon_size / BASE_ICON_SIZE
        return QSize(65, int(38 * max(1.0, scale)))
