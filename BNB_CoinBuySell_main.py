### License ###
### https://sharpswan.github.io/ ###

### CoinBuySell made by sharpswan ###


## Binance version ##

from binance.client import Client
import datetime as dt
import pandas as pd
import telegram
import time
import ohlc
import indicators



coin_name = 'BTCUSDT'
inteval_time = '15m'
sendTelegram = True   #you can turn or off to writedown here 'True = on' and 'False = off'



while True:
    client=Client()

    # get ohlc data    
    df=ohlc.get_historical_ohlc_data(symbol=coin_name, past_days=None, interval=inteval_time)
    
    # Preprocessing
    df = df.set_index("open_date_time")   
    df['close']=df['close'].astype(float)
    df=df['close']
               
    #RSI indicator    
    rsi=round(indicators.rsi(df,14)[-1], 4)
   


    ## telegram bot set
    bot = telegram.Bot(token='1659512846:AAEtRJ-drNZYGWi6-BTonhuZ0LPcBrAqPyU')
    telegram_id = bot.getUpdates()[-1].message.chat.id
    

    # print result
    Present_price = df[-1]


    print(f'바이낸스 {coin_name} 현재가: ', Present_price)
    print(f"Binance {coin_name} RSI: ", rsi)

    if 71 > rsi > 69:
        print('RSI가 70에 가까워졌습니다.')
        # bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n RSI가 70에 가까워졌습니다.')      
        print('\b')
    elif 29 < rsi <32:
        print('RSI가 30에 가까워졌습니다.')
        # bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n RSI가 30에 가까워졌습니다.')
        print('\b')
    else:
        print('아직 관망하세요')
        # bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n 아직 관망하세요')
        print('\b')
    
    if sendTelegram:
        if 71 > rsi > 69:
            bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n {inteval_time} RSI가 70에 가까워졌습니다.')      
            print('\b')
        elif 29 < rsi <32:
            bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n {inteval_time} RSI가 30에 가까워졌습니다.')
            print('\b')
        else:
            # bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n {inteval_time} 아직 관망하세요')
            print('\b')
    
    time.sleep(3)
    

    










