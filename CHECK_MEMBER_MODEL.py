from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json
import os
import time
import random
import re

def check_member_facade(ans,url,rule,wait_second = [3,4]):
        ALL_NUMBER = 0
        def prepare_driver():
            # 設定 User-Agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            # 建立 ChromeOptions
            options = webdriver.ChromeOptions()
            #options.add_argument("--headless")  # 啟用無頭模式
            #options.add_argument("--disable-gpu")  # 可能有助於在某些系統上穩定運行
            options.add_argument("--window-size=1920x1080")  # 設定視窗大小，避免某些元素無法渲染
            options.add_argument(f"user-agent={user_agent}")  # 設定 User-Agent

            # 1. 啟動瀏覽器
            service = Service(ChromeDriverManager().install())  # Selenium 4 的新寫法
            driver = webdriver.Chrome(service=service,options=options)
            
            # 2. 先訪問目標網站 (與 Cookie 作用的 domain 一致)
            driver.get("https://www.facebook.com/")

            # 3. 讀取 JSON 檔案
            with open("fb-cookies.json", "r", encoding="utf-8") as f: cookies = json.load(f)

            # 4. 加載 Cookie
            for cookie in cookies: 
                if "sameSite" not in cookie or cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "Lax"  # 設定預設值
                if "domain" in cookie:
                    del cookie["domain"]
                driver.add_cookie(cookie)
            print('成功加載')
            driver.refresh()
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label='你的個人檔案']")))
            driver.execute_script("arguments[0].click();", button)
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label='切換為迫真避難社社團專家群']")))
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
            return driver
        driver = prepare_driver()
        def EnterToPage():
            nonlocal ALL_NUMBER
            driver.get(url)
            MOVE = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '申請')]")))
            driver.execute_script("arguments[0].click();",MOVE)
            try:
                number = re.sub(r'\D+','',WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.xngnso2.x1qb5hxa.x1xlr1w8.xi81zsa"))).text)
                print(f'這是{number}')
                ALL_NUMBER = int(number)
            except:
                print(f'沒有入社申請')
                ALL_NUMBER = 0
            print(f'現在有{ALL_NUMBER}個入社申請')
            
            time.sleep(1)
        def RestAndPrepareNewDriver():
            SLEEP = random.randint(600,700)
            print(f'休眠{SLEEP/60}分鐘緩衝，請稍後'+'.'*30)
            time.sleep(SLEEP)
            ERROR = 0
            print('重開瀏覽器')
            driver.quit()
            driver = prepare_driver()
            return driver
        EnterToPage()
        NowTime = time.time()
        ERROR = 0
        pre = ''
        while True:
            try:
                if ALL_NUMBER == 0:
                    driver = RestAndPrepareNewDriver()
                pages = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.x1jx94hy.x30kzoy.x9jhf4c.xgqcy7u.x1lq5wgf.xev17xk.xktsk01.x1d52u69.x19i0xim.x6ikm8r.x10wlt62.x1n2onr6')))
                name = pages.find_element(By.CSS_SELECTOR,'.xu06os2.x1ok221b').text
                time.sleep(random.randint(*wait_second))
                if pages.text == pre:
                    EnterToPage()
                    continue
                # print(pages.text)
                ERROR = 0
                pre = pages.text
                if rule(pages,ans) :
                    driver.execute_script("arguments[0].click();", pages.find_element(By.XPATH, './/*[contains(@aria-label, "批准")]'))
                    print(f'批准{name}入社')
                else:
                    driver.execute_script("arguments[0].click();", pages.find_element(By.XPATH, './/*[contains(@aria-label, "拒絕")]'))
                    print(f'拒絕{name}入社')
                ALL_NUMBER -= 1
                print(f'目前的{ALL_NUMBER}')
            except Exception as e:
                if len(driver.find_elements(By.CSS_SELECTOR, '[aria-label="重新載入頁面"]')):
                    RETRY = driver.find_element(By.CSS_SELECTOR, '[aria-label="重新載入頁面"]')
                    driver.execute_script("arguments[0].click();", RETRY)
                    continue

                ERROR += 1
                print(f'壞{ERROR}次\n錯誤訊息:{e}\n')
                time.sleep(1)
                if ERROR >= 10:
                    driver = RestAndPrepareNewDriver()
                broken = 0
                while broken < 10:
                    try:
                        EnterToPage()
                        break
                    except:
                        broken += 1
                        continue
                if broken == 10:
                    print('重開瀏覽器')
                    prepare_driver()
                    EnterToPage()

