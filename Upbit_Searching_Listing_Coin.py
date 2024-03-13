from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import telegram
import asyncio
import Database

def Driver_Option ():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    service = Service('C:\Program Files\python_workspace\chromedriver_win32\chromedriver.exe')
    driver = webdriver.Chrome(service=service,options=options)
    

async def main(Text):
    token = ""
    id = ""
    bot = telegram.Bot(token = token)
    await bot.send_message(chat_id=id,text=Text)


def Searching_Upbit_List_Coin(Title):
    Return = True
    conn = Database.DB_Connection('Fucture')
    sql = 'SELECT * FROM Searching_Upbit_Listing_Coin WHERE NoticeTitle =%s'
    values = Title
    cursor = Database.DB_Select(conn,sql,values)
    row = cursor.fetchone()
    while row:
        print(row[1])
        print(row[2])
        if row[2] == Title:
            Return = False
    Database.DB_Connection_Close(conn)
    return Return


def SearchingListingCoin ():
    Driver_Option()
    driver.get("https://upbit.com/service_center/notice")
    driver.maximize_window()
    notice = driver.find_elements(By.CLASS_NAME, "css-12ct4qh")

    if notice == [] : 
        asyncio.run(main('NotFound Class_Name'))

    for i in notice:
        title = i.text
        #if title.find('자산 추가') != -1 and Searching_Upbit_List_Coin(title) == True:
        if title.find('유통량') != -1 and Searching_Upbit_List_Coin(title) == True:
            Database.Save_Listing_Coin(title)
            asyncio.run(main(title))
    driver.quit()

SearchingListingCoin()


