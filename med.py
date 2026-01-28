import time
import traceback
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

TOKEN = "ВСТАВЬТЕ_ТОКЕН_ИЗ_BOTFATHER"
CHAT_ID = "ВСТАВЬТЕ_АЙДИ_ЧАТА"
DATA_IN ="ВСТАВЬТЕ_ПРОВЕРЯЕМЫЙ_НОМЕР_ПАСПОРТА"
CHECK_INTERVAL = 24 * 60 * 60  # 24 часа
HEADLESS = False  # <-- True = headless, False = откроет браузер
TESTMODE = True   # Тестовый режим с выводом результатов в телеграм независимо от условий

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def check_status():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://aoam.cnam.gov.md:10201/check-status")

        input_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "TextField0"))
        )
        input_field.clear()
        input_field.send_keys(DATA_IN)  

        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[.//span[text()="Verifica statut"]]')
            )
        )
        button.click()

        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.ID, "TextField15").get_attribute("value") != ""
        )

        result = driver.find_element(By.ID, "TextField15").get_attribute("value")
        print("Статус:", result)


        if TESTMODE:
        # Отправляем тестовое сообщение
            send_telegram_message(f"[TEST] Статус: {result}")
            if result.strip().upper() != "ASIGURAT":
                send_telegram_message("Seems your health insurance expired")
        else:
        # Реальное поведение
        # Следующая закомментированная строка использована для того чтобы убедиться
        # что переключение работает
        # В протичном случае ждать пока не истечет медицинский полис
        # send_telegram_message(f"[PROD] Статус: {result}")
         if result.strip().upper() != "ASIGURAT":
                send_telegram_message("Seems your health insurance expired")


    finally:
        driver.quit()

# ==============
# ОСНОВНОЙ ЦИКЛ
# ==============

print("Bot started. Checking every 24 hours.")

while True:
    try:
        check_status()
    except Exception:
        err = traceback.format_exc()
        send_telegram_message("Insurance bot crashed:\n" + err)

    print("Sleeping for 24 hours...\n")
    time.sleep(CHECK_INTERVAL)
