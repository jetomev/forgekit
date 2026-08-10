#!/usr/bin/env python3
"""Regenerate the README screenshot gallery from examples/demo.py.

Run from the repo root:  PYTHONPATH=. python docs/screenshots/generate.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples.demo import BitlaForgeDemo, EditDialog  # noqa: E402

OUT = Path(__file__).resolve().parent
SIZE = (110, 32)


def shot(app, name: str) -> None:
    app.save_screenshot(filename=f"{name}.svg", path=str(OUT))
    print(f"  {name}.svg")


async def main() -> None:
    app = BitlaForgeDemo()
    async with app.run_test(size=SIZE) as pilot:
        await pilot.pause()
        shot(app, "01-shell")

        # Config section with the edit dialog floating
        app.action_activate("config"); await pilot.pause()
        await pilot.pause()
        app.push_screen(EditDialog("Edit — pool_url",
                                   {"name": "pool_url",
                                    "value": "stratum+tcp://solo.ckpool.org:3333",
                                    "type": "text", "enabled": True}))
        await pilot.pause()
        shot(app, "02-edit-dialog")
        await pilot.press("escape"); await pilot.pause()

        # Help menu open (the dropdown itself)
        app.action_activate("help"); await pilot.pause()
        shot(app, "03-menu-open")
        await pilot.press("escape"); await pilot.pause()

        # About window
        app.action_act("about"); await pilot.pause()
        shot(app, "04-about-window")

    print("forgekit gallery done.")


asyncio.run(main())
