"""``ForgeApp`` — the base application shell.

A Forge app subclasses this and supplies:

    APP_NAME, MENU, SHORTCUTS, ABOUT, LICENSE_NAME, LICENSE_NOTICE   (class attrs)
    CSS = FORGE_CSS + "…your section styles…"
    def compose_sections(self):     # yield section widgets, ids "sec-<id>"
    def on_action(self, action_id): # handle your submenu actions (add/edit/…)
    # optional: on_section_shown(id), plus BINDINGS for section accelerators

The base provides: the title + menu bar, the content switcher, dropdown
dispatch, section switching + active highlight, and the Help windows
(Shortcuts / License / About). Menu-bar order convention: main options, then
Help (id ``help``), then Quit (id ``quit``).
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import ContentSwitcher, Static

from .dialogs import AboutDialog, LicenseDialog, ShortcutsDialog
from .menu import MenuBar, MenuDropdown
from .theme import FORGE_CSS


class ForgeApp(App[None]):
    # ── to be overridden by the app ──────────────────────────────────────────
    APP_NAME: str = "ForgeApp"
    MENU: list[dict] = []
    SHORTCUTS: list[tuple[str, str]] = []
    ABOUT: dict = {}
    LICENSE_NAME: str = "GPL-3.0-or-later"
    LICENSE_NOTICE: str = ""

    CSS = FORGE_CSS

    # Universal accelerators (apps add their own section bindings). Help lives
    # on Ctrl+H, Quit on Ctrl+Q by convention.
    BINDINGS = [
        Binding("ctrl+h", "activate('help')", show=False, priority=True),
        Binding("ctrl+q", "activate('quit')", show=False, priority=True),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = self.APP_NAME
        self._by_id = {m["id"]: m for m in self.MENU}

    # ── shell composition ────────────────────────────────────────────────────
    def compose(self) -> ComposeResult:
        with Vertical(id="forge-header"):
            yield Static(self.APP_NAME, id="forge-title")
            yield MenuBar(self.MENU)
        with ContentSwitcher(initial=f"sec-{self._first_section()}", id="forge-work"):
            yield from self.compose_sections()

    def compose_sections(self) -> ComposeResult:
        yield from ()

    def on_mount(self) -> None:
        self._mark_active(self._first_section())

    def _first_section(self) -> str:
        for m in self.MENU:
            if m["kind"] == "section":
                return m["id"]
        return ""

    # ── menu dispatch ────────────────────────────────────────────────────────
    def on_click(self, event) -> None:
        w = event.widget
        if w is not None and w.id and w.id.startswith("menu-"):
            self.action_activate(w.id.removeprefix("menu-"))

    def action_activate(self, entry_id: str) -> None:
        entry = self._by_id[entry_id]
        kind = entry["kind"]
        if kind == "section":
            self._switch_section(entry_id)
        elif kind == "action":
            self.action_act(entry["action"])
        elif kind == "menu":
            w = self.query_one(f"#menu-{entry_id}")
            self.push_screen(MenuDropdown(entry["items"], w.region.x, w.region.y + 1),
                             self._on_menu_choice)

    def _switch_section(self, section_id: str) -> None:
        self.query_one("#forge-work", ContentSwitcher).current = f"sec-{section_id}"
        self._mark_active(section_id)
        self.on_section_shown(section_id)

    def on_section_shown(self, section_id: str) -> None:
        """Hook: called after a section becomes visible."""

    def _mark_active(self, section_id: str) -> None:
        for m in self.MENU:
            self.query_one(f"#menu-{m['id']}").set_class(m["id"] == section_id, "active")

    def _on_menu_choice(self, action_id: str | None) -> None:
        if action_id:
            self.action_act(action_id)

    def action_act(self, action_id: str) -> None:
        if action_id == "quit":
            self.exit()
        elif action_id == "shortcuts":
            self.push_screen(ShortcutsDialog(self.SHORTCUTS))
        elif action_id == "license":
            self.push_screen(LicenseDialog(self.LICENSE_NAME, self.LICENSE_NOTICE))
        elif action_id == "about":
            self.push_screen(AboutDialog(self.ABOUT))
        else:
            self.on_action(action_id)

    def on_action(self, action_id: str) -> None:
        """Hook: handle the app's own submenu action ids."""
