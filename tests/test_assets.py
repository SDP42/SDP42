"""Checks that keep the README's artwork valid and in sync with its data.

    python -m unittest discover -s tests
"""
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
sys.path.insert(0, str(ROOT / "scripts"))

import data  # noqa: E402

SVG = "{http://www.w3.org/2000/svg}"


def svgs():
    return sorted(ASSETS.rglob("*.svg"))


class SvgTests(unittest.TestCase):
    def test_every_svg_is_well_formed(self):
        for path in svgs():
            with self.subTest(path=path.name):
                ET.parse(path)

    def test_every_svg_is_labelled(self):
        for path in svgs():
            with self.subTest(path=path.name):
                root = ET.parse(path).getroot()
                self.assertEqual(root.get("role"), "img")
                self.assertTrue(root.get("aria-label"))
                self.assertIsNotNone(root.find(f"{SVG}title"))

    def test_no_external_resources(self):
        # GitHub serves README images through a proxy that blocks anything
        # an SVG tries to fetch, so every asset must be self-contained.
        for path in svgs():
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r'(href|src)="https?://')
                self.assertNotIn("@import", text)
                self.assertNotIn("<script", text)

    def test_assets_stay_small(self):
        for path in svgs():
            with self.subTest(path=path.name):
                self.assertLess(path.stat().st_size, 100_000)

    def test_motion_can_be_turned_off(self):
        for path in svgs():
            with self.subTest(path=path.name):
                self.assertIn("prefers-reduced-motion", path.read_text(encoding="utf-8"))


class ReadmeTests(unittest.TestCase):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_local_images_exist(self):
        for src in re.findall(r'src="((?:assets|profile-3d-contrib)/[^"]+)"', self.readme):
            with self.subTest(src=src):
                self.assertTrue((ROOT / src).is_file(), src)

    def test_images_have_alt_text(self):
        for tag in re.findall(r"<img [^>]+>", self.readme):
            with self.subTest(tag=tag[:60]):
                self.assertRegex(tag, r'alt="[^"]+"')

    def test_in_page_links_resolve(self):
        anchors = set(re.findall(r'<a id="([^"]+)"', self.readme))
        for target in re.findall(r'href="#([^"]+)"', self.readme):
            with self.subTest(target=target):
                self.assertIn(target, anchors)

    def test_every_card_is_used(self):
        for card in (ASSETS / "cards").glob("*.svg"):
            if card.stem.endswith("mirage"):
                continue  # the captain has its own feature card
            with self.subTest(card=card.name):
                self.assertIn(f"assets/cards/{card.name}", self.readme)

    def test_links_to_the_portfolio(self):
        self.assertIn(data.PORTFOLIO, self.readme)


class DataTests(unittest.TestCase):
    def test_squad_is_a_full_eleven(self):
        numbers = [p["no"] for p in data.SQUAD]
        self.assertEqual(sorted(numbers), list(range(1, 12)))
        self.assertEqual(sum(1 for p in data.SQUAD if p.get("captain")), 1)

    def test_players_stay_on_the_pitch(self):
        for p in data.SQUAD:
            x, z = p["at"]
            with self.subTest(player=p["title"]):
                self.assertLessEqual(abs(x), 52.5)
                self.assertLessEqual(abs(z), 34)

    def test_passing_order_uses_real_shirts(self):
        numbers = {p["no"] for p in data.SQUAD}
        self.assertTrue(set(data.PASSING_ORDER) <= numbers)

    def test_card_copy_fits(self):
        for p in data.SQUAD:
            with self.subTest(player=p["title"]):
                self.assertLessEqual(len(p["tagline"]), 68)
                self.assertEqual(len(p["points"]), 3)
                for point in p["points"]:
                    self.assertLessEqual(len(point), 70)

    def test_commit_total_matches_the_squad(self):
        total = sum(p["commits"] for p in data.SQUAD)
        shown = dict((label, value) for value, label in data.STATS)["Commits across the XI"]
        self.assertEqual(int(shown.replace(",", "")), total)
