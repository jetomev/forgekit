"""Reusable floating dialogs.

* ``ConfirmDialog`` — small yes/no, stacks over anything, returns bool.
* ``ForgePanelScreen`` — the standard scrolling panel (title + body + a Close
  button that scrolls with the content). Base for read-only info windows.
* ``ShortcutsDialog`` / ``LicenseDialog`` / ``AboutDialog`` — Help windows.

Apps build their own editors on ``.forge-panel`` styling + ``ConfirmDialog``
(see ``examples/demo.py``'s ``EditDialog``).
"""

from __future__ import annotations

from typing import TypeVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Static


ResultType = TypeVar("ResultType")


class ForgeModal(ModalScreen[ResultType]):
    """Base for app-built floating dialogs (editors, pickers, wizards).

    Carries the standard Forge modal treatment — centered on screen with the
    dimmed backdrop — so app dialogs match the kit's own windows. Subclass it
    (optionally parameterized: ``ForgeModal[dict | None]``) and compose a
    ``.forge-panel`` Vertical inside, as in ``examples/demo.py``.
    """


class ConfirmDialog(ModalScreen[bool]):
    BINDINGS = [
        Binding("escape", "no", "", show=False),
        Binding("y", "yes", "", show=False),
        Binding("n", "no", "", show=False),
    ]

    def __init__(self, message: str, confirm_label: str = "Confirm",
                 danger: bool = False) -> None:
        super().__init__()
        self._message, self._confirm_label, self._danger = message, confirm_label, danger

    def compose(self) -> ComposeResult:
        with Vertical(classes="forge-confirm"):
            yield Static(self._message, classes="forge-confirm-msg")
            with Horizontal(classes="forge-buttons"):
                yield Button(self._confirm_label, id="ok",
                             variant="error" if self._danger else "primary")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, e: Button.Pressed) -> None:
        self.dismiss(e.button.id == "ok")

    def action_yes(self) -> None: self.dismiss(True)
    def action_no(self) -> None: self.dismiss(False)


class ForgePanelScreen(ModalScreen[None]):
    """A read-only scrolling panel with a trailing Close button."""

    BINDINGS = [Binding("escape", "close", "", show=False)]
    panel_title = "forgekit"

    def compose(self) -> ComposeResult:
        with Vertical(classes="forge-panel"):
            yield Static(self.panel_title, classes="forge-panel-title")
            with VerticalScroll(classes="forge-panel-body"):
                yield from self.compose_body()
                with Horizontal(classes="forge-buttons"):
                    yield Button("Close", id="forge-close", variant="primary")

    def compose_body(self) -> ComposeResult:
        yield from ()

    def on_button_pressed(self, e: Button.Pressed) -> None:
        self.dismiss()

    def action_close(self) -> None:
        self.dismiss()


class ShortcutsDialog(ForgePanelScreen):
    panel_title = "Keyboard shortcuts"

    def __init__(self, shortcuts: list[tuple[str, str]]) -> None:
        super().__init__()
        self._shortcuts = shortcuts

    def compose_body(self) -> ComposeResult:
        for key, desc in self._shortcuts:
            yield Static(f"[#89b4fa b]{key:<8}[/]  {desc}")


class LicenseDialog(ForgePanelScreen):
    def __init__(self, license_name: str, notice: str) -> None:
        super().__init__()
        self.panel_title = f"License — {license_name}"
        self._notice = notice

    def compose_body(self) -> ComposeResult:
        yield Static(self._notice)


class AboutDialog(ForgePanelScreen):
    def __init__(self, about: dict) -> None:
        super().__init__()
        self.panel_title = f"About {about['name']}"
        self._a = about

    def compose_body(self) -> ComposeResult:
        a = self._a
        yield Static(f"[b #cba6f7]{a['name']}[/]   [#a6adc8]v{a['version']}[/]")
        if a.get("tagline"):
            yield Static(f"[i #a6adc8]{a['tagline']}[/]")
        if a.get("description"):
            yield Static(f"\n{a['description']}\n")
        if a.get("authors"):
            yield Static(f"[#89b4fa b]Authors[/]   {a['authors']}")
        if a.get("license"):
            yield Static(f"[#89b4fa b]License[/]   {a['license']}")
        if a.get("links"):
            yield Static("\n[#89b4fa b]Links[/]")
            for label, url in a["links"]:
                yield Static(f"  {label}:  [u #89b4fa]{url}[/]")
