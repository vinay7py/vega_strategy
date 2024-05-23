import csv
import time
from datetime import datetime, timedelta
import pandas as pd
from .data_retrieval import DataRetriever
from .greeks_calculations import option_vega, option_vomma, calculate_iv

class VegaStrategy:
    def __init__(self, retriever, expiry):
        self.retriever = retriever
        self.expiry = expiry
        self.expiry_1 = datetime.strptime(expiry, '%Y-%m-%d') + timedelta(hours=15, minutes=30)
        self.instruments = pd.read_csv('data/instruments.csv')
        
        self.underlying_inst_id = self.instruments[(self.instruments.exchange == 'NSE') & (self.instruments.name == 'NIFTY 50') & (self.instruments.segment == 'INDICES')].iloc[0]['instrument_token']

        self.today = datetime.now().strftime('%Y-%m-%d')
        self.open_price = self.retriever.get_open_price(self.underlying_inst_id, self.today)
    
    def run_strategy(self):
        while True:
            now = datetime.now()
            if self.is_market_open(now):
                self.calculate_vega_vomma(now)
                self.log_results()

    def is_market_open(self, now):
        time_1 = now.replace(hour=9, minute=15, second=0, microsecond=0)
        time_2 = now.replace(hour=15, minute=30, second=0, microsecond=0)
        return time_1 < now < time_2 and now.second == 0

    def calculate_vega_vomma(self, now):
        underlying_price = self.retriever.get_historical_data(self.underlying_inst_id, self.today, now)['close'][0]
        atm_live = round(underlying_price / 50) * 50
        year_to_expiry = (self.expiry_1 - now).days / 365
        
        strike_prices_ce = [atm_live + i * 50 for i in range(1, 10)]
        strike_prices_pe = [atm_live - i * 50 for i in range(1, 10)]
        
        vega_sum, vega_sum_pe = 0, 0
        vomma_sum, vomma_sum_pe = 0, 0
        
        for strike in strike_prices_ce:
            vega, vomma = self.calculate_greek_changes(strike, 'call', underlying_price, year_to_expiry)
            vega_sum += vega
            vomma_sum += vomma
        
        for strike in strike_prices_pe:
            vega, vomma = self.calculate_greek_changes(strike, 'put', underlying_price, year_to_expiry)
            vega_sum_pe += vega
            vomma_sum_pe += vomma
        
        self.log_to_csv(vega_sum, vega_sum_pe, vomma_sum, vomma_sum_pe)
    
    def calculate_greek_changes(self, strike, option_type, underlying_price, year_to_expiry):
        instrum = self.instruments[(self.instruments.exchange == 'NFO') & (self.instruments.name == 'NIFTY') & (self.instruments.instrument_type == option_type.upper()) & (self.instruments.strike == strike)]
        instrum = instrum[instrum.expiry == self.expiry]
        instrum = int(instrum.iloc[0]['instrument_token'])
        
        ltp = self.retriever.get_historical_data(instrum, self.today, datetime.now())['close'][0]
        iv_live = calculate_iv(ltp, underlying_price, strike, year_to_expiry, 0.07, 0.02, option_type)
        vega_live = option_vega(underlying_price, strike, year_to_expiry, 0.07, iv_live, 0.02)
        vomma_live = option_vomma(underlying_price, strike, year_to_expiry, 0.07, iv_live, 0.02)
        
        initial_open = self.retriever.get_open_price(instrum, self.today)
        iv_open = calculate_iv(initial_open, self.open_price, strike, year_to_expiry, 0.07, 0.02, option_type)
        vega_open = option_vega(self.open_price, strike, year_to_expiry, 0.07, iv_open, 0.02)
        vomma_open = option_vomma(self.open_price, strike, year_to_expiry, 0.07, iv_open, 0.02)
        
        vega_change = (vega_live - vega_open) / vega_open * 100
        vomma_change = (vomma_live - vomma_open) / vomma_open * 100
        
        return vega_change, vomma_change
    
    def log_to_csv(self, vega_sum, vega_sum_pe, vomma_sum, vomma_sum_pe):
        with open('data/vega_vomma_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([vega_sum, vega_sum_pe, vomma_sum, vomma_sum_pe, datetime.now()])
