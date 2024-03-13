from datetime import datetime
import Binance_Order_INFO
import time
import Binance_Contidion
import SocketClient
import log
import traceback
import Upbit_AllCoinBuy
import threading

def Status_Check(): # Status = B: Before Order / A: After Order
    Status = SocketClient.read_ini_file('BinanceStatus','status')
    Condition = SocketClient.read_ini_file('BinanceStatus','condition')
    if Status == 'A': Binance_Order_INFO.After_Order(Condition)
        

def Searching_Transaction_Condition_BTC() :
    Status_Check()    
    while True :        
        try :             
            CurrentPrice =  Binance_Contidion.Get_BTC_Chart_DATA(99)
            EMA200N = Binance_Contidion.Get_BTC_EMA_DATA(200,"now")
            EMA5,EMA10,EMA200 = Binance_Contidion.Get_BTC_TRIPLE_EMA_DATA(5,10,200,"past")
            MACD12,MACD26 = Binance_Contidion.Get_BTC_MACD_DATA(12,26,14,"past")
            CCI,CCIN = Binance_Contidion.Get_BTC_CCI_DATA (200)
            Condition_1 = Binance_Contidion.Check_Position(CurrentPrice,EMA200N)
            Condition_2 = Binance_Contidion.Check_Position(EMA5,EMA200)                                                 # EMA5 <> EMA200
            Condition_3 = Binance_Contidion.Check_Position(EMA5,EMA10)                                                  # EMA5 <> EMA10
            Condition_4 = Binance_Contidion.Check_Position(MACD12,0)                                                    # MACD12 <> 0
            Condition_5 = Binance_Contidion.Check_Position(MACD12,MACD26)                                               # MACD12 <> MACD26
            Condition_6 = Binance_Contidion.Check_Position_CCI(CCI,100)                                                 # CCI > 100 OR CCI < -100
            if Condition_6 == 'H': Condition_6 = Binance_Contidion.Check_Position_CCI(CCIN,115)                         # CCI(N) > 115 OR CCI < -115          
                             
            CurrentCondition = "현재가: ",CurrentPrice," / EMA5: ",EMA5," / EMA10: ",EMA10," / EMA200: ",EMA200," / EMA200N: ",EMA200N," / MACD12: ",MACD12," / MACD26: ",MACD26," / CCI: ",CCI," / CCIN: ",CCIN
            SocketClient.SendServer("Condition"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+Condition_1+'#'+Condition_2+'#'+Condition_3+'#'+Condition_4+'#'+Condition_5+'#'+Condition_6+'#'
                                    +str(CurrentPrice)+'#'+str(EMA5)+'#'+str(EMA10)+'#'+str(EMA200)+'#'+str(EMA200N)+'#'+str(MACD12)+'#'+str(MACD26)+'#'+str(CCI)+'#'+str(CCIN))
            values_to_check = [Condition_1, Condition_2, Condition_3, Condition_4, Condition_5, Condition_6]
            print(values_to_check)
            log.WriteLog_Future(values_to_check)
            log.WriteLog_Future(CurrentCondition)
            result = Binance_Contidion.are_all_equal(values_to_check)
            SocketClient.Write_ini_file('BinanceStatus','Status','B')
            SocketClient.Write_ini_file('BinanceStatus','Condition',str(Condition_6))
            if result:
                Binance_Order_INFO.Get_Login_INFO().futures_change_leverage(symbol = 'BTCUSDT', leverage = 10)             # 레버리지 설정
                Binance_Order_INFO.Buy_Order(Condition_6,1)                                                                # 시장가 주문하기 = Condition_2 : "L"일 경우 롱 / Condition_2 : "S"일 경우 숏
                Binance_Order_INFO.After_Order(Condition_6)                                                                # 주문 후 로직
                time.sleep(1)
            else: continue
            
        except Exception as e :
            exception_message = str(e)
            print(exception_message)
            SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+'Searching_Transaction_Condition_BTC: '+exception_message)

            if "-1111" in exception_message:
                Binance_Order_INFO.Get_Login_INFO().futures_change_leverage(symbol = 'BTCUSDT', leverage = 20)               # 레버리지 설정
                Binance_Order_INFO.Buy_Order(Condition_6,99)                                                                 # 시장가 주문하기 = Condition_2 : "L"일 경우 롱 / Condition_2 : "S"일 경우 숏
                Binance_Order_INFO.After_Order(Condition_6)                                                                  # 주문 후 로직
            else: print("Error message does not contain -1111")
                
                
AllCoinTrading = threading.Thread(target=Upbit_AllCoinBuy.Main)
AllCoinTrading.start()

Searching_Transaction_Condition_BTC()




# 주문 조건 초기화 로직 다시 짜기
# Main 함수 실행 가능토록 로직 다시 짜기