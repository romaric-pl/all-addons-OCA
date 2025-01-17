# Copyright 2023 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import argparse
import logging
from pprint import pformat

from freezegun import freeze_time

from . import const, utils
from .wamas2ubl import wamas2dict

_logger = logging.getLogger("wamas2wamas")


def simulate_response(dict_wamas_in, processed_qty=None):
    res = []
    line_idx = 0
    dict_parent_id = {}
    for telegram_type_in, dicts in dict_wamas_in.items():
        for telegram_type_out in const.DICT_CONVERT_WAMAS_TYPE[telegram_type_in]:
            grammar_out = const.DICT_WAMAS_GRAMMAR[telegram_type_out]
            for dict_item in dicts:
                line_idx += 1
                line = utils.generate_wamas_line(
                    dict_item,
                    grammar_out,
                    line_idx=line_idx,
                    dict_parent_id=dict_parent_id,
                    telegram_type_out=telegram_type_out,
                    do_wamas2wamas=True,
                    processed_qty=processed_qty,
                )
                if line:
                    res.append(line)
    return res


def wamas2wamas(infile, processed_qty=None):
    data = wamas2dict(infile)
    _logger.debug(pformat(data))
    wamas_lines = simulate_response(data, processed_qty=processed_qty)
    return "\n".join(wamas_lines)


@freeze_time("2023-12-20 09:11:16")
def main():
    parser = argparse.ArgumentParser(
        description="Converts a wamas message into wamas response.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="enable debug log")
    parser.add_argument(
        "-p",
        "--processed-qty",
        type=float,
        dest="processed_qty",
        help="quantity processed, by default complete quantity is processed",
    )
    parser.add_argument(
        "-o", "--output", dest="outputfile", help="write result in this file"
    )
    parser.add_argument("inputfile", help="read message from this file")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    infile = utils.file_open(args.inputfile).read()
    res = wamas2wamas(infile, args.processed_qty)
    if args.outputfile:
        fd = utils.file_open(args.outputfile, "w")
        fd.write(res)
    else:
        print(res)  # pylint: disable=print-used


if __name__ == "__main__":
    main()
