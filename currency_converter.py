#!/usr/bin/python
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
        output_currencies = converter.SupportedCurrencyList
        output_currencies.remove(input_currency)

    for curr in converter.SupportedCurrencyList:
        is_online = converter.download_actual_currency_rates(curr)
        if not is_online:
            print("You are offline. Exchange rates may not be up to date.")
            break

    print(json.dumps(Converter.create_output_data(amount, input_currency, output_currencies), indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
