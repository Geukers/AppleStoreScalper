import datetime
import time

from selenium.webdriver.common.by import By

import smtplib
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URLs = {"Space Grey": "https://www.apple.com/ca/shop/buy-mac/macbook-pro/14-inch-space-grey-8-core-cpu-14-core-gpu-512gb#",
        "Silver": "https://www.apple.com/ca/shop/buy-mac/macbook-pro/14-inch-silver-8-core-cpu-14-core-gpu-512gb#"}


def send_email(text):
    SMTP_SERVER = 'smtp-mail.outlook.com'
    SMTP_LOGIN = '<EMAIL>'
    SMTP_PASSWORD = '<PWD>'

    FROM = SMTP_LOGIN
    TO = ["philippe.geukers.1@ens.etsmtl.ca"]  # must be a list
    SUBJECT = 'The Macbook Pro is available'
    message = text + "Order now : " + URLs

    # Prepare actual message
    msg = EmailMessage()
    msg.set_content(message)
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = SUBJECT

    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(SMTP_LOGIN, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    notFound = True
    while notFound:
        # p = Path(__file__).with_name('chromedriver.exe')
        # print(p)
        # driver = webdriver.Chrome(p)
        for NAME, URL in URLs.items():
            driver.get(URL)

            time.sleep(1)

            driver.find_element(by=By.CLASS_NAME, value="as-retailavailabilitytrigger-infobutton").click()
            inputElement = driver.find_element(by=By.ID, value="as-retailavailabilitysearch-query")
            inputElement.send_keys('J4Y0L3')
            driver.find_element(by=By.CLASS_NAME, value="search-stores").click()

            time.sleep(1)

            stores = driver.find_elements(by=By.CLASS_NAME, value="as-storeitem")
            available_stores = []
            for i in range(4):
                if "Available" in stores[i].text:
                    available_stores.append(stores[i].find_element(by=By.CLASS_NAME, value="as-storeitem-storename").text)

            if len(available_stores) > 0:
                text = ""
                for store in available_stores:
                    text += NAME + " : " + store + "\n"
                print(str(datetime.datetime.now()))
                text = text + "Order now : " + URL
                print(text)
                send_email(text)
                notFound = False
                break
            print(str(datetime.datetime.now()) + " : No available MacBooks - " + NAME)
        time.sleep(60 * 5)
    driver.quit()

