from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
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
        URL, ENDPOINTS, PREP, SCHED = json.load(file).values()


async def auth(username: str, password: str, driver = None):
    ''' Авторазация пользователя на сайте, с получением драйвера если он уже был запущен. '''
    driver_start = False # Запустим ли мы драйвер сами, или мы уже получили запущенный
    if driver is None:
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(URL)
        driver_start = True
        await asyncio.sleep(5)

    driver.find_element(By.ID, PREP['username']).send_keys(username)
    driver.find_element(By.ID, PREP['password']).send_keys(password)
    driver.find_element(By.XPATH, PREP['button_auth']).click()

    await asyncio.sleep(5)

    try:
        driver.find_element(By.XPATH, PREP['check_access'])
    except Exception:
        return 'successfully authorizate'
         
    else:
        return "failed to authorizate"
    
    finally:
        if driver_start:
            driver.quit()
     
async def parserJournal(username: str, password: str) -> dict:
    ''' Получение данных о пользователе с главной страницы '''
    driver = webdriver.Chrome(options=options, service=service)
    try:
        driver.get(URL)
        await asyncio.sleep(5)

        if await auth(username, password, driver=driver) == "failed to authorizate":
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


async def parserSchedule(username: str, password: str) -> dict:
    """ Получение данных об расписание пользователя """
    driver = webdriver.Chrome(options=options, service=service)
    try:
        driver.get(URL)
        await asyncio.sleep(5)

        if await auth(username, password, driver=driver) == "failed to authorizate":
            raise SystemError('Не удалось авторизоваться!')
        
        driver.get(f'{URL}/main/schedule/page/index')
        await asyncio.sleep(5) 

        driver.find_element(By.XPATH, SCHED['selected_day']).click()

        await asyncio.sleep(3)

        schedule = driver.find_element(By.XPATH, SCHED['schedule'])

        lines = schedule.text.strip().split('\n')
        current_index, current_lesson, result = None, {}, {}

        for line in lines:
            line = line.strip()

            if line.isdigit():
                if current_index is not None and current_lesson:
                    result[current_index] = current_lesson
                current_index, current_lesson = int(line), {}

            elif ' - ' in line: 
                current_lesson['time'] = line

            elif not current_lesson.get('name'):
                current_lesson['name'] = line

            elif not current_lesson.get('location'):
                current_lesson['location'] = line

            elif not current_lesson.get('teacher'): 
                current_lesson['teacher'] = line

        if current_index is not None and current_lesson:
            result[current_index] = current_lesson

        return result
    
    except Exception as error:
        logging.error(error)
        return str(error) 
    finally:
        driver.quit()       