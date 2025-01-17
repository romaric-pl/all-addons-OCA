import unittest

from freezegun import freeze_time

from ..utils import file_open, file_path
from ..wamas2wamas import wamas2wamas


class TestWamas2wamas(unittest.TestCase):

    maxDiff = None

    def _test(self, filename, processed_qty=None):
        with file_open(
            file_path("tests/samples/wamas2wamas_input_%s.wamas" % filename)
        ) as infile, file_open(
            file_path("tests/samples/wamas2wamas_output_%s.wamas" % filename)
        ) as outfile:
            str_input = infile.read()
            output = wamas2wamas(str_input, processed_qty=processed_qty)
            expected_output = outfile.read()
            self.assertEqual(output, expected_output)

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_wea_full(self):
        """Reception where the demand is fully processed"""
        self._test("wea")

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_wea_partial(self):
        """Reception where the demand is partially processed"""
        self._test("wea_partial", processed_qty=1)

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_wea_nothing(self):
        """Reception where the demand is not processed at all"""
        self._test("wea_nothing", processed_qty=0)

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_kret_full(self):
        """Customer return where the demand is fully processed"""
        self._test("wea")

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_kret_partial(self):
        """Customer return where the demand is partially processed"""
        self._test("wea_partial", processed_qty=1)

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_kret_nothing(self):
        """Customer return where the demand is not processed at all"""
        self._test("wea_nothing", processed_qty=0)


if __name__ == "__main__":
    unittest.main()
