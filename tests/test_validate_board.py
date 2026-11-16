"""Stock library references must name a symbol or footprint that exists.

Run with: python3 -m unittest discover tests
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_board.py"
spec = importlib.util.spec_from_file_location("validate_board", SCRIPT)
vb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vb)

DEVICE_SYM = """(kicad_symbol_lib
\t(symbol "FerriteBead_Small"
\t\t(symbol "FerriteBead_Small_0_1")
\t)
)
"""


class StockReferences(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.sym = root / "symbols"
        self.fp = root / "footprints"
        self.hw = root / "board" / "hardware"
        self.sym.mkdir()
        (self.fp / "Resistor_SMD.pretty").mkdir(parents=True)
        self.hw.mkdir(parents=True)
        (self.sym / "Device.kicad_sym").write_text(DEVICE_SYM)
        (self.fp / "Resistor_SMD.pretty" / "R_0805_2012Metric.kicad_mod").write_text("(footprint)\n")

    def tearDown(self):
        self.tmp.cleanup()

    def problems(self, sch_lib_id=None, pcb_fp=None):
        if sch_lib_id:
            (self.hw / "b.kicad_sch").write_text(f'(kicad_sch (symbol (lib_id "{sch_lib_id}")))\n')
        if pcb_fp:
            (self.hw / "b.kicad_pcb").write_text(f'(kicad_pcb\n\t(footprint "{pcb_fp}"\n\t)\n)\n')
        out: list[str] = []
        vb.check_libraries(self.hw, {}, {}, out, self.sym, self.fp)
        return out

    def test_existing_stock_symbol_passes(self):
        self.assertEqual(self.problems(sch_lib_id="Device:FerriteBead_Small"), [])

    def test_missing_stock_symbol_fails(self):
        out = self.problems(sch_lib_id="Device:Ferrite_Bead_Small")
        self.assertEqual(len(out), 1)
        self.assertIn("Device:Ferrite_Bead_Small", out[0])

    def test_sub_unit_name_is_not_a_symbol(self):
        self.assertEqual(len(self.problems(sch_lib_id="Device:FerriteBead_Small_0_1")), 1)

    def test_existing_stock_footprint_passes(self):
        self.assertEqual(self.problems(pcb_fp="Resistor_SMD:R_0805_2012Metric"), [])

    def test_missing_stock_footprint_fails(self):
        out = self.problems(pcb_fp="Resistor_SMD:R_0805_Missing")
        self.assertEqual(len(out), 1)
        self.assertIn("Resistor_SMD:R_0805_Missing", out[0])

    def test_stock_libraries_absent_keeps_skipping(self):
        out: list[str] = []
        (self.hw / "b.kicad_sch").write_text('(kicad_sch (symbol (lib_id "Device:Nope")))\n')
        vb.check_libraries(self.hw, {}, {}, out)
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
