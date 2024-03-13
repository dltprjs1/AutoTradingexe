import logging
import os
from datetime import datetime

def WriteLog(info, log_filename,logFileName):
    # 로그 설정
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filename=log_filename,filemode='a')
    logging.info(info)


def WriteLog_Future (info) :
    # 로그 디렉토리 생성
    log_dir_Future = 'C:\Program Files\python_workspace\AutoTrading\Future_logs'
    os.makedirs(log_dir_Future, exist_ok=True)
    log_filename_Future = os.path.join(log_dir_Future, "Future "+datetime.now().strftime("%Y%m%d.log"))
    WriteLog(info, log_filename_Future,"Future "+datetime.now().strftime("%Y%m%d.log"))


def WriteLog_Trading (info) :
    # 로그 디렉토리 생성
    log_dir_Trading = 'C:\Program Files\python_workspace\AutoTrading\Trading_logs'
    os.makedirs(log_dir_Trading, exist_ok=True)
    log_filename_Trading = os.path.join(log_dir_Trading, "Trading "+datetime.now().strftime("%Y%m%d.log"))
    WriteLog(info, log_filename_Trading,"Trading "+datetime.now().strftime("%Y%m%d.log"))
