from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import asyncio
import logging

service = Service('D:/JournalParser/webdriver/chromedriver.exe')
options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.binary_location = "webdriver/chrome-win/chrome.exe"
options.add_experimental_option("excludeSwitches", ["enable-logging"])

with open('parser/config.json', "r") as file:
        URL, ENDPOINTS, PREP = json.load(file).values()

async def parserJournal(username: str, password: str) -> dict:
    driver = webdriver.Chrome(options=options, service=service)
    try:
        driver.get(URL)
        await asyncio.sleep(5)

        driver.find_element(By.ID, PREP['username']).send_keys(username)
        driver.find_element(By.ID, PREP['passworssd']).send_keys(password)
        driver.find_element(By.XPATH, PREP['button_auth']).click()
        await asyncio.sleep(5)

        try:
            driver.find_element(By.XPATH, PREP['check_access'])
        except Exception:
            pass
        else:
            raise SystemError('Не удалось авторизоваться!') 
        
        try:
            driver.find_element(By.XPATH, PREP['notification']).click()
        except Exception:
            await asyncio.sleep(1)

        return {key: driver.find_element(By.XPATH, xpath).text for key, xpath in ENDPOINTS.items()}
    
    except Exception as error:
        logging.error(error)
        return str(error)
    
    finally:
        driver.quit()
