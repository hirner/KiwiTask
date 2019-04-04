#!/usr/bin/python
import json
import requests


class Converter:
    SupportedCurrencyList = ["USD", "AUD", "CAD", "CHF", "CNY", "EUR",
                             "GBP", "HKD", "ILS", "INR", "JPY", "KRW",
                             "MXN", "MYR", "NOK", "NZD", "RUB", "SEK",
                             "SGD", "THB", "TRY", "ZAR"]

    CurrencySynonyms = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "CNY"}

    ExchangeRatesURL = "https://api.exchangerate-api.com/v4/latest/" #https://api.exchangeratesapi.io/latest?base=

    def __init__(self):
        with open('config.json') as f:
            data = json.load(f)
        try:
            self.SupportedCurrencyList = data["SupportedCurrencyList"]
            self.CurrencySynonyms = data["CurrencySynonyms"]
            self.ExchangeRatesURL = data["ExchangeRatesURL"]
        except KeyError:
            pass

    def download_actual_currency_rates(self, currency_name):
        url = self.ExchangeRatesURL + currency_name
        try:
            r = requests.get(url)
        except requests.ConnectionError:
            return False
        with open('rates\\' + currency_name + '.json', 'w') as outfile:
            json.dump(r.json(), outfile)
        return True

    def resolve_currency_name(self, name_to_resolve):
        if name_to_resolve in self.SupportedCurrencyList:
            return name_to_resolve
        elif name_to_resolve in self.CurrencySynonyms:
            return self.CurrencySynonyms[name_to_resolve]
        else:
            return None

    @staticmethod
    def obtain_currency_rate(input_currency, output_currency):
        with open('rates\\' + input_currency + '.json') as f:
            data = json.load(f)
        rates = data['rates']
        return rates[output_currency]

    @staticmethod
    def calculate_output_amount(amount, input_currency, output_currency):
        return amount * Converter.obtain_currency_rate(input_currency, output_currency)

    @staticmethod
    def create_output_data(amount, input_currency, output_currencies):
        data = {"input": {"amount": amount, "currency": input_currency},
                "output": {}}
        output = {}
        for item in output_currencies:
            output[item] = Converter.calculate_output_amount(amount, input_currency, item)
        data["output"] = output
        return data
