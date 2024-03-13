from datetime import datetime
import pymssql
import socket

def DB_Connection(database_Name):
    database = database_Name
    user = 'dltprjs1'
    password = '@@Cwoo7848'
    conn = pymssql.connect("39.115.190.122:1234",user,password,database)
    return conn


def DB_Select(conn,sql,values):
    cursor = conn.cursor()
    if values != "": cursor.execute(sql,(values))
    else: cursor.execute(sql)
    return cursor


def DB_Execute(conn,sql,values):
    cursor = conn.cursor()
    cursor.execute(sql,(values))


def DB_Connection_Close(conn):
    conn.commit()
    conn.close()


def Get_My_IP () :
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def Get_Date_Time_Number () :
    DateTimeNumber = ""
    return DateTimeNumber

# 선물 거래 조건 업데이트 (코인명 / 거래구분 / 레버리지 / First_EMA / Second_EMA / Third_EMA / MACD_Fast_Period / MACD_Slow_Period / MACD_Signal_Period / CCI_Period  /스토캐스틱 / RSI / Trix)
# def Update_Fucture_Condition () :
#     conn = DB_Connection('AUTOCONDITION')
#     sql = 'UPDATE CONDITION SET INTERVAL=%s ,PURCHASE=%d ,AMOUNT=%d, RETRY=%d,WHERE IP = %d'
#     values = (entry_Process_r_1.get(),entry_K_r_1.get(),entry_D_r_1.get(),MY_IP)
#     DB_Execute(conn,sql,values)
#     DB_Connection_Close(conn)

    
# 구매 주문 시 조건 저장하기 (날짜 / 시간 / 거래구분 / 현재가 / EMA5 / EMA10 / EMA200 / EMA200(N) / MACD12 / MACD26 / CCI / CCI(N) / 포지션 / IP)
def Save_Trading_Order_Condition_Info (Type,CurrentPrice,FirstEMA,SecondEMA,ThirdEMA,FourthEMA,FirstMACD,SecondMACD,FirstCCI,SecondCCI,Position) :
    conn = DB_Connection('Fucture')
    #sql = 'INSERT INTO TRANS_INFO VALUSE(COIN_NAME=%s,TYPE=%s,TRANSACTION_PRICE=%d,AMOUNT=%d,PROFIT_LOSS=%d) WHERE IP=%s'
    sql = 'INSERT INTO Save_Trading_Order_Condition_Info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (Get_Date_Time_Number_TEST(),Type,CurrentPrice,FirstEMA,SecondEMA,ThirdEMA,FourthEMA,FirstMACD,SecondMACD,FirstCCI,SecondCCI,Position,Get_My_IP())
    DB_Execute(conn,sql,values)
    DB_Connection_Close(conn)


# 구매 주문 내역 저장하기 (날짜 / 시간 / 거래구분 / 포지션 / 코인명 / 주문금액 / 주문수량 / 상태 / 1차 익절가 / 2차 익절가 / 3차 익절가 / 1차 손절가 / 2차 손절가 / 3차 손절가 / IP)
def Save_Trading_Buy_Info (Type,Position,CoinName,OrderPrice,OrderQuantity,Status,FirstBenefitPrice,SecondBenefitPrice,ThirdBenefitPrice,FirstLossPrice,SecondLossPrice,ThirdLossPrice) :
    conn = DB_Connection('Fucture')
    sql = 'INSERT INTO Save_Trading_Buy_Info VALUSE(DateTimeNumber=%s,Type=%s,Position=%s,Name=%s,OrderPrice=%s,OrderQuantity=%s,Status=%s,FirstBenefitPrice=%s,SecondBenefitPrice=%s,ThirdBenefitPrice=%s,FirstLossPrice=%s,SecondLossPrice=%s,ThirdLossPrice=%s,IP=%s)'
    values = (Get_Date_Time_Number(),Type,Position,CoinName,OrderPrice,OrderQuantity,Status,FirstBenefitPrice,SecondBenefitPrice,ThirdBenefitPrice,FirstLossPrice,SecondLossPrice,ThirdLossPrice,Get_My_IP())
    DB_Execute(conn,sql,values)
    DB_Connection_Close(conn)


# 판매 주문 내역 저장하기 (날짜 / 시간 / 거래구분 / 포지션 / 코인명 / 주문금액 / 주문수량 / IP)
def Save_Trading_Sell_Info (Type,Position,CoinName,OrderPrice,OrderQuantity) :
    conn = DB_Connection('Fucture')
    sql = 'INSERT INTO Save_Trading_Sell_Info VALUSE(DateTimeNumber=%s,Type=%s,Position=%s,Name=%s,OrderPrice=%s,OrderQuantity=%s,IP=%s)'
    values = (Get_Date_Time_Number(),Type,Position,CoinName,OrderPrice,OrderQuantity,Get_My_IP())
    DB_Execute(conn,sql,values)
    DB_Connection_Close(conn)
    

# 신규 코인 내역 저장하기(날짜 / 시간 / 공지사항 제목)
def Save_Listing_Coin(Title) :
    conn = DB_Connection('Fucture')
    sql = 'INSERT INTO Searching_Upbit_Listing_Coin VALUSE(DataTimeNumber=%s,NoticeTitle=%s)'
    values = (Get_Date_Time_Number_TEST(),Title)
    DB_Execute(conn,sql,values)
    DB_Connection_Close(conn)


# 테스트_에러 메세지 저장하기 (날짜 / 시간 / 에러내용)
def TEST_SAVE_ERROR_INFO (ErrorContents) :
    conn = DB_Connection('Fucture')
    sql = 'INSERT INTO Error_Table_Test VALUES(%s,%s)'
    values = (Get_Date_Time_Number_TEST(),ErrorContents)
    DB_Execute(conn,sql,values)
    DB_Connection_Close(conn)


# 테스트_에러 발생 날짜 구하기
def Get_Date_Time_Number_TEST() :
    curr_time = datetime.now()
    Current_Time = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    return Current_Time