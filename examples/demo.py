"""examples/demo.py — a BitlaForge-shaped app built on forgekit.

Run:  python examples/demo.py   (from the repo root, or after `pip install -e .`)

Shows the whole pattern: subclass ``ForgeApp``, declare the MENU / SHORTCUTS /
ABOUT, yield section widgets, add section-accelerator bindings, and handle the
app's own submenu actions in ``on_action``. The edit dialog is app-specific and
built on forgekit's ``.forge-panel`` styling + ``ConfirmDialog``.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Input, Label, Select, Static, Switch
from textual import work

from forgekit import ForgeApp, ForgeModal, ConfirmDialog, FORGE_CSS, GPL3_NOTICE


MENU = [
    {"id": "dashboard", "title": "Dashboard", "kind": "section"},
    {"id": "log",       "title": "Log",       "kind": "section"},
    {"id": "config",    "title": "Config",    "kind": "menu", "items": [
        ("New entry",       "n", "add"),
        ("Edit selected",   "e", "edit"),
        ("Delete selected", "d", "delete"),
    ]},
    {"id": "setup",     "title": "Setup",     "kind": "section"},
    {"id": "help",      "title": "Help",      "kind": "menu", "items": [
        ("Shortcuts",       "s", "shortcuts"),
        ("License",         "l", "license"),
        ("About",           "a", "about"),
    ]},
    {"id": "quit",      "title": "Quit",      "kind": "action", "action": "quit"},
]

SHORTCUTS = [
    ("Ctrl+D", "Dashboard"), ("Ctrl+L", "Log"), ("Ctrl+C", "Config"),
    ("Ctrl+S", "Setup"), ("Ctrl+H", "Help"), ("Ctrl+Q", "Quit"),
    ("Ctrl+N", "New entry"), ("Enter", "Edit selected"), ("Del", "Delete selected"),
]

ABOUT = {
    "name": "BitlaForge",
    "version": "0.1.3",
    "tagline": "Solo Bitcoin mining, the lottery way — a Textual TUI over minerd.",
    "description": (
        "BitlaForge is a Catppuccin-Mocha terminal UI for solo mining to a pool "
        "like ckpool: configure wallet, pool and threads, launch the miner, and "
        "watch the log. Part of the Forge Suite for KognogOS."
    ),
    "authors": "Javier (jetomev) + Claude (Anthropic)",
    "license": "GPL-3.0-or-later",
    "links": [
        ("GitHub", "https://github.com/jetomev/bitlaforge"),
        ("AUR",    "https://aur.archlinux.org/packages/bitlaforge"),
    ],
}

DEMO_CSS = """
.section-h { color: #89b4fa; text-style: bold; padding: 0 0 1 0; }
.stat { color: #cdd6f4; }
.muted { color: #a6adc8; }
DataTable { height: auto; max-height: 1fr; }
DataTable > .datatable--cursor { background: #45475a; }
DataTable > .datatable--header { background: #313244; color: #89b4fa; text-style: bold; }
.switch-row { height: auto; padding: 1 0 0 0; }
.switch-label { padding: 1 0 0 1; }
"""


class EditDialog(ForgeModal[dict | None]):
    """App-specific editor, built on forgekit's ForgeModal + `.forge-panel` styling."""

    BINDINGS = [Binding("escape", "cancel", "", show=False)]
    TYPES = [("Text", "text"), ("Number", "number"),
             ("Boolean", "boolean"), ("Choice", "choice")]

    def __init__(self, title: str, entry: dict | None = None) -> None:
        super().__init__()
        self._title = title
        self._entry = entry or {"name": "", "value": "", "type": "text", "enabled": True}

    def compose(self) -> ComposeResult:
        e = self._entry
        with Vertical(classes="forge-panel"):
            yield Static(self._title, classes="forge-panel-title")
            with VerticalScroll(classes="forge-panel-body"):
                yield Label("Name")
                yield Input(value=e["name"], placeholder="entry name", id="f-name")
                yield Label("Value")
                yield Input(value=str(e["value"]), placeholder="value", id="f-value")
                yield Label("Type")
                yield Select(self.TYPES, value=e["type"], allow_blank=False, id="f-type")
                with Horizontal(classes="switch-row"):
                    yield Switch(value=bool(e["enabled"]), id="f-enabled")
                    yield Label("Enabled", classes="switch-label")
                with Horizontal(classes="forge-buttons"):
                    yield Button("Save", id="save", variant="primary")
                    yield Button("Cancel", id="cancel")

    def _values(self) -> dict:
        return {
            "name": self.query_one("#f-name", Input).value.strip(),
            "value": self.query_one("#f-value", Input).value.strip(),
            "type": self.query_one("#f-type", Select).value,
            "enabled": self.query_one("#f-enabled", Switch).value,
        }

    def on_button_pressed(self, e: Button.Pressed) -> None:
        if e.button.id == "cancel":
            self.dismiss(None)
        elif e.button.id == "save":
            self._confirm_and_save()

    def action_cancel(self) -> None:
        self.dismiss(None)

    @work
    async def _confirm_and_save(self) -> None:
        vals = self._values()
        if not vals["name"]:
            self.notify("Name is required.", severity="warning")
            return
        if await self.app.push_screen_wait(
            ConfirmDialog(f"Save changes to “{vals['name']}”?", "Save")
        ):
            self.dismiss(vals)


class BitlaForgeDemo(ForgeApp):
    APP_NAME = "BitlaForge"
    MENU = MENU
    SHORTCUTS = SHORTCUTS
    ABOUT = ABOUT
    LICENSE_NAME = "GPL-3.0-or-later"
    LICENSE_NOTICE = GPL3_NOTICE
    CSS = FORGE_CSS + DEMO_CSS

    BINDINGS = [
        Binding("ctrl+d", "activate('dashboard')", show=False, priority=True),
        Binding("ctrl+l", "activate('log')", show=False, priority=True),
        Binding("ctrl+c", "activate('config')", show=False, priority=True),
        Binding("ctrl+s", "activate('setup')", show=False, priority=True),
        Binding("ctrl+n", "act('add')", show=False, priority=True),
        Binding("delete", "act('delete')", show=False, priority=True),
    ]

    ROWS = [
        {"name": "pool_url",  "value": "stratum+tcp://solo.ckpool.org:3333", "type": "text", "enabled": True},
        {"name": "wallet",    "value": "bc1q…tphome01", "type": "text", "enabled": True},
        {"name": "threads",   "value": "4", "type": "number", "enabled": True},
        {"name": "algo",      "value": "sha256d", "type": "choice", "enabled": True},
        {"name": "autostart", "value": "false", "type": "boolean", "enabled": False},
    ]

    def compose_sections(self) -> ComposeResult:
        with Vertical(id="sec-dashboard"):
            yield Static("⛏  Mining Dashboard", classes="section-h")
            yield Static("Hashrate      12.4 kH/s", classes="stat")
            yield Static("Accepted      37", classes="stat")
            yield Static("Rejected      0", classes="stat")
            yield Static("Uptime        3d 4h 12m", classes="stat")
            yield Static("\nSolo lottery — no shares, full block or nothing.", classes="muted")
        with VerticalScroll(id="sec-log"):
            yield Static("\n".join(
                f"[dim]2026-07-18 {21 + i // 60 % 3:02d}:{i % 60:02d}:11[/dim]  accepted 0/0 diff 1 (n={i})"
                for i in range(200)), classes="stat")
        yield DataTable(id="sec-config", cursor_type="row")
        with Vertical(id="sec-setup"):
            yield Static("🛠  Setup", classes="section-h")
            yield Static("First-run wizard would live here.", classes="muted")

    def on_mount(self) -> None:
        super().on_mount()
        t = self.query_one("#sec-config", DataTable)
        t.zebra_stripes = True
        t.add_columns("Name", "Value", "Type", "Enabled")
        self._reload_table()

    def _reload_table(self) -> None:
        t = self.query_one("#sec-config", DataTable)
        t.clear()
        for r in self.ROWS:
            t.add_row(r["name"], r["value"], r["type"], "✓" if r["enabled"] else "—")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.on_action("edit")

    def on_action(self, action_id: str) -> None:
        if action_id not in ("add", "edit", "delete"):
            return
        self._switch_section("config")
        table = self.query_one("#sec-config", DataTable)
        if action_id == "add":
            self._edit_flow(None)
        elif action_id == "edit":
            self._edit_flow(table.cursor_row)
        else:
            self._delete_flow(table.cursor_row)

    @work
    async def _edit_flow(self, index: int | None) -> None:
        if index is None:
            title, entry = "New entry", None
        else:
            title, entry = f"Edit — {self.ROWS[index]['name']}", dict(self.ROWS[index])
        result = await self.push_screen_wait(EditDialog(title, entry))
        if result is None:
            return
        if index is None:
            self.ROWS.append(result)
        else:
            self.ROWS[index] = result
        self._reload_table()
        self.notify(f"Saved “{result['name']}”.", title=self.APP_NAME)

    @work
    async def _delete_flow(self, index: int | None) -> None:
        if index is None or not self.ROWS:
            return
        name = self.ROWS[index]["name"]
        if await self.push_screen_wait(
            ConfirmDialog(f"Delete “{name}” permanently?", "Delete", danger=True)
        ):
            del self.ROWS[index]
            self._reload_table()
            self.notify(f"Deleted “{name}”.", severity="warning", title=self.APP_NAME)


if __name__ == "__main__":
    BitlaForgeDemo().run()
