"""Tests for scripts/validate_board.py. Run: python3 -m unittest discover tests"""

import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "validate_board", Path(__file__).resolve().parent.parent / "scripts" / "validate_board.py"
)
validate_board = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_board)


class StockLibraries(unittest.TestCase):
    # Every symbol library KiCad 10's stock symbol set ships whose name the
    # old list missed, plus a few it already had.
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


if __name__ == "__main__":
    unittest.main()
