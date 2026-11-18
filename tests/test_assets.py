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
