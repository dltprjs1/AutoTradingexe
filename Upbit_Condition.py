import time
import pyupbit
import Upbit_Login_INFO
import talib
import log


# 모든 코인 불러오기
def Get_All_Coin () :
    tickers = pyupbit.get_tickers(fiat='KRW',is_details=True)
    return tickers


# 거래대금 평균 구하기
def Get_Average_Transaction_Amount (avg_volume_all) :
    print('거래대금 평균 구하는 중...')
    for symbol in Get_All_Coin () :
        volume = int(pyupbit.get_ohlcv(symbol['market'], interval="day",count=1)['value'].iloc[0])
        avg_volume_all = (avg_volume_all+volume) / len(symbol)
        time.sleep(0.01)
    return avg_volume_all


# 비트코인 추세 확인
def Check_First_BTC_Condition (symbol,minute) :
    Return = False
    K,D = Get_Ticker_StochRSI_DATA(symbol,minute)
    EMA50,EMA100,Upward_Trend = Get_Ticker_EMA_DATA(symbol,minute)
    print('Minute: ',minute,' / K : ',K,' / D : ',D,' / EMA50 : ',EMA50,' / EMA100 : ',EMA100)
    if (K - D <= 8) or (EMA50 < EMA100) or (Upward_Trend == False) or (D > 50): Return = False
    else :         
        CurrentCondition ="Symbol: ",symbol, " / K : ",K," / D : ",D," / EMA50 : ",EMA50," / EMA100 : ",EMA100," / Minute: ",minute
        log.WriteLog_Trading(CurrentCondition)
        Return = True
    return Return


# 매수 조건 확인
def Check_Final_Condition (symbol,All_Coin_Average_Transaction_Amount,minute) :
    Return = False
    K,D = Get_Ticker_StochRSI_DATA(symbol,minute)
    EMA50,EMA100,Upward_Trend = Get_Ticker_EMA_DATA(symbol,minute)
    volume = int(pyupbit.get_ohlcv(symbol, interval="day",count=1)['value'].iloc[0])
    print("Symbol: ",symbol, " / K : ",K," / D : ",D," / EMA50 : ",EMA50," / EMA100 : ",EMA100," / Volume: ",volume, " / AVGVolume: ",All_Coin_Average_Transaction_Amount)
    if (volume < All_Coin_Average_Transaction_Amount) or (Condition_1(symbol) == False) or (symbol == "KRW-DOGE") or (symbol == "KRW-XRP") or (K - D <= 8) or (EMA50 < EMA100) or (Upward_Trend == False) or (D > 20): Return = False
    else : 
        CurrentCondition ="Symbol: ",symbol, " / K : ",K," / D : ",D," / EMA50 : ",EMA50," / EMA100 : ",EMA100," / Volume: ",volume, " / AVGVolume: ",All_Coin_Average_Transaction_Amount
        log.WriteLog_Trading(CurrentCondition)
        Return = True
    return Return


# StochRSI 데이터 추출
def Get_Ticker_StochRSI_DATA (symbol,minute) :
    df = pyupbit.get_ohlcv(symbol, interval = minute)
    rsi = talib.RSI(df['close'], timeperiod=14)
    stochrsi  = (rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min())
    K = stochrsi.rolling(5).mean()
    D = K.rolling(5).mean()
    return K.iloc[-2]*100 ,D.iloc[-2]*100


# TALIB을 이용한 EMA 데이터 추출
def Get_Ticker_EMA_DATA (symbol,minute) :
    df = pyupbit.get_ohlcv(symbol, interval = minute)
    EMA50 = talib.EMA(df['close'], timeperiod=50)
    EMA100 = talib.EMA(df['close'], timeperiod=100)
    UpWard_Trend = Check_Upward_Trend_Line(EMA50)
    return EMA50[-2], EMA100[-2], UpWard_Trend


# 상승추세 확인
def Check_Upward_Trend_Line (EMA50) :
    Return = False
    if EMA50[-11] < EMA50[-1] : Return = True
    return Return


# 주문가능 개수 10개 초과 또는 1500000개 미만 거르기
def Condition_1 (Symbol) :
    Return = False
    if Upbit_Login_INFO.Get_Orderable_quantity (Symbol) > 10 and Upbit_Login_INFO.Get_Orderable_quantity (Symbol) < 1500000 : Return = True
    return Return






