# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2019 Erik Hirner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import getopt
import sys
import json
from converter_lib import Converter


def usage():
    print(
        'currency_converter.py --amount <amount> --input_currency <inputcurrency> [--output_currency <outputcurrency>]'
    )


def main(argv):
    converter = Converter()

    amount = ''
    input_currency = ''
    output_currencies = ''

    try:
        opts, args = getopt.getopt(argv, "h", ["amount=", "input_currency=", "output_currency="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in "--amount":
            try:
                amount = float(arg)
            except TypeError:
                print("Amount you entered is not valid")
                usage()
                sys.exit(2)
        elif opt in "--input_currency":
            input_currency = converter.resolve_currency_name(arg)
            if input_currency is None:
                print("Input currency you entered is not supported")
                usage()
                sys.exit(2)
        elif opt in "--output_currency":
            output_currencies = [converter.resolve_currency_name(arg)]
            if output_currencies is None:
                print("Output currency you entered is not supported")
                usage()
                sys.exit(2)

    if input_currency == '' or amount == '':
        usage()
        sys.exit(2)

    if output_currencies == '':
        output_currencies = converter.SupportedCurrencyList.copy()
        output_currencies.remove(input_currency)

    for curr in converter.SupportedCurrencyList:
        is_online = converter.download_actual_currency_rates(curr)
        if not is_online:
            print("You are offline. Exchange rates may not be up to date.")
            break

    print(json.dumps(Converter.create_output_data(amount, input_currency, output_currencies), indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
