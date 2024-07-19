from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()

# VARIABLES A CAMBIAR 
CAMPUS_URL = os.getenv("CAMPUS_URL")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")

# Verificar si las variables de entorno están definidas
if not CAMPUS_URL or not USER_EMAIL or not USER_PASSWORD:
    raise ValueError("Asegúrate de que las variables de entorno CAMPUS_URL, USER_EMAIL y USER_PASSWORD estén definidas")


# Initialize the Chrome driver with options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode if desired
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
try:
    driver.get(CAMPUS_URL)

    # Wait for the login button to be clickable and then click it
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div/a')))
    button.click()

    # Wait for the email input field to be clickable and then enter the user's email
    email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0116"]')))
    email_input.send_keys(USER_EMAIL)

    # Wait for the next button to be clickable and then click it
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
    next_button.click()

    # Wait for the username input field to be clickable and then enter the user's email again
    username_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    username_input.send_keys(USER_EMAIL)

    # Wait for the password input field to be clickable and then enter the user's password
    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    password_input.send_keys(USER_PASSWORD)

    # Wait for the submit credentials button to be clickable and then click it
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SubmitCreds"]')))
    submit_button.click()

    # VER NOTIFICACIONES => DAR CLICK EN INBOX
    inbox_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div/div/ul/li[2]/a')))
    inbox_element.click()

    time.sleep(3)

    # Iterate over //*[@id="tr8837"] and print each one separated
    message_elements = driver.find_elements(By.XPATH, '//*[@id="lista_mensajes"]/table/tbody/tr')

    unread_count = 0
    read_count = 0
    for message_element in message_elements:
        if "leido" in message_element.get_attribute('class'):
            print(message_element.text)
            unread_count += 1
        else:
            print(message_element.text + " NEW")
            read_count += 1

    print(f"Unread messages: {unread_count}")
    print(f"Read messages: {read_count}")

    time.sleep(5)
finally:
    driver.quit()  # Ensure the browser is closed after the script completes

driver.implicitly_wait(10)
