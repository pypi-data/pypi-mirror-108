import numpy as np
import pandas as pd

from zipline.pipeline.factors import SimpleMovingAverage, AverageDollarVolume, Latest
from zipline.pipeline.filters import StaticSids
from zipline.pipeline.data import USEquityPricing

from fsharadar import sep
from fsharadar import daily
from fsharadar.db_access import DBReader


class AverageMarketCap(SimpleMovingAverage):
    inputs = [daily.Fundamentals.marketcap]

def TradableStocksUS():
    
    # Domestic Common Stocks
    sep_bundle_data = sep.load()
    asset_finder = sep_bundle_data.asset_finder
    db_url = asset_finder.engine.url.database.replace('assets-7.sqlite', 'fsharadar-1.sqlite')
    
    db_reader = DBReader(db_url)
    tickers_df = db_reader.get_tickers()
    dcs_sids = tickers_df[tickers_df.category == "Domestic Common Stock"].sid.values
    dcs_universe = StaticSids(dcs_sids)
    
    # marketcap > 350 M
    tradable_stocks = AverageMarketCap(window_length=20, mask=dcs_universe) >= 350.0
    
    # dollar volume > 2.5 M
    tradable_stocks = AverageDollarVolume(window_length=200, mask=tradable_stocks) >= 2.5e6
    
    # price > $5. 
    tradable_stocks = Latest([USEquityPricing.close], mask=tradable_stocks) > 5.0
    
    return tradable_stocks
