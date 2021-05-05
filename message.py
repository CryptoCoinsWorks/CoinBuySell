import telegram



def tele_message(rsi):
    if sendTelegram:
    if 71 > rsi > 69:
        bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n {inteval_time} RSI가 70에 가까워졌습니다.')      
        print('\b')
    elif 29 < rsi <32:
        bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n {inteval_time} RSI가 30에 가까워졌습니다.')
        print('\b')
    else:
        bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {coin_name} 현재가:{Present_price} \n RSI: {rsi} \n {inteval_time} 아직 관망하세요')
        print('\b')
    
time.sleep(3)