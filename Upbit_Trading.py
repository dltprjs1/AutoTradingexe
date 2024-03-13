import Upbit_Condition
import Upbit_Order_INFO
import Upbit_Login_INFO
import time
import log


def Searching_Transaction_Condition_Coin () :    
    All_Coin_Average_Transaction_Amount = Upbit_Condition.Get_Average_Transaction_Amount(0)
    if Upbit_Login_INFO.Check_Bought_Coin()[0] : Upbit_Order_INFO.After_Order_Sell(Upbit_Login_INFO.Check_Bought_Coin()[1])
    while True :  
        try :            
            BTC_Trend_Check()
            for symbol in Upbit_Condition.Get_All_Coin () :
                print(symbol['market'])
                if symbol['market_warning'] == 'NONE' :                                                         # 유의종목 continue
                    pass
                    if Upbit_Condition.Check_Final_Condition(symbol['market'],All_Coin_Average_Transaction_Amount,'minute15') :                    
                        CheckBooghtInfo = "매수: ",symbol['market']
                        log.WriteLog_Trading(CheckBooghtInfo)                        
                        Upbit_Order_INFO.Buy(symbol['market'], 7, 1)
                        All_Coin_Average_Transaction_Amount = Upbit_Condition.Get_Average_Transaction_Amount(0)
                    time.sleep(0.1)
        except Exception as e:
            print(f"에러 메시지: {e}")


def BTC_Trend_Check():
    Minute_List = ['minute15','minute30','minute60','minute240']
    Return = False
    while True:
        try: 
            if Return : break
            for i in range(len(Minute_List)):
                arg = Minute_List[i]
                if Upbit_Condition.Check_First_BTC_Condition ('KRW-BTC',arg):
                    Return = True
                    break
                time.sleep(0.1)
        except Exception as e:
            print(f"에러 메시지: {e}")