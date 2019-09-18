import json
import requests

with open('../resources/environment.json') as json_data:
    parameters = json.load(json_data)

api_url_base = "https://www.alphavantage.co/query?"


def get_stock_global_quote(symbol):
    parameters['function'] = 'GLOBAL_QUOTE'
    parameters['symbol'] = symbol
    response = requests.get(api_url_base, params=parameters)
    return response.json()


