"""Tests for scripts/set_infra_ref.py. Run: python3 -m unittest discover tests"""

import importlib.util
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("set_infra_ref", ROOT / "scripts" / "set_infra_ref.py")
assert SPEC is not None and SPEC.loader is not None
set_infra_ref = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(set_infra_ref)

SCRIPT_WORKFLOWS = ["deploy-pages.yml", "kibot-ci.yml", "publish-kibot.yml", "validate-board.yml"]


def inputs(text):
    on = yaml.safe_load(text)[True]
    return on["workflow_call"]["inputs"]


class InfraRef(unittest.TestCase):
    def test_defaults_agree(self):
        """Every workflow that checks bread-infra out for scripts has one infra_ref default, the same in all.
        Which value (main, or the tag on a release commit) is checked in CI by set_infra_ref.py --check."""
        seen = set()
        for name in SCRIPT_WORKFLOWS:
            with self.subTest(name):
                text = (set_infra_ref.WORKFLOWS / name).read_text()
                refs = set_infra_ref.defaults(text)
                self.assertEqual(len(refs), 1)
                self.assertEqual(inputs(text)["infra_ref"]["default"], refs[0])
                self.assertIn("ref: ${{ inputs.infra_ref }}", text)
                seen.update(refs)
        self.assertEqual(len(seen), 1, seen)

    def test_every_infra_checkout_uses_the_input(self):
        """No workflow checks bread-infra out at a fixed ref; schema_ref is validate-manifest's own pin."""
        for path in sorted(set_infra_ref.WORKFLOWS.glob("*.yml")):
            text = path.read_text()
            if "repository: feastorg/bread-infra" not in text:
                continue
            for block in text.split("repository: feastorg/bread-infra")[1:]:
                ref_line = next(line.strip() for line in block.splitlines() if line.strip().startswith("ref:"))
                with self.subTest(path.name):
                    self.assertIn(ref_line, ("ref: ${{ inputs.infra_ref }}", "ref: ${{ inputs.schema_ref }}"))

    def test_set_changes_only_the_defaults(self):
        for name in SCRIPT_WORKFLOWS:
            with self.subTest(name):
                text = (set_infra_ref.WORKFLOWS / name).read_text()
                tagged = set_infra_ref.set_ref(text, "v1.3.0")
                self.assertEqual(inputs(tagged)["infra_ref"]["default"], "v1.3.0")
                before, after = yaml.safe_load(text), yaml.safe_load(tagged)
                original = before[True]["workflow_call"]["inputs"]["infra_ref"]["default"]
                after[True]["workflow_call"]["inputs"]["infra_ref"]["default"] = original
                self.assertEqual(before, after)
                self.assertEqual(set_infra_ref.set_ref(tagged, "main"), set_infra_ref.set_ref(text, "main"))


if __name__ == "__main__":
    unittest.main()
