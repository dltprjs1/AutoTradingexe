import talib
import pandas as pd
import ccxt


# TALIB에 적용할 데이터 추출  CurrentPrice : type = 99
def Get_BTC_Chart_DATA (Type) :
    binance = ccxt.binance(config={'options': {'defaultType': 'future'}})
    btc_ohlcv = binance.fetch_ohlcv("BTC/USDT",'30m', limit=500)
    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    if Type == 99 : df = df['close'][len(df['close'])-1]
    return df


# TALIB을 이용한 EMA 데이터 추출
def Get_BTC_EMA_DATA (Period,Type) :
    BTC_Price_Info = Get_BTC_Chart_DATA(1)
    ema = talib.EMA(BTC_Price_Info['close'], timeperiod=Period)[len(BTC_Price_Info['close'])-2]          # 30분 전
    if Type == "now" : ema = talib.EMA(BTC_Price_Info['close'], timeperiod=Period)[len(BTC_Price_Info['close'])-1]                   # 현재가    [len(close_prices)-1] == [-1]
    print("EMA: ",round(float(ema),2))
    return round(float(ema),2)


# TALIB을 이용한 MULTI_EMA 데이터 추출
def Get_BTC_MULTI_EMA_DATA (Period_1,Period_2,Type) :
    BTC_Price_Info = Get_BTC_Chart_DATA(1)
    ema_1 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_1)[len(BTC_Price_Info['close'])-2]                   # 30분 전
    ema_2 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_2)[len(BTC_Price_Info['close'])-2]                   # 30분 전
    if Type == "now" : 
        ema_1 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_1)[len(BTC_Price_Info['close'])-1]                              # 현재가    [len(close_prices)-1] == [-1]
        ema_2 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_2)[len(BTC_Price_Info['close'])-1]                              # 현재가    [len(close_prices)-1] == [-1]
    print("EMA_1: ",round(float(ema_1),2)," EMA_2: ", round(float(ema_2),2))
    return round(float(ema_1),2), round(float(ema_2),2)


# TALIB을 이용한 TRIPLE_EMA 데이터 추출
def Get_BTC_TRIPLE_EMA_DATA (Period_1,Period_2,Period_3,Type) :
    BTC_Price_Info = Get_BTC_Chart_DATA(1)
    ema_1 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_1)[len(BTC_Price_Info['close'])-2]                   # 30분 전
    ema_2 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_2)[len(BTC_Price_Info['close'])-2]                   # 30분 전
    ema_3 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_3)[len(BTC_Price_Info['close'])-2]                   # 30분 전
    if Type == "now" : 
        ema_1 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_1)[len(BTC_Price_Info['close'])-1]                              # 현재가    [len(close_prices)-1] == [-1]
        ema_2 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_2)[len(BTC_Price_Info['close'])-1]                              # 현재가    [len(close_prices)-1] == [-1]
        ema_3 = talib.EMA(BTC_Price_Info['close'], timeperiod=Period_3)[len(BTC_Price_Info['close'])-1]                              # 현재가    [len(close_prices)-1] == [-1]
    print("EMA5: ",round(float(ema_1),2), " EMA10: ", round(float(ema_2),2), " EMA200: ", round(float(ema_3),2))
    return round(float(ema_1),2), round(float(ema_2),2), round(float(ema_3),2)


# TALIB을 이용한 MACD 데이터 추출
def Get_BTC_MACD_DATA (FastPeriod,SlowPeriod,SignalPeriod,Type) :
    BTC_Price_Info = Get_BTC_Chart_DATA(1)
    macd, signal, line = talib.MACD(BTC_Price_Info['close'], fastperiod=FastPeriod, slowperiod=SlowPeriod, signalperiod=SignalPeriod)
    macd = round(float(macd[len(macd)-2]),2)
    signal = round(float(signal[len(signal)-2]),2)
    if Type == "now" : 
        macd, signal = talib.MACD(BTC_Price_Info['close'], fastperiod=FastPeriod, slowperiod=SlowPeriod, signalperiod=SignalPeriod)
        macd = round(float(macd[-1]),2)
        signal = round(float(signal[-1]),2)
    print("MACD12: ", macd, " MACD26: ",signal)
    return macd,signal


# TALIB을 이용한 CCI 데이터 추출
def Get_BTC_CCI_DATA (Period) :
    BTC_Price_Info = Get_BTC_Chart_DATA(1)
    cci = talib.CCI(BTC_Price_Info['high'], BTC_Price_Info['low'], BTC_Price_Info['close'], timeperiod=Period)
    print("CCI: ", round(float(cci[len(cci)-2]),2), " CCIN: ", round(float(cci[len(cci)-1]),2))
    return round(float(cci[len(cci)-2]),2),round(float(cci[len(cci)-1]),2)


# L(Long) / S(Short) 확인
def Check_Position (Condition_1,Condition_2) :
    Return = "S"
    if Condition_1 > Condition_2 : Return = "L"
    return Return


# CCI L(Long) / S(Short) 확인
def Check_Position_CCI (Condition,Signal) :
    if Condition < Signal * -1 : Return = "S"         
    if Condition > Signal * 1 : Return = "L"
    if (Condition < Signal * 1) and (Condition > Signal * -1)  : Return = "H"
    return Return


# 포지션 확인
def Check_Condition (Condition_1,Condition_2) :
    Return = True
    if Condition_1 != Condition_2 : 
        Return = False
    return Return


def are_all_equal(values):
    return all(x == values[0] for x in values)