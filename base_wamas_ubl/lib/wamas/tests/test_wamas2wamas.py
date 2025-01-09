import unittest

from freezegun import freeze_time

from ..utils import file_open, file_path
from ..wamas2wamas import wamas2wamas


class TestWamas2wamas(unittest.TestCase):

    maxDiff = None

    def _test(self, filename, partial_qty=False):
        with file_open(
            file_path("tests/samples/wamas2wamas_input_%s.wamas" % filename)
        ) as infile, file_open(
            file_path("tests/samples/wamas2wamas_output_%s.wamas" % filename)
        ) as outfile:
            str_input = infile.read()
            output = wamas2wamas(str_input, partial_qty=partial_qty)
            expected_output = outfile.read()
            self.assertEqual(output, expected_output)

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_full(self):
        self._test("wea")

    @freeze_time("2023-12-20 09:11:16")
    def testWamas2wamas_partial(self):
        self._test("wea_partial", partial_qty=True)


if __name__ == "__main__":
    unittest.main()
