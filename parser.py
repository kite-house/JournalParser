from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import asyncio

base_url = 'https://journal.top-academy.ru/ru'

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument("--disable-extensions")
options.add_argument('--disable-application-cache')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--incognito')
options.add_argument('--disable-crash-reporter')
#options.binary_location = "webdriver/chrome-win/chrome.exe"
options.add_experimental_option("excludeSwitches", ["enable-logging"])

async def parserJournal(username: str, password: str) -> dict:
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(base_url)
    
    asyncio.sleep(4)


    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/section/div/div/div/div/div[1]/tabset/div/tab[1]/form/button').click()

    asyncio.sleep(3)

    try:
        driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/section/div/div/div/div/div[1]/tabset/div/tab[1]/form/div[1]/div/div')
    except Exception:
        try:
            try:
                driver.find_element(By.XPATH, '/html/body/modal-container/div/div/div/button').click() # Убераем уведомление 
            except Exception:
                asyncio.sleep(1)

            data = {'homework': {}}
            data['name'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[1]/top-pane/nav/div[1]/span[2]/span[1]/a').text
            data['group'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[1]/top-pane/nav/div[1]/span[2]/span[2]/span[2]').text
            data['avg_rating'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/progress-component/div/div/div/div/div[2]/div/div/div[1]/span[1]').text
            data['avg_attendance'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/attendance-component/div/div/div/div/div[2]/div/div/div[1]/span[1]').text
            data['homework']['done'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/span').text
            data['homework']['overdue'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/span').text
            data['homework']['current'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div[1]/span').text
            data['homework']['verification'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div[1]/span').text
            data['place_group'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/leader-component/div/div/div[1]/div/div[1]/div/div/div[2]/div[1]/div').text
            data['place_flow'] = driver.find_element(By.XPATH, '/html/body/mystat/ng-component/ng-component/div/div[3]/div[2]/ng-component/div/div/leader-component/div/div/div[1]/div/div[1]/div/div/div[2]/div[2]/div').text
        
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