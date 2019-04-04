#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from converter_lib import Converter

app = Flask(__name__)


@app.route("/")
def usage():
    return 'Try: /currency_converter?amount=[amount]&input_currency=[inputcurrency][&output_currency=[outputcurrency]]'


@app.route("/currency_converter")
def convert():
    converter = Converter()

    try:
        amount = float(request.args.get('amount'))
    except TypeError:
        return usage()
    input_currency = converter.resolve_currency_name(request.args.get('input_currency'))
    output_currencies = [converter.resolve_currency_name(request.args.get('output_currency'))]

    if amount is None or input_currency is None:
        return usage()

    if output_currencies == [None]:
        output_currencies = converter.SupportedCurrencyList
        output_currencies.remove(input_currency)

    for curr in converter.SupportedCurrencyList:
        is_online = converter.download_actual_currency_rates(curr)
        if not is_online:
            print("You are offline. Exchange rates may not be up to date.")
            break

    return jsonify(Converter.create_output_data(amount, input_currency, output_currencies))


def main():
    app.run()


if __name__ == "__main__":
    main()
