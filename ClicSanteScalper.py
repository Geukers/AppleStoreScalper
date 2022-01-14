import datetime
import time

from selenium.webdriver.common.by import By

import smtplib
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URLs = {"Clic santé": "https://portal3.clicsante.ca/"}


def send_email(subject, text):
    SMTP_SERVER = 'smtp-mail.outlook.com'
    SMTP_LOGIN = 'geukers@outlook.com'
    SMTP_PASSWORD = 'F3YKLb2FLWv6B93!k2*o!PO8@BLkYy!MpuYCgkSc*mebW%D^9O2t&8B3%6&rXvuT'

    FROM = SMTP_LOGIN
    TO = ["philippe.geukers.1@ens.etsmtl.ca"]  # must be a list

    message = text

    # Prepare actual message
    msg = EmailMessage()
    msg.set_content(message)
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = subject

    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(SMTP_LOGIN, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    notFound = True
    while notFound:
        for NAME, URL in URLs.items():
            driver.get(URL)

            time.sleep(1)

            card_text = driver.find_element(by=By.CLASS_NAME, value="v-card__text")

            if "18" in card_text.text:
                send_email("Book your Vaccine Now!", "URL : " + URL)
                print("Book your Vaccine Now! - URL : " + URL)
                notFound = False
                break
            print(str(datetime.datetime.now()) + " : Vaccination is still restricted")
        time.sleep(60 * 5)
    driver.quit()

