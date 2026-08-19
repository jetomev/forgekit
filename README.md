# 🔨 forgekit

![Version: 0.3.0](https://img.shields.io/badge/Version-0.3.0-purple.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Built with Textual](https://img.shields.io/badge/Built%20with-Textual-5a3fd6.svg)
![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Theme: Catppuccin Mocha](https://img.shields.io/badge/Theme-Catppuccin%20Mocha-f5c2e7.svg)

> 🛡 **Security** — every release is GPG-signed and every commit is GitHub-Verified. **[Where We Stand](https://github.com/jetomev/KognogOS/blob/main/docs/where-we-stand.md)** covers our response to the 2026 AUR supply-chain attacks and how to check us yourself.

**A shared foundation for building terminal apps that look and behave the same.**

Every app in the [Forge Suite](#the-forge-suite) runs in a terminal, but they're
real applications — menus you click or type through, dialogs that float over your
work, keyboard shortcuts, a consistent look. forgekit is the part they all share.

Without it, every app would rebuild its own menu bar and its own dialogs, and they'd
drift apart. With it, you write only what makes your app different, and a fix or a
polish improves every app at once.

```
┌───────────────────────────── bitlaForge ─────────────────────────────┐   title bar
│ Dashboard  Log  Config  Setup  Help  Quit                            │   menu bar
│                                                                       │
│   … the active section owns the whole width …                        │   workspace
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**What you get:**

- **A menu bar** across the top. Each option's first letter is underlined and works
  as `Ctrl+<letter>`. Options always end with `Help` and `Quit`, in that order.
- **A workspace** showing one full-width section at a time. No permanent sidebar
  eating your screen — you switch sections from the menu.
- **Floating dialogs** that sit over your work rather than splitting the screen.
  They can stack: a confirmation can open on top of an editor. They resize with
  the terminal.
- **Help windows** — `Shortcuts`, `License` and `About` are built in and work
  from the start.
- **Toasts** for quick messages that don't need a dialog.

> **Status: 0.3.0 (alpha).** The API may still shift while the Forge apps migrate
> onto it. Pin a version if you depend on it.

## Screenshots

*Generated from `examples/demo.py`. Run `PYTHONPATH=. python docs/screenshots/generate.py` to re-render them.*

**The shell** — title bar, menu bar, and a section
![Shell](docs/screenshots/01-shell.svg)

**A floating edit dialog**
![Edit dialog](docs/screenshots/02-edit-dialog.svg)

**A menu dropdown**
![Menu](docs/screenshots/03-menu-open.svg)

**The About window**
![About](docs/screenshots/04-about-window.svg)

## Install

On Arch, from the AUR. This is the packaged path the Forge apps depend on, and it
verifies our release signature while building:

```bash
yay -S python-forgekit
```

Anywhere else:

```bash
pip install git+https://github.com/jetomev/forgekit
```

For development:

```bash
git clone https://github.com/jetomev/forgekit && cd forgekit
pip install -e .
python examples/demo.py
```

Requires Python 3.10 or newer, and `textual>=8.0`.

## Quickstart

A complete app. Subclass one class, declare your menu, and write your sections.

```python
from textual.binding import Binding
from forgekit import ForgeApp, FORGE_CSS, GPL3_NOTICE
from textual.widgets import Static
from textual.containers import Vertical

class MyApp(ForgeApp):
    APP_NAME = "MyForge"
    CSS = FORGE_CSS
    MENU = [
        {"id": "home", "title": "Home", "kind": "section"},
        {"id": "help", "title": "Help", "kind": "menu", "items": [
            ("Shortcuts", "s", "shortcuts"),
            ("License",   "l", "license"),
            ("About",     "a", "about"),
        ]},
        {"id": "quit", "title": "Quit", "kind": "action", "action": "quit"},
    ]
    SHORTCUTS = [("Ctrl+G", "Home"), ("Ctrl+H", "Help"), ("Ctrl+Q", "Quit")]
    ABOUT = {"name": "MyForge", "version": "0.1.0", "description": "…",
             "license": "GPL-3.0-or-later", "links": [("GitHub", "https://…")]}
    LICENSE_NOTICE = GPL3_NOTICE
    BINDINGS = [Binding("ctrl+g", "activate('home')", show=False, priority=True)]

    def compose_sections(self):
        with Vertical(id="sec-home"):
            yield Static("Hello from the workspace.")

    def on_action(self, action_id):
        ...  # handle your own menu actions here

if __name__ == "__main__":
    MyApp().run()
```

[`examples/demo.py`](examples/demo.py) shows the full pattern, including a Config
section with a floating editor and a delete confirmation stacked on top of it.

## What's in the box

| Object | What it is |
| --- | --- |
| `ForgeApp` | The base app — title bar, menu bar, section switching, and the Help windows. Subclass this. |
| `MenuBar` / `MenuDropdown` | The top bar and its dropdowns. |
| `ConfirmDialog` | A small yes/no. Stacks over anything and returns a boolean. |
| `ForgePanelScreen` | The standard scrolling panel — title, body, and a Close button. Use it for any information window. |
| `AboutDialog` / `LicenseDialog` / `ShortcutsDialog` | The built-in Help windows. |
| `FORGE_CSS` / `COLORS` / `GPL3_NOTICE` | The stylesheet, the Catppuccin palette, and a ready-made GPL notice. |

### How a menu is described

```python
{"id": "config", "title": "Config", "kind": "menu", "items": [
    ("New entry", "n", "add"),          # (label, letter to press, action id)
]}
```

Each entry has a `kind`:

- `"section"` — switch the workspace to that section
- `"menu"` — open a dropdown
- `"action"` — run something immediately

## Keyboard model

Menu options use their first letter as `Ctrl+<letter>`, and the app's shortcuts
take priority over the terminal's.

One sharp edge worth knowing: a few control keys are terminal conventions rather
than yours. `Ctrl+C` interrupts, `Ctrl+S` and `Ctrl+Q` are flow control, and
`Ctrl+H` is often Backspace. forgekit claims them with priority so your app wins
wherever the terminal allows it — but if a section's first letter is one of those
and your terminal insists on keeping it, underline a different letter for that
option instead.

## The Forge Suite

forgekit is the shared foundation for the Forge apps that ship with
[KognogOS](https://github.com/jetomev/KognogOS):

- **[grubForge](https://github.com/jetomev/grubforge)** — bootloader manager
- **[alacrittyForge](https://github.com/jetomev/alacrittyforge)** — terminal configurator
- **[bitlaForge](https://github.com/jetomev/bitlaforge)** — solo Bitcoin mining
- **[nogForge](https://github.com/jetomev/nogforge)** — package manager companion
- **welcomeforge** — the KognogOS Welcome Center, and forgekit's pilot app
- **installforge** — the KognogOS installer, built on the foundation welcomeforge matures

KognogOS decided in July 2026 that its system tools would be terminal apps rather
than graphical ones. That makes this library load-bearing: it's the reason the
installer and the welcome screen will feel like the same product as the tools you
use afterwards. The suite is growing toward a full **Forge Control Center** for
the whole OS.

## License & credits

GPL-3.0-or-later — see [`LICENSE`](LICENSE).

A human and AI collaboration: **Javier** ([@jetomev](https://github.com/jetomev))
with **Claude** (Anthropic) as co-developer.
