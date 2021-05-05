import pandas as pd

def rsi(ohlc: pd.DataFrame, period: int = 14):
    
        delta = ohlc.diff()
    
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
    
        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    
        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")  