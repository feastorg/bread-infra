"""Tests for scripts/migrate_manifest_v2.py. Run: python3 -m unittest discover tests"""

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


migrate = load("migrate_manifest_v2")
validate = load("validate_manifest")

SLICE_V1 = yaml.safe_load((ROOT / "templates" / "slice.yaml.template").read_text())
LOAF_V1 = yaml.safe_load((ROOT / "templates" / "loaf.yaml.template").read_text())


def board(w, h):
    """A board file whose Edge.Cuts is a w x h rectangle at (100, 50), written the way KiCad 10 writes it."""
    pts = [(100, 50), (100 + w, 50), (100 + w, 50 + h), (100, 50 + h)]
    lines = "".join(
        f'\t(gr_line\n\t\t(start {a[0]} {a[1]})\n\t\t(end {b[0]} {b[1]})\n\t\t(layer "Edge.Cuts")\n\t)\n'
        for a, b in zip(pts, pts[1:] + pts[:1], strict=True)
    )
    silk = '\t(gr_line\n\t\t(start 0 0)\n\t\t(end 500 500)\n\t\t(layer "F.SilkS")\n\t)\n'
    return f"(kicad_pcb\n{lines}{silk})\n"


class Migrate(unittest.TestCase):
    def convert(self, kind, v1, size=None, use_format=True):
        out, notes = migrate.migrate(kind, copy.deepcopy(v1), 3, size, use_format)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / f"{kind}.yaml"
            path.write_text(yaml.safe_dump(out))
            errors = validate.validate(path, validate.find_schema(None, path))
        self.assertEqual(errors, [])
        return out, notes

    def test_outline_ignores_other_layers(self):
        with tempfile.TemporaryDirectory() as d:
            pcb = Path(d) / "BREAD_Slice.kicad_pcb"
            pcb.write_text(board(70, 100))
            self.assertEqual(migrate.outline(pcb), (70.0, 100.0))

    def test_format_from_outline(self):
        cases = {(70, 100): "slice-S-v0", (100.116, 144.894): "slice-L-v0", (100.116, 99.951): None, (70.6, 100): None}
        for size, fmt in cases.items():
            with self.subTest(size=size):
                out, _ = self.convert("slice", SLICE_V1, size)
                self.assertEqual(out["hardware"]["mounting"]["pattern"], fmt)

    def test_dimensions_follow_the_board(self):
        v1 = copy.deepcopy(SLICE_V1)
        v1["hardware"]["pcb"]["dimensions"] = "70mm x 100mm"
        out, notes = self.convert("slice", v1, (100.116, 144.894))
        self.assertEqual(out["hardware"]["pcb"]["dimensions"], "100mm x 145mm")
        self.assertTrue(any("pcb.dimensions" in n for n in notes))

    def test_no_format(self):
        out, _ = self.convert("slice", SLICE_V1, (100, 145), use_format=False)
        self.assertIsNone(out["hardware"]["mounting"]["pattern"])
        self.assertEqual(out["hardware"]["pcb"]["dimensions"], "100mm x 145mm")

    def test_status_map(self):
        expected = {
            "concept": "concept",
            "prototype": "development",
            "validated": "development",
            "released": "development",
            "deprecated": "retired",
        }
        for old, new in expected.items():
            with self.subTest(old=old):
                v1 = copy.deepcopy(SLICE_V1)
                v1["status"] = old
                self.assertEqual(self.convert("slice", v1, (70, 100))[0]["status"], new)

    def test_kept_fields(self):
        v1 = copy.deepcopy(SLICE_V1)
        v1["hardware"]["mcu"] = {
            "type": "dev-board-socket",
            "form_factor": "pico",
            "primary": "RP2040",
            "supported": [],
        }
        v1["interfaces"]["host"]["address_default"] = 18
        out, _ = self.convert("slice", v1, (70, 100))
        self.assertEqual(out["hardware"]["hw_gen_current"], 3)
        self.assertEqual(out["hardware"]["interface"], "SI1")
        self.assertEqual(out["hardware"]["mcu"], {"form_factor": "pico"})
        self.assertEqual(out["interfaces"]["host"]["address_default"], 18)
        self.assertEqual(out["metadata"]["tags"], v1["metadata"]["tags"])

    def test_loaf(self):
        out, _ = self.convert("loaf", LOAF_V1)
        self.assertEqual(out["interconnect"]["slice_slots"], LOAF_V1["interconnect"]["slice_slots"])
        self.assertNotIn("mounting", out["hardware"])

    def test_unknown_status_stops(self):
        v1 = copy.deepcopy(SLICE_V1)
        v1["status"] = "shipped"
        with self.assertRaises(SystemExit):
            migrate.migrate("slice", v1, 3, (70, 100), True)


if __name__ == "__main__":
    unittest.main()
