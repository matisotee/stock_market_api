from dataclasses import dataclass
import requests


def get_stock_data(symbol):
    response = requests.get(
        f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=X86NOH6II01P7R24'
    ).json()

    if response.get('Error Message'):
        raise InvalidSymbolError()

    unsorted_daily_data = response['Time Series (Daily)']
    daily_data = dict(sorted(unsorted_daily_data.items()))
    last_date = list(daily_data.keys())[-1]
    previous_date = list(daily_data.keys())[-2]

    open_price = daily_data[last_date]['1. open']
    higher_price = daily_data[last_date]['2. high']
    lower_price = daily_data[last_date]['3. low']
    close_price = daily_data[last_date]['4. close']
    previous_close_price = daily_data[previous_date]['4. close']
    close_price_variation = calculate_variation(close_price, previous_close_price)

    return StockData(open_price, higher_price, lower_price, close_price_variation)


def calculate_variation(current_value, previous_value):
    current_value = float(current_value)
    previous_value = float(previous_value)
    variation = ((current_value - previous_value) / previous_value) * 100
    rounded_variation = round(variation, 2)
    return f'{rounded_variation}%'


@dataclass
class StockData:
    open_price: str
    higher_price: str
    lower_price: str
    close_price_variation: str


class InvalidSymbolError(Exception):
    pass
