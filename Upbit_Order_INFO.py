import Upbit_Login_INFO
import time
import pandas as pd
import numpy as np
import Upbit_Condition
import pyupbit
import Database
import log

my_list = ['minute30', 'minute60', 'minute240']

# 매수하기
def Buy (symbol, OrderableCount, Type):
    print('3. 매수하기')
    Upbit_Login_INFO.Get_Login_INFO().buy_limit_order(symbol,Upbit_Login_INFO.Get_Asking_Price(symbol, 1),Upbit_Login_INFO.Get_Orderable_quantity(symbol)/OrderableCount)    
    five_minute_function(symbol,Type)


# 첫번째 호가 주문 후 5분 뒤 주문 취소
def five_minute_function(symbol,Type):
    EndTime = time.time() + 300
    print('4. 첫번째 호가 주문 후 5분 뒤 주문 취소')
    while time.time() < EndTime :       
        time.sleep(1)
    Additional_Order_Cancel(symbol,'bid')
    if Type == 99 : Additional_Order_Cancel(symbol,'ask')        
    if Upbit_Login_INFO.Check_Bought_Coin()[0] : 
        After_Order_Sell(Upbit_Login_INFO.Check_Bought_Coin()[1])

       
# 매수 후 로직(매도)
def After_Order_Sell(Symbol) :
    All_Coin_Average_Transaction_Amount = Upbit_Condition.Get_Average_Transaction_Amount(0)    
    while Upbit_Login_INFO.Get_Account_KRW() <  Upbit_Login_INFO.Get_Upbit_Account() - 100000 :
        try :
            BoughtCoinName = ""
            Orderedcoin = pd.DataFrame(Upbit_Login_INFO.Get_Login_INFO().get_balances())                    # 내가 매수한 코인의 정보(df)
            print('매수한 코인 정보')
            print(Orderedcoin)
            for i in range(len(Orderedcoin)) :
                if Symbol == 'KRW-'+Orderedcoin.iloc[i,0] :
                    BoughtCoinName = 'KRW-'+Orderedcoin.iloc[i,0]                                           # 매수 코인 이름
                    BoughtcoinCount = Upbit_Login_INFO.Get_Login_INFO().get_balance(BoughtCoinName)         # 매수한 개수
                    BoughtCoinPrice = (np.ceil(float(Orderedcoin.iloc[i,3]) * 1000)) / 1000                 # 매수할 때 코인 금액
                    CurrentCoinPrice = pyupbit.get_ohlcv(BoughtCoinName, interval="minute60",count=1)['close'][0]
            if BoughtCoinName == "" : continue
            TradingInfo = "매수코인: ",BoughtCoinName," / 주문개수: ",BoughtcoinCount," / 주문금액: ",BoughtCoinPrice," / 현재금액: ",CurrentCoinPrice," / 퍼센트: ",Check_Sell_Order (BoughtCoinPrice, CurrentCoinPrice)[1]
            log.WriteLog_Trading(TradingInfo)
            After_Order_Buy(BoughtCoinName,All_Coin_Average_Transaction_Amount)
            if Check_Sell_Order(BoughtCoinPrice, CurrentCoinPrice)[0] :
                Upbit_Login_INFO.Get_Login_INFO().sell_limit_order(BoughtCoinName, Upbit_Login_INFO.Get_Asking_Price(BoughtCoinName,99), BoughtcoinCount)
            time.sleep(0.1)
        except Exception as e :
            Database.TEST_SAVE_ERROR_INFO (f"에러 메시지: {e}")


# 매도가에 도달 했는지 확인
def Check_Sell_Order (BoughtCoinPrice, CurrentCoinPrice) :
    Return = False
    Check = ((CurrentCoinPrice - BoughtCoinPrice) / BoughtCoinPrice) * 100
    if Check >= 1 : Return = True
    return Return, Check


# 매수 조건 확인(매수 또는 추가매수)
def After_Order_Buy(symbol,All_Coin_Average_Transaction_Amount) :
    global my_list
    for i in my_list:
        if Upbit_Condition.Check_Final_Condition (symbol,All_Coin_Average_Transaction_Amount,i) :
            my_list.remove(i)
            CurrentPrice = Upbit_Login_INFO.Get_Account_KRW ()
            OrderCount = CurrentPrice[0]
            Buy(symbol, OrderCount,99)


# 지정가 추가 매수 / 매도 취소  Type = bid : 매수 / ask : 매도
def Additional_Order_Cancel (BoughtCoinName,Type) :
    WatingOrder = pd.DataFrame(Upbit_Login_INFO.Get_Login_INFO().get_order(BoughtCoinName))
    print("취소 안하나??")
    for i  in range(len(WatingOrder)) : 
        i = 0
        order_uuid=Upbit_Login_INFO.Get_Login_INFO().get_order(BoughtCoinName)                #내가 지정가 매도/매수한 uuid구하기
        order_val =order_uuid[i]                                                              #1번째 uuid
        if order_val['side'] ==Type:                                                          #현재 지정가매수/매도가 3개이상이고 매도지정가가 있을경우
            order_uuid1 = order_val['uuid']                                                   # 지정가 매도 uuid를 order_uuid1에 저장
            Upbit_Login_INFO.Get_Login_INFO().cancel_order(order_uuid1)

