import ccxt
import SocketClient
from datetime import datetime
import pprint


try:
    # 예외를 발생시키는 코드
    raise Exception("asdaaosdbhaijsnbdkjaubskdj\nakshdbkahjsbdkujabskdjawe\nqowenljansbkduhakosjdnajuwoudjnaosid.")
except Exception as e:
    error_message = str(e)
    # 여기서 에러 메시지 출력 또는 저장
    print(error_message)
    SocketClient.SendServer("Error"+'#'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'#'+'FUTURE'+'#'+'Test: '+str(e))
