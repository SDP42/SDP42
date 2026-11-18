"""Regenerate every animated SVG used by the profile README.

    python scripts/build.py           # write assets/
    python scripts/build.py --check   # fail if assets/ is out of date

Only the standard library is needed. Output is deterministic (seeded
randomness, no timestamps), so --check can run in CI.
"""
import argparse
import sys
from pathlib import Path

import banners
import bench
import captain
import cards
import cta
import hero
import honours
import pitch
import scoreboard
import ticker
from svgkit import ASSETS

BUILDERS = (hero, ticker, banners, scoreboard, captain, pitch, cards, bench, honours, cta)


def snapshot():
    return {p: p.read_bytes() for p in ASSETS.rglob("*.svg")}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if any asset would change")
    args = parser.parse_args()

    before = snapshot()
    for module in BUILDERS:
        module.build()
    after = snapshot()

    changed = sorted(str(p.relative_to(ASSETS)) for p in after if before.get(p) != after[p])
    total = sum(len(b) for b in after.values())
    print(f"{len(after)} SVGs, {total / 1024:.0f} KB in total")
    if changed:
        print("changed:", *changed, sep="\n  ")
    if args.check and changed:
        print("assets/ is stale: run `python scripts/build.py` and commit the result.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(main())
