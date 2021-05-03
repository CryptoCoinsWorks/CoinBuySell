import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *
from binance.client import Client
import time
import datetime as dt
import pandas as pd
import telegram
import os 


def resource_path(relative_path): 

    """ Get absolute path to resource, works for dev and for PyInstaller """ 
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) 
    return os.path.join(base_path, relative_path)

form = resource_path('Coinalarm.ui')


client=Client()


form_class = uic.loadUiType(form)[0]

#you can turn or off to writedown here 'True = on' and 'False = off'
sendTelegram = False
telegram_token = 'your telegram token' 

# telegram bot set
bot = telegram.Bot(token=telegram_token)
telegram_id = bot.getUpdates()[-1].message.chat.id

# set coin name and interval time
tickers = ["BTCUSDT", 'ETHUSDT']
inteval_time = '15m'


class Worker(QThread):
    finished = pyqtSignal(dict)
    
    def run(self):
        while True:
            data = {}

            for ticker in tickers:
                data[ticker] = self.get_market_infos(ticker, inteval_time)


            self.finished.emit(data)
            # self.tele_text(data)

            time.sleep(2)


    def get_market_infos(self, symbol, interval):

        try:

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

            df=get_historical_ohlc_data(symbol, past_days=None, interval = None)
    
            # Preprocessing
            df = df.set_index("open_date_time")   
            df['close']=df['close'].astype(float)
            df=df['close']

            #rsi와 현재가 출력

            def rsi(ohlc: pd.DataFrame, period: int = 14):
    
                delta = ohlc.diff()
    
                up, down = delta.copy(), delta.copy()
                up[up < 0] = 0
                down[down > 0] = 0
    
                _gain = up.ewm(com=(period - 1), min_periods=period).mean()
                _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    
                RS = _gain / _loss
                return pd.Series(100 - (100 / (1 + RS)), name="RSI")

            rsi=round(rsi(df,14)[-1], 4)
            Present_price = df[-1]

            return Present_price, rsi
        except:
            return None, None
        
class MyWindow(QMainWindow, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.worker = Worker()
        self.worker.finished.connect(self.update_table_widget)
        self.worker.finished.connect(self.tele_text)
        self.worker.start()
        

        self.checkBox_1.stateChanged.connect(self.tele_text)
        self.checkBox_2.stateChanged.connect(self.setOnTop)

        self.dialog = QDialog()

        # self.button = QPushButton('텔레그램 토큰 입력', self)
        self.pushButton.clicked.connect(self.token_window)

    def token_window(self):
        self.dialog.setWindowTitle('텔레그램 토큰 입력')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.show()

    def tele_text(self, data):
        if self.checkBox_1.isChecked():

            try:
                for ticker, infos in data.items():
                    index = tickers.index(ticker)
                    rsi = infos[1]

                    if 71 > rsi > 69:
                        # print( f' 바이낸스 {tickers[index]} 현재가:{infos[index]} \n RSI: {infos[index]} \n RSI가 70에 가까워졌습니다.')
                        bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {tickers[index]} 현재가:{infos[index]} \n RSI: {infos[index]} \n RSI가 70에 가까워졌습니다.')      
                    
                    elif 29 < rsi <32:
                    # print(f' 바이낸스 {tickers[index]} 현재가:{infos[index]} \n RSI: {infos[index]} \n RSI가 30에 가까워졌습니다.')
                        bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {tickers[index]} 현재가:{infos[index]} \n RSI: {infos[index]} \n RSI가 30에 가까워졌습니다.')
                    
                    # else:
                    #     # print(f' 바이낸스 {tickers[index]} 현재가:{infos[index]} \n RSI: {infos[index]} \n 아직 관망하세요')
                    #     bot.sendMessage(chat_id = telegram_id, text = f' 바이낸스 {tickers[index]} 현재가:{infos[index]} \n RSI: {infos[index]} \n 아직 관망하세요')
                    
            except:
                pass
        else:
            pass
    
    def setOnTop(self):

        if self.checkBox_2.isChecked():
            self.window().setWindowFlags(
                self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.window().setWindowFlags(
                self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        self.window().show()


    @pyqtSlot(dict)
    def update_table_widget(self, data):
        try:
            for ticker, infos in data.items():
                index = tickers.index(ticker)
                
 
                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))

        except:
            pass
 
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()