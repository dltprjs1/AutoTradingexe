from binance.client import Client
import Binance_Contidion
import requests
import time
import ccxt
import log
import math
import traceback
import SocketClient
from datetime import datetime


global api_key
global api_secret
global ExChange
api_key = SocketClient.read_ini_file('BinanceAPI','APIKey')
api_secret = SocketClient.read_ini_file('BinanceAPI','APISecret')
binance = ccxt.binance(config={'apiKey': api_key,'secret': api_secret,'enableRateLimit': True,'options': {'defaultType': 'future'}})

def Get_Login_INFO () : 
    client = Client(api_key=api_key, api_secret=api_secret)
    return client


# Binance 계좌 정보 불러오기
def Get_Account_INFO () :
    current_time = get_server_time()
    account_info = Get_Login_INFO().futures_account_balance(timestamp=current_time)
    return account_info


def get_server_time():
    url = "https://api.binance.com/api/v3/time"
    response = requests.get(url)
    server_time = response.json()["serverTime"]
    return server_time


# USDT 자산 확인하기
def Get_Account_USDT () :    
    USDT_balance = None
    for balance in Get_Account_INFO () :
        if balance['asset'] == 'USDT':
            USDT_balance = balance['balance']
            print('현재 자산: ', round(float(USDT_balance),2))
    return round(float(USDT_balance),2)


# 바이낸스 BTC 구매 가능 수량 구하기 Type = 1: 소수점 세 자리로 구매가능 수량 필터 / 99: 소수점 두 자리로 구매가능 수량 필터
def Get_Enable_Order_BTC (Type) :
    Current_USDT = Get_Account_USDT ()
    Current_BTC = Binance_Contidion.Get_BTC_Chart_DATA(99) - 3
    Enable_Order_BTC = ((Current_USDT*0.9) / Current_BTC) * 10                             # 10: Leverage
    EnableOrderQuntity = math.trunc(Enable_Order_BTC*100)/100
    if Type == 99 : 
        Enable_Order_BTC = ((Current_USDT*0.9) / Current_BTC) * 20                         # 20: Leverage
        EnableOrderQuntity = math.trunc(Enable_Order_BTC*10)/10
    OrderInfo = "내자산: ",Current_USDT," / BTC가격: ",Current_BTC," / 주문가능수량: ",Enable_Order_BTC," / 주문수량: ",EnableOrderQuntity
    SocketClient.SendServer("CurrentAccountInfo"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+str(Current_USDT)+'#'+str(Current_BTC)+'#'+str(Enable_Order_BTC)+'#'+str(EnableOrderQuntity))
    log.WriteLog_Future(OrderInfo)
    return EnableOrderQuntity


# 선물 배팅
def Buy_Order(Condition,Type) :
    Get_Account_INFO ()
    EnableOrderQuantity = Get_Enable_Order_BTC(Type)
    if Condition == "L" :
        binance.create_market_buy_order("BTC/USDT",EnableOrderQuantity)
        print("1. 롱 주문")
    elif Condition == "S" :
        binance.create_market_sell_order("BTC/USDT",EnableOrderQuantity)
        print("1. 숏 주문")  


