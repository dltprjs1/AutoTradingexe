import pyupbit
import pandas as pd
import math
import log
import SocketClient

def Get_Login_INFO () :
    access_key = SocketClient.read_ini_file('UpbitAPI','apikey')
    secret_key = SocketClient.read_ini_file('UpbitAPI','apisecret')
    Client=pyupbit.Upbit(access_key, secret_key)
    return Client


# 총 보유자산 구하기
def Get_Upbit_Account () :                                                                                      
    previous = int(round(Get_Login_INFO().get_amount('ALL'))) + int(round(Get_Login_INFO().get_balance(ticker="KRW")))
    return previous


# 현재 원화 잔고 구하기
def Get_Account_KRW () :                                                                                    
    currentcoin = pd.DataFrame(Get_Login_INFO().get_balances())
    my_money = float(currentcoin.iloc[0,1])                                                                      
    return my_money


# 주문 가능 개수 구하기
def Get_Orderable_quantity (symbol) :
    OrderCount=math.trunc(math.trunc(Get_Account_KRW())/Get_Asking_Price(symbol,1))
    return OrderCount


# 프로그램 실행 시 매수한 코인이 있는지 확인
def Check_Bought_Coin() :
    Return = False
    BoughtCoin = ''
    for i in range(len(pd.DataFrame(Get_Login_INFO().get_balances()))) :
        UpbitExistCoin = pd.DataFrame(Get_Login_INFO().get_balances()).iloc[i,3]
        print(pd.DataFrame(Get_Login_INFO().get_balances()))
        if UpbitExistCoin != '0' and float(pd.DataFrame(Get_Login_INFO().get_balances()).iloc[i,3]) * float(pd.DataFrame(Get_Login_INFO().get_balances()).iloc[i,1]) >= 500000 :
            BoughtCoin = 'KRW-'+pd.DataFrame(Get_Login_INFO().get_balances()).iloc[i,0]
            BoughtCoinCount = Get_Login_INFO().get_balance(BoughtCoin)                      # 매수한 개수
            Return = Check_Coin_Info(BoughtCoin,BoughtCoinCount)
            CheckBooghtInfo = "결과: ",Return," / 코인명: ",BoughtCoin," / 주문수량: ",BoughtCoinCount
            log.WriteLog_Trading(CheckBooghtInfo)
    return Return,BoughtCoin

def Check_Coin_Info (BoughtCoin,BoughtCoinCount) :
    Return = False
    CoinPrice = Get_Asking_Price(BoughtCoin,99) 
    if CoinPrice * BoughtCoinCount > 500000 : Return = True
    return Return
   

# 첫번째 매수 호가 구하기 Type = 99 : 첫번째 매도 호가
def Get_Asking_Price (symbol,Type) :
    AskingPrice=pd.DataFrame(pd.DataFrame(pyupbit.get_orderbook(ticker = symbol)['orderbook_units']))['bid_price'][0]
    if Type == 99 : AskingPrice=pd.DataFrame(pd.DataFrame(pyupbit.get_orderbook(ticker = symbol)['orderbook_units']))['ask_price'][0]
    return AskingPrice
