"""Tests for scripts/validate_board.py. Run: python3 -m unittest discover tests"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "validate_board", Path(__file__).resolve().parent.parent / "scripts" / "validate_board.py"
)
validate_board = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_board)


class StockLibraries(unittest.TestCase):
    # A sample of KiCad 10's stock symbol libraries, one per pattern the
    # old list lacked, plus a few it already had.
    STOCK = [
        "4xxx", "4xxx_IEEE", "74xGxx", "74xx", "74xx_IEEE", "Auxiliary_Items", "Buffer",
        "CPLD_Xilinx", "CPU", "CPU_NXP_IMX", "DSP_Texas", "Fiber_Optic", "FPGA_Lattice",
        "GPU", "LED", "Security", "Device", "power", "Connector_Generic", "Logic_LevelTranslator",
    ]
    NOT_STOCK = ["KMLib_Boards_Modules", "KiCad-Master-Lib", "kml-custom", "BREAD_Slice"]

    def test_stock_libraries_match(self):
        for lib in self.STOCK:
            with self.subTest(lib=lib):
                self.assertTrue(validate_board.STOCK.match(lib))

    def test_other_libraries_do_not_match(self):
        for lib in self.NOT_STOCK:
            with self.subTest(lib=lib):
                self.assertIsNone(validate_board.STOCK.match(lib))


DEVICE_SYM = """(kicad_symbol_lib
\t(symbol "FerriteBead_Small"
\t\t(symbol "FerriteBead_Small_0_1")
\t)
)
"""


class StockReferences(unittest.TestCase):
    """Stock library references must name a symbol or footprint that exists."""

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
        validate_board.check_libraries(self.hw, {}, {}, out, self.sym, self.fp)
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
        validate_board.check_libraries(self.hw, {}, {}, out)
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
