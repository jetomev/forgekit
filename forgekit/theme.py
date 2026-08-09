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

/* scrollbars — furniture, not content: gray family only, slim, accent only
   while dragging (scrollbar props don't inherit, hence the * selector) */
* {
    scrollbar-background: #313244;
    scrollbar-background-hover: #313244;
    scrollbar-background-active: #313244;
    scrollbar-color: #585b70;
    scrollbar-color-hover: #7f849c;
    scrollbar-color-active: #89b4fa;
    scrollbar-size-vertical: 1;
    scrollbar-size-horizontal: 1;
}

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

/* work area — no right padding so section scrollbars hug the screen edge */
#forge-work { padding: 1 0 1 2; height: 1fr; }

/* dropdown submenu */
MenuDropdown { align: left top; background: black 30%; }
.forge-dropdown { background: #313244; color: #cdd6f4; height: auto; border: round #585b70; }
.forge-dropdown > .option-list--option-highlighted { background: #45475a; color: #89b4fa; }

/* modals — panel scales with the terminal; buttons scroll with content.
   ForgeModal covers app-built dialogs so they center like the kit's own. */
ConfirmDialog, ForgePanelScreen, ForgeModal { align: center middle; background: black 45%; }
.forge-confirm { width: 50; height: auto; padding: 1 2; background: #313244; border: round #f9e2af; }
.forge-confirm-msg { padding: 0 0 1 0; }
/* panels hug their content (F-7): short windows end a breath after the
   footer; long bodies cap at ~65% of the terminal height and scroll —
   the body carries the clamp (in vh) so the fixed footer always fits */
.forge-panel { width: 70%; height: auto; max-height: 100%; padding: 1 2; background: #313244; border: round #89b4fa; }
.forge-panel-title { color: #89b4fa; text-style: bold; padding: 0 0 1 0; }
.forge-panel-body { height: auto; max-height: 65vh; }
/* F-8: fixed footer under a divider — buttons never scroll away.
   Kept thin (divider + button row; the panel's bottom padding is the
   air underneath). Definite height so layout reserves its rows. */
.forge-panel-footer { height: 2; padding: 0; border-top: solid #585b70; }

/* form widgets (F-9, promoted from BitlaForge/alacrittyForge app CSS —
   every Forge app edits config, so forms are kit territory) */
Label { color: #a6adc8; padding: 1 0 0 0; }
Input { background: #313244; color: #cdd6f4; border: solid #45475a; }
Input:focus { border: solid #89b4fa; }
Select { background: #313244; color: #cdd6f4; border: solid #45475a; }
Select:focus { border: solid #89b4fa; }
Checkbox { background: #1e1e2e; color: #cdd6f4; }
Switch.-on { color: #89b4fa; }
Switch:focus { border: tall #89b4fa; }
DataTable > .datatable--header { background: #313244; color: #89b4fa; text-style: bold; }
DataTable > .datatable--cursor { background: #45475a; color: #cdd6f4; }
/* compact one-row buttons — Textual's 3-row bordered default is too heavy */
.forge-buttons { height: auto; padding: 1 0 0 0; align-horizontal: right; }
.forge-buttons Button {
    height: 1; min-width: 10; border: none; padding: 0 2; margin: 0 0 0 2;
    background: #45475a; color: #cdd6f4;
}
.forge-buttons Button:hover { background: #585b70; }
.forge-buttons Button:focus { background: #2b4a7a; text-style: bold; }
.forge-buttons Button.-primary { background: #2b4a7a; }
.forge-buttons Button.-primary:hover { background: #89b4fa; color: #11111b; }
.forge-buttons Button.-error { background: #f38ba8; color: #11111b; }
.forge-buttons Button.-error:hover { background: #f9e2af; color: #11111b; }
"""
