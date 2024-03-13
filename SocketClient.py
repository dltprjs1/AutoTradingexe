import socket
import configparser
from datetime import datetime

CompareTime = ""

def SendServer(Messages):    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        Type = Check_Header(Messages)
        Result = "Send"
        
        if Type == 1 :  
            Result = Check_Time()
            
        if Result == "Send" : 
            client_socket.connect((read_ini_file('Server','ip'), int(read_ini_file('Server','port'))))
            client_socket.sendall(Messages.encode())
            
    except ConnectionRefusedError:
        print("연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    finally:
        client_socket.close()


def Check_Header(Messages):
    Type = 2
    if ("Condition" in Messages) or ("ConditionResetInfo" in Messages) or ("Error" in Messages): Type = 1
    return Type
    
    
def Check_Time():
    global CompareTime
    current_time = datetime.now()
    Time = current_time.strftime("%H%M")
    Result = "Don't Send"
    if CompareTime != Time: 
        Result = "Send"
        CompareTime = Time
        
    return Result


def read_ini_file(Title,Key):
    config = configparser.ConfigParser()
    config.read("AutoTrading\AutoTrading.ini")
    Value = config.get(Title, Key)
    return Value


def Write_ini_file(Title,Key,Value):
    config = configparser.ConfigParser()
    config.read('AutoTrading\AutoTrading.ini')
    config.set(Title, Key, Value)
    with open('AutoTrading\AutoTrading.ini', 'w') as configfile:
        config.write(configfile)