import pyupbit
import time
import pandas as pd
import datetime
import Upbit_Login_INFO
import SocketClient
from datetime import datetime

bool = ""
check = ""
checkcount = ""
checktime = ""
buytime = ""
outstandingcanceltime = ""
selltime = ""

def Get_All_Coin() :
    tickers = pyupbit.get_tickers(fiat='KRW',is_details=True)
    return tickers,len(tickers)


def Main() :
    try :
        CheckIni()
        print(bool,check,checkcount,checktime,buytime,outstandingcanceltime,selltime)
        while True :            
            current_time = datetime.now()
            Time = current_time.strftime("%H%M%S")
            print("Current time :",Time)
            if Time == checktime and check == 'Y' : Check()
            elif Time == buytime and bool == 'Y' : Buy()
            elif Time == outstandingcanceltime and bool == 'Y' : Outstanding_Orders_Cancel()
            elif Time == selltime : Sell()
            time.sleep(1)
    except Exception as e:
        print(e)
        exception_message = str(e)
        SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'TRADE'+'#'+'All_Coin_Buy: '+exception_message)


def CheckIni() :
    global bool 
    global check
    global checkcount
    global checktime
    global buytime
    global outstandingcanceltime
    global selltime
    
    bool = SocketClient.read_ini_file('AllCoinBuy','bool')
    check = SocketClient.read_ini_file('AllCoinBuy','check')
    checkcount = SocketClient.read_ini_file('AllCoinBuy','checkcount')
    checktime = SocketClient.read_ini_file('AllCoinBuy','checktime')
    buytime = SocketClient.read_ini_file('AllCoinBuy','buytime')
    outstandingcanceltime = SocketClient.read_ini_file('AllCoinBuy','outstandingcanceltime')
    selltime = SocketClient.read_ini_file('AllCoinBuy','selltime')
    
def Check() :
    check = 0
    try :            
        for symbol in Get_All_Coin ()[0] :
            if symbol['market_warning'] == 'NONE' : 
                pass
                print(symbol['market'])
                Coin = pyupbit.get_ohlcv(symbol['market'], interval="day",count=1)
                Open = float(Coin['open'].iloc[0])
                Close = float(Coin['close'].iloc[0])
                Percent = (Close - Open) / Open * 100
                if Percent > 0 : 
                    check = check +1
                else :
                    check = check -1
                print('Open: ',Open,' Close: ',Close,' Percent: ',Percent,' check: ',check)
            time.sleep(0.4)
        SocketClient.Write_ini_file('AllCoinBuy','bool','Y')
        if check < int(checkcount) : SocketClient.Write_ini_file('AllCoinBuy','bool','N')            
        CheckIni()
    except Exception as e:
        exception_message = str(e)
        SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'TRADE'+'#'+'All_Coin_Buy: '+exception_message)


def Buy() :
    try :            
        Price = int(Upbit_Login_INFO.Get_Upbit_Account() / Get_All_Coin()[1]) 
        print('One Coin per Prices: ',Price)
        for symbol in Get_All_Coin ()[0] :
            if symbol['market_warning'] == 'NONE' : 
                pass
                Quantity = round(Price/Upbit_Login_INFO.Get_Asking_Price(symbol['market'],1),2)
                if int(Quantity) > 0 :
                    print(symbol['market'])
                    print('BidPrice: ',Upbit_Login_INFO.Get_Asking_Price(symbol['market'],1))
                    print('AskingPrice: ',Upbit_Login_INFO.Get_Asking_Price(symbol['market'],99))
                    print('Quantity: ',Quantity)
                    Upbit_Login_INFO.Get_Login_INFO().buy_limit_order(symbol['market'],Upbit_Login_INFO.Get_Asking_Price(symbol['market'], 1),Quantity)
            time.sleep(0.4)
    except Exception as e:
        exception_message = str(e)
        SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'TRADE'+'#'+'All_Coin_Buy: '+exception_message)


def Outstanding_Orders_Cancel() :
    try:
        Client = Upbit_Login_INFO.Get_Login_INFO()
        for symbol in Get_All_Coin ()[0] :
            print(symbol['market'])
            outstanding_order_uuid = pd.DataFrame(Client.get_order(symbol['market']))
            if outstanding_order_uuid.empty == False :
                outstanding_order = outstanding_order_uuid['uuid'][0]
                Client.cancel_order(outstanding_order)
            time.sleep(0.4)
    except Exception as e:
        exception_message = str(e)
        SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'TRADE'+'#'+'All_Coin_Buy: '+exception_message)


def Sell() :
    BalanceInfo = pd.DataFrame(Upbit_Login_INFO.Get_Login_INFO().get_balances())
    for i in range(len(BalanceInfo)) :
        Price = float(BalanceInfo.iloc[i,3])
        if (Price != 0) and ('ASTR' not in BalanceInfo.iloc[i,0]) :
            Coin = 'KRW-'+BalanceInfo.iloc[i,0]
            Quantity = BalanceInfo.iloc[i,1]
            print('CoinName: ',Coin, 'Quantity: ',Quantity)
            Upbit_Login_INFO.Get_Login_INFO().sell_market_order(Coin, Quantity)
        time.sleep(0.4)