# 매수 조건 초기화
def Check_Reset_Fucture_Condition (Condition,Fucture_Reset) :
    while Fucture_Reset == False :
        try:
            EMA5,EMA10 = Binance_Contidion.Get_BTC_MULTI_EMA_DATA(5,10,1)
            Condition_Reset = Binance_Contidion.Check_Position(EMA5, EMA10)
            if Condition == "L" and Condition_Reset == "S" : 
                ResetCondition = "EMA5: ",EMA5," / EMA10: ",EMA10," / Condition: ",Condition," / Condition_Reset: ",Condition_Reset
                SocketClient.SendServer("ResetCondition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+str(EMA5)+'#'+str(EMA10)+'#'+str(Condition)+'#'+str(Condition_Reset))
                log.WriteLog_Future(ResetCondition)
                Fucture_Reset = True
            if Condition == "S" and Condition_Reset == "L" : 
                ResetCondition = "EMA5: ",EMA5," / EMA10: ",EMA10," / Condition: ",Condition," / Condition_Reset: ",Condition_Reset
                SocketClient.SendServer("ResetCondition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+str(EMA5)+'#'+str(EMA10)+'#'+str(Condition)+'#'+str(Condition_Reset))
                log.WriteLog_Future(ResetCondition)
                Fucture_Reset = True
            print("3. 매수 조건 초기화", Condition, Condition_Reset)
            SocketClient.SendServer("ConditionResetInfo"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+str(Condition)+'#'+str(Condition_Reset)+'#'+str(EMA5)+'#'+str(EMA10))
            time.sleep(0.1)
        except Exception as e:
            exception_message = str(e)
            SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+'Check_Reset_Fucture_Condition: '+exception_message)
    return Fucture_Reset


# 주문 정보 확인하기
def Check_Order() :    
    positions = binance.fetch_positions(symbols=["BTCUSDT"])
    percentage = positions[0]['percentage']
    executed_Quantity = positions[0]['contracts']
    entry_price = positions[0]['entryPrice']
    Side = positions[0]['side']
    Con = "S"
    if Side == 'long' : Con = 'L'
    print("2. 주문정보 = 손익률: ", percentage,"/ 주문수량: ", executed_Quantity,"/ 포지션: ", Con)
    return round(executed_Quantity,3), percentage, entry_price, Con


def Sell_Order_limit(Condition,Qty,Price,Percentage,EntryPrice) :
    print("4. 익절/손절 주문") 
    print(Condition)
    if Condition == "L" :     
        order = binance.create_limit_sell_order("BTC/USDT", Qty, Price)
        SocketClient.SendServer("CancelPosition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+Condition+'#'+str(Percentage)+'#'+str(round(EntryPrice + (EntryPrice*0.004),1))+'#'+str(Check_Order()[3]))
    elif Condition == "S" :
        order = binance.create_limit_buy_order("BTC/USDT", Qty, Price)
        SocketClient.SendServer("CancelPosition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+Condition+'#'+str(Percentage)+'#'+str(round(EntryPrice + (EntryPrice*0.004),1))+'#'+str(Check_Order()[3]))
    return order


def Sell_Order_Market(Condition,Qty,Percentage,EntryPrice) :
    print("4. 익절/손절 주문") 
    print(Condition)
    if Condition == "L" :     
        order = binance.create_market_sell_order("BTC/USDT", Qty)
        SocketClient.SendServer("CancelPosition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+Condition+'#'+str(Percentage)+'#'+str(round(EntryPrice + (EntryPrice*0.004),1)))
    elif Condition == "S" :
        order = binance.create_market_buy_order("BTC/USDT", Qty)
        SocketClient.SendServer("CancelPosition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+Condition+'#'+str(Percentage)+'#'+str(round(EntryPrice + (EntryPrice*0.004),1)))
    return order


def After_Order (Condition) :
    Prices_Setting = 0
    StopRetryOrder = 0                              # 분할 주문(Prices_Setting) = 1: 1차주문 / 2: 2차주문 / 3: 3차주문
    EntryPrice = Check_Order()[2]
    SocketClient.Write_ini_file('BinanceStatus','Status','A')
    SocketClient.Write_ini_file('BinanceStatus','Condition',str(Condition))
    while True :
        try:
            Percentage = Check_Order()[1] # 주문 후 이익률        
            print(Percentage, Condition, Prices_Setting, StopRetryOrder)
            if Percentage is None :
                Fucture_Reset = Check_Reset_Fucture_Condition(Condition,False)          # 롱(L)으로 주문한 경우 EMA5가 EMA10을 데드크로스 해야 Main으로 넘어감 숏(S)일 경우 골든크로스 필요
                if Fucture_Reset : break 
            if Percentage >= 2.0 and Prices_Setting == StopRetryOrder:
                Prices_Setting = 1 
                StopRetryOrder = -1
                Sell_Order_limit(Condition, round(Check_Order()[0],3),round(EntryPrice + (EntryPrice*0.004),1),Percentage,EntryPrice)
            if Percentage <= -4.0 and Prices_Setting == StopRetryOrder :  
                Prices_Setting = -1
                StopRetryOrder = 1
                Sell_Order_Market(Condition, round(Check_Order()[0],3),Percentage,EntryPrice)
            if Prices_Setting != StopRetryOrder and StopRetryOrder < 0 and Percentage <= -4.0  :
                Prices_Setting = StopRetryOrder
                Cancel_Order()
            if Prices_Setting != StopRetryOrder and StopRetryOrder > 0 and Percentage >= 2.0 :
                Prices_Setting = StopRetryOrder
                Cancel_Order()
            SocketClient.SendServer("AfterOrder"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+Condition+'#'+Percentage)
            Check_Position(Prices_Setting)
            time.sleep(0.5)
        except Exception as e:
            exception_message = str(e)
            SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+'After_Order: '+exception_message)

#After_Order('L')
def Cancel_Order () :
    ReadyOrder = binance.fetch_open_orders(symbol="BTC/USDT")
    ReadyOrderID = ReadyOrder[0]['id']
    binance.cancel_order(id=ReadyOrderID, symbol="BTC/USDT")
    
    
def Check_Position (Prices_Setting) :
    if Prices_Setting != 0:
        ReadyOrder = binance.fetch_open_orders(symbol="BTC/USDT")
        Side = ReadyOrder[0]['side']
        print(Side)
        if Prices_Setting > 0 and Side != "sell":
            Cancel_Order()
            Prices_Setting = Prices_Setting * -1
        elif Prices_Setting < 0 and Side != "buy":
            Cancel_Order()
            Prices_Setting = Prices_Setting * -1
    return Prices_Setting