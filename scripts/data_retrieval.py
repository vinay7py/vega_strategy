import pandas as pd
from datetime import datetime
from kiteconnect import KiteConnect

class DataRetriever:
    def __init__(self, user_id, password, twofa):
        self.kite = KiteConnect(api_key="your_api_key")
        self.kite.set_access_token("your_access_token")

    def get_instruments(self):
        instruments = pd.DataFrame(self.kite.instruments())
        instruments.to_csv('data/instruments.csv')
        return instruments

    def get_historical_data(self, instrument_token, from_date, to_date, interval="day"):
        return self.kite.historical_data(instrument_token=instrument_token, from_date=from_date, to_date=to_date, interval=interval)

    def get_open_price(self, instrument_token, date):
        data = self.kite.historical_data(instrument_token=instrument_token, from_date=date, to_date=date, interval="day")
        return data[0]['open']
