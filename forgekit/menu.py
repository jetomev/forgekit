"""Menu bar + dropdown submenu.

Menu model (a plain list of dicts the app owns):

    {"id": "config", "title": "Config", "kind": "menu", "items": [
        ("New entry", "n", "add"), ...]}          # kind: section | menu | action

Main options use their first letter as the accelerator (Ctrl+<letter>); submenu
items carry a per-item letter that selects them (no Ctrl) while the menu is open.
"""

from __future__ import annotations

from rich.text import Text

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option


def accel(entry: dict) -> str:
    """The main-option accelerator letter (defaults to the title's first)."""
    return entry.get("acc", entry["title"][0]).lower()


def underline_label(label: str, acc_letter: str) -> Text:
    """Render ``label`` with ``acc_letter`` underlined (first match)."""
    t = Text(" ")
    i = label.lower().find(acc_letter.lower())
    if i < 0:
        t.append(label)
    else:
        t.append(label[:i])
        t.append(label[i], style="underline")
        t.append(label[i + 1:])
    return t


class MenuBar(Horizontal):
    """The top menu bar. Renders one clickable title per entry with its
    accelerator letter underlined. Titles get id ``menu-<entry id>``."""

    def __init__(self, menu: list[dict], **kwargs) -> None:
        super().__init__(id="forge-menubar", **kwargs)
        self._menu = menu

    def compose(self) -> ComposeResult:
        for m in self._menu:
            title, a = m["title"], accel(m)
            i = title.lower().find(a)
            markup = f"{title[:i]}[u]{title[i]}[/u]{title[i+1:]}" if i >= 0 else title
            yield Static(f" {markup} ", id=f"menu-{m['id']}", classes="menu-title")


class MenuDropdown(ModalScreen[str | None]):
    """Transient dropdown anchored under a menu title. Returns the chosen
    action id, or None on escape / click-away. ``items`` is a list of
    (label, accel_letter, action_id)."""

    BINDINGS = [Binding("escape", "dismiss_none", "", show=False)]

    def __init__(self, items: list[tuple[str, str, str]], x: int, y: int) -> None:
        super().__init__()
        self._items = items
        self._x, self._y = x, y
        self._accels = {a.lower(): act for _l, a, act in items}

    def compose(self) -> ComposeResult:
        # +6 = leading space + option padding + round border → longest name
        # always fits on one line (no wrapping).
        width = max((len(l) for l, _a, _ in self._items), default=8) + 6
        ol = OptionList(
            *(Option(underline_label(l, a), id=act) for l, a, act in self._items),
            classes="forge-dropdown",
        )
        ol.styles.width = width
        yield ol

    def on_mount(self) -> None:
        ol = self.query_one(OptionList)
        ol.styles.offset = (self._x, self._y)
        ol.focus()

    def on_key(self, event) -> None:
        ch = (event.character or "").lower()
        if ch in self._accels:
            event.stop()
            self.dismiss(self._accels[ch])

    def on_option_list_option_selected(self, e: OptionList.OptionSelected) -> None:
        self.dismiss(e.option.id)

    def action_dismiss_none(self) -> None:
        self.dismiss(None)

    def on_click(self, event) -> None:
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self:
            self.dismiss(None)
