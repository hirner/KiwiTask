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
        output_currencies = converter.SupportedCurrencyList.copy()
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
