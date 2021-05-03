import pandas as pd
from binance.client import Client
import datetime as dt


client=Client()

def get_historical_ohlc_data(symbol,past_days=None,interval=None):
        
        """Returns historcal klines from past for given symbol and interval
        past_days: how many days back one wants to download the data"""


        """symbol example

        'BTCUSDT'

        'ETHUSDT'

        'XRPUSDT'

        """

        """interval example
        num +

        m: minute
        h: hour

        """
        
        if not interval:
            interval='15m'
        if not past_days:
            past_days= 30
    
        start_str=str((pd.to_datetime('today')-pd.Timedelta(str(past_days)+' days')).date())
        
        D=pd.DataFrame(client.get_historical_klines(symbol=symbol,start_str=start_str,interval=interval))
        D.columns=['open_time','open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol','is_best_match']
        D['open_date_time']=[dt.datetime.fromtimestamp(x/1000) for x in D.open_time]
        D['symbol']=symbol
        D=D[['symbol','open_date_time','open', 'high', 'low', 'close', 'volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol']]
    
        return D