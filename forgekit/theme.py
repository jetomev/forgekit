"""Catppuccin-Mocha palette + the base forgekit stylesheet.

Apps set ``CSS = FORGE_CSS`` (and may append their own rules). The palette dict
is exported for convenience when apps want the exact accent colors in markup.
"""

from __future__ import annotations

# Catppuccin Mocha — https://catppuccin.com
COLORS = {
    "base": "#1e1e2e", "mantle": "#181825", "crust": "#11111b",
    "surface0": "#313244", "surface1": "#45475a", "surface2": "#585b70",
    "overlay0": "#7f849c", "subtext": "#a6adc8", "text": "#cdd6f4",
    "blue": "#89b4fa", "sapphire": "#74c7ec", "mauve": "#cba6f7",
    "green": "#a6e3a1", "yellow": "#f9e2af", "red": "#f38ba8",
    "boxblue": "#2b4a7a",
}

# The shell + dialog styling. Widget-scoped so apps only add their own section
# rules on top.
FORGE_CSS = """
Screen { background: #1e1e2e; color: #cdd6f4; }

/* header: title bar (row 0) + menu bar (row 1) */
#forge-header { dock: top; height: 2; }
#forge-title {
    height: 1; background: #11111b; color: #cba6f7;
    text-style: bold; text-align: center; content-align: center middle;
}
#forge-menubar { height: 1; background: #181825; }
.menu-title { width: auto; height: 1; color: #cdd6f4; }
.menu-title:hover { background: #313244; color: #89b4fa; }
.menu-title.active { background: #2b4a7a; color: #cdd6f4; text-style: bold; }

/* work area */
#forge-work { padding: 1 2; height: 1fr; }

/* dropdown submenu */
MenuDropdown { align: left top; background: black 30%; }
.forge-dropdown { background: #313244; color: #cdd6f4; height: auto; border: round #585b70; }
.forge-dropdown > .option-list--option-highlighted { background: #45475a; color: #89b4fa; }

/* modals — panel scales with the terminal; buttons scroll with content */
ConfirmDialog, ForgePanelScreen { align: center middle; background: black 45%; }
.forge-confirm { width: 50; height: auto; padding: 1 2; background: #313244; border: round #f9e2af; }
.forge-confirm-msg { padding: 0 0 1 0; }
.forge-panel { width: 70%; height: 80%; padding: 1 2; background: #313244; border: round #89b4fa; }
.forge-panel-title { color: #89b4fa; text-style: bold; padding: 0 0 1 0; }
.forge-panel-body { height: 1fr; }

Label { color: #a6adc8; padding: 1 0 0 0; }
Switch.-on { color: #89b4fa; }
Switch:focus { border: tall #89b4fa; }
.forge-buttons { height: auto; padding: 1 0 0 0; align-horizontal: right; }
.forge-buttons Button { margin: 0 0 0 2; }
"""
