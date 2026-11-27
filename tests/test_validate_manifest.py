"""Tests for scripts/validate_manifest.py and the v2 schemas. Run: python3 -m unittest discover tests"""

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("validate_manifest", ROOT / "scripts" / "validate_manifest.py")
validate_manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_manifest)

SLICE_V2 = {
    "schema_version": "2.0",
    "id": "slice-dcmt",
    "name": "DC Motor Controller",
    "summary": "Two brushed DC motor channels.",
    "category": "actuation",
    "status": "development",
    "hardware": {
        "hw_gen_current": 3,
        "interface": "SI1",
        "pcb": {"layers": 2, "dimensions": "70mm x 100mm", "thickness": "1.6mm"},
        "mounting": {"pattern": "slice-S-v0"},
        "mcu": {"form_factor": "nano"},
    },
    "interfaces": {"host": {"address_default": 18}},
    "metadata": {"tags": ["motor"]},
}

LOAF_V2 = {
    "schema_version": "2.0",
    "id": "loaf-x004",
    "name": "Four-slot backplane",
    "summary": "Four Slice slots and a chain connector.",
    "role": "backplane",
    "status": "development",
    "hardware": {"hw_gen_current": 3, "interface": "SI1", "pcb": {"layers": 2}},
    "interconnect": {"slice_slots": 4, "bus": {"type": "i2c"}},
}


class Manifests(unittest.TestCase):
    def check(self, filename, manifest):
        """Write the manifest under its real filename and validate it the way CI does."""
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / filename
            path.write_text(yaml.safe_dump(manifest))
            schema = validate_manifest.find_schema(None, path)
            return schema.name, validate_manifest.validate(path, schema)

    def test_v2_slice_passes_against_v2(self):
        self.assertEqual(self.check("slice.yaml", SLICE_V2), ("slice.schema.v2.json", []))

    def test_v2_loaf_passes_against_v2(self):
        self.assertEqual(self.check("loaf.yaml", LOAF_V2), ("loaf.schema.v2.json", []))

    def test_v1_manifest_still_uses_v1(self):
        m = yaml.safe_load((ROOT / "templates" / "slice.yaml.template").read_text())
        self.assertEqual(self.check("slice.yaml", m), ("slice.schema.json", []))

    def test_minimal_slice_without_optional_fields(self):
        m = copy.deepcopy(SLICE_V2)
        for key in ("interfaces", "metadata"):
            del m[key]
        m["hardware"]["mcu"] = None
        m["hardware"]["mounting"]["pattern"] = None
        self.assertEqual(self.check("slice.yaml", m)[1], [])

    def test_rejections(self):
        cases = {
            "dropped field": lambda m: m.update(license={"hardware": "CERN-OHL-S-2.0"}),
            "old status": lambda m: m.update(status="prototype"),
            "old pattern": lambda m: m["hardware"]["mounting"].update(pattern="slice-standard-v0"),
            "no interface": lambda m: m["hardware"].pop("interface"),
            "no thickness": lambda m: m["hardware"]["pcb"].pop("thickness"),
            "v1 mcu fields": lambda m: m["hardware"]["mcu"].update(primary="ATmega328P"),
        }
        for label, change in cases.items():
            with self.subTest(label):
                m = copy.deepcopy(SLICE_V2)
                change(m)
                self.assertNotEqual(self.check("slice.yaml", m)[1], [])


if __name__ == "__main__":
    unittest.main()
