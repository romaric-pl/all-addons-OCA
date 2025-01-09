import ast
import unittest

from freezegun import freeze_time

from ..dict2wamas import dict2wamas
from ..utils import file_open, file_path


class TestDict2wamas(unittest.TestCase):

    maxDiff = None

    def _test(self, msg_type, filename):
        with file_open(
            file_path("tests/samples/dict2wamas_input%s.dict" % filename)
        ) as infile, file_open(
            file_path("tests/samples/dict2wamas_output%s.wamas" % filename)
        ) as outfile:
            dict_input = ast.literal_eval(infile.read())
            output = dict2wamas(dict_input, msg_type)
            expected_output = outfile.read()
            self.assertEqual(output, expected_output)

    @freeze_time("2024-02-11 22:14:22")
    def test_LST(self):
        self._test("Supplier", "")

    @freeze_time("2024-02-11 22:15:32")
    def test_KSTAUS(self):
        self._test("CustomerDeliveryPreferences", "_2")


if __name__ == "__main__":
    unittest.main()
