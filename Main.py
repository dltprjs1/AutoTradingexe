import Binance_Trading
import Upbit_Trading
import threading
import schedule
import time
import subprocess
import sys

#def restart_program():
#    print("Restarting the program...")
#    python = sys.executable

#    subprocess.call([python] + sys.argv)


#schedule.every().day.at("00:01").do(restart_program)
#now = time.localtime()
#start_time = time.strftime("%H:%M", now)
#schedule.every().day.at(start_time).do(restart_program)

BinanceThread = threading.Thread(target=Binance_Trading.Searching_Transaction_Condition_BTC)
UpbitThread = threading.Thread(target=Upbit_Trading.Searching_Transaction_Condition_Coin)

BinanceThread.start()
UpbitThread.start()

#while True:
#    schedule.run_pending()
#    time.sleep(1)

