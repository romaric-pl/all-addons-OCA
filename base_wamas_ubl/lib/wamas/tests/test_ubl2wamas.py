import unittest
from datetime import date, datetime

from freezegun import freeze_time

from ..ubl2wamas import ubl2wamas
from ..utils import file_open, file_path, set_value_to_string


class TestUbl2wamas(unittest.TestCase):

    maxDiff = None

    def test_helpers(self):
        dict_data = {
            "str": [
                {
                    "input_val": "WEAPQ0050",
                    "expected_output_val": "WEAPQ0050",
                    "length": 9,
                    "dp": False,
                },
            ],
            "int": [
                {
                    "input_val": 30,
                    "expected_output_val": "000030",
                    "length": 6,
                    "dp": False,
                },
                {
                    "input_val": "30",
                    "expected_output_val": "000030",
                    "length": 6,
                    "dp": False,
                },
            ],
            "float": [
                {
                    "input_val": 5184.0,
                    "expected_output_val": "000005184000",
                    "length": 12,
                    "dp": 3,
                },
                {
                    "input_val": "5184.0",
                    "expected_output_val": "000005184000",
                    "length": 12,
                    "dp": 3,
                },
            ],
            "date": [
                {
                    "input_val": "2023-05-01",
                    "expected_output_val": "20230501",
                    "length": 8,
                    "dp": False,
                },
                {
                    "input_val": date(2023, 5, 1),
                    "expected_output_val": "20230501",
                    "length": 8,
                    "dp": False,
                },
                {
                    "input_val": datetime(2023, 5, 1, 0, 0),
                    "expected_output_val": "20230501",
                    "length": 8,
                    "dp": False,
                },
            ],
            "datetime": [
                {
                    "input_val": "2023-05-01 06:57:23",
                    "expected_output_val": "20230501085723",
                    "length": 14,
                    "dp": False,
                },
                {
                    "input_val": datetime(2023, 5, 1, 6, 57, 23),
                    "expected_output_val": "20230501",
                    "length": 8,
                    "dp": False,
                },
            ],
            "bool": [
                {
                    "input_val": "N",
                    "expected_output_val": "N",
                    "length": 1,
                    "dp": False,
                },
            ],
        }

        for ttype in dict_data:
            for data in dict_data[ttype]:
                input_val = data["input_val"]
                expected_output_val = data["expected_output_val"]
                length = data["length"]
                dp = data["dp"]

                output_val = set_value_to_string(
                    input_val, ttype, length, dp, do_convert_tz=True
                )
                self.assertEqual(output_val, expected_output_val)

    @freeze_time("2023-05-01")
    def _convert_ubl2wamas(
        self, input_filename, expected_output_filename, telegram_type
    ):
        path = file_path("tests/samples/")
        with file_open(path + input_filename) as inputfile, file_open(
            path + expected_output_filename
        ) as outputfile:
            str_input = inputfile.read()
            output = ubl2wamas(str_input, telegram_type)
            expected_output = outputfile.read().strip("\n")
            self.assertEqual(output, expected_output)

    def test_convert_ubl2wamas_picking(self):
        input_file = "UBL2WAMAS-SAMPLE_AUSK_AUSP-DESPATCH_ADVICE2.xml"
        expected_output = "UBL2WAMAS-SAMPLE_AUSK_AUSP.wamas"
        msg_type = "Picking"
        self._convert_ubl2wamas(input_file, expected_output, msg_type)

    def test_convert_ubl2wamas_reception(self):
        input_file = "UBL2WAMAS-SAMPLE_WEAK_WEAP-DESPATCH_ADVICE.xml"
        expected_output = "UBL2WAMAS-SAMPLE_WEAK_WEAP.wamas"
        msg_type = "Reception"
        self._convert_ubl2wamas(input_file, expected_output, msg_type)

    def test_convert_ubl2wamas_return(self):
        input_file = "UBL2WAMAS-SAMPLE_KRETK_KRETP-DESPATCH_ADVICE.xml"
        expected_output = "UBL2WAMAS-SAMPLE_KRETK_KRETP.wamas"
        msg_type = "Return"
        self._convert_ubl2wamas(input_file, expected_output, msg_type)


if __name__ == "__main__":
    unittest.main()
