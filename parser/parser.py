from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parser.settings import *
import asyncio

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
#options.binary_location = "webdriver/chrome-win/chrome.exe"
options.add_experimental_option("excludeSwitches", ["enable-logging"])

async def parserJournal(username: str, password: str) -> dict:
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(URL)
    
    await asyncio.sleep(4)


    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, BUTTON_AUTH).click()

    await asyncio.sleep(3)

    try:
        driver.find_element(By.XPATH, CHECK_ACCESS)
    except Exception:
        try:
            try:
                driver.find_element(By.XPATH, NOTIFICATION).click() # Убераем уведомление 
            except Exception:
                await asyncio.sleep(1)

            data = {'homework': {}}
            data['name'] = driver.find_element(By.XPATH, NAME).text
            data['group'] = driver.find_element(By.XPATH, GROUP).text
            data['avg_rating'] = driver.find_element(By.XPATH, AVG_RATING).text
            data['avg_attendance'] = driver.find_element(By.XPATH, AVG_ATTENDANCE).text
            data['homework']['done'] = driver.find_element(By.XPATH, HOMEWORK_DONE).text
            data['homework']['overdue'] = driver.find_element(By.XPATH, HOMEWORK_OVERDUE).text
            data['homework']['current'] = driver.find_element(By.XPATH, HOMEWORK_CURRENT).text
            data['homework']['verification'] = driver.find_element(By.XPATH, HOMEWORK_VERIFICATION).text
            data['place_group'] = driver.find_element(By.XPATH, PLACE_GROUP).text
            data['place_flow'] = driver.find_element(By.XPATH, PLACE_FLOW).text
        
        except Exception as error:
            print(error)
            driver.quit()
            return 'Ошибка на сервере'
        else:
            driver.quit()
            return data
    else:
        driver.quit()
        return 'Authorization error'