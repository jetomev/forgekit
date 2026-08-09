"""forgekit — a shared Textual TUI shell for the Forge Suite.

Top menu bar, full-width workspace, and floating dialogs, Catppuccin-themed.
Build an app by subclassing ``ForgeApp``; see ``examples/demo.py``.
"""

from .app import ForgeApp
from .dialogs import (
    AboutDialog, ConfirmDialog, ForgeModal, ForgePanelScreen, LicenseDialog,
    ShortcutsDialog,
)
from .licenses import GPL3_NOTICE
from .menu import MenuBar, MenuDropdown, accel, underline_label
from .theme import COLORS, FORGE_CSS

__version__ = "0.2.0"

__all__ = [
    "ForgeApp",
    "MenuBar", "MenuDropdown", "accel", "underline_label",
    "ConfirmDialog", "ForgeModal", "ForgePanelScreen", "ShortcutsDialog", "LicenseDialog", "AboutDialog",
    "FORGE_CSS", "COLORS", "GPL3_NOTICE",
    "__version__",
]
