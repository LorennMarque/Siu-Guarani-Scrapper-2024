from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
# options.add_argument('--headless')  # Run in headless mode if desired
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_and_interact_with_element(xpath, text_content=""):
    """
    Esta función espera a que un elemento sea clickeable y luego interactúa con él.
    Si se proporciona un text_content, se ingresará en el elemento, de lo contrario, se hará clic en el elemento.
    :param xpath: El xpath del elemento con el que interactuar.
    :param text_content: El texto a ingresar en el elemento, si corresponde.
    :return: Ninguno
    """
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    if text_content == "":
        element.click()
    else:
        element.send_keys(text_content)

def microsoft_login():
    # Esta función inicia el proceso de login en el campus virtual.
    # Toma en cuenta el login externo de microsoft. Modificar en caso de que tu universidad no lo ultilice.
    # Ayuda en discord => .lorenn
    print("🔒 Ingresando...")
    driver.get(CAMPUS_URL)

    # Wait for the login button to be clickable and then click it
    wait_and_interact_with_element('//*[@id="login"]/div/a')

    # Wait for the email input field to be clickable and then enter the user's email
    wait_and_interact_with_element('//*[@id="i0116"]', USER_EMAIL)

    # Wait for the next button to be clickable and then click it
    wait_and_interact_with_element('//*[@id="idSIButton9"]')

    print("🔐 Login de microsoft...")
    # Wait for the username input field to be clickable and then enter the user's email again
    wait_and_interact_with_element('//*[@id="username"]', USER_EMAIL)

    # Wait for the password input field to be clickable and then enter the user's password
    wait_and_interact_with_element('//*[@id="password"]', USER_PASSWORD)

    # Wait for the submit credentials button to be clickable and then click it
    wait_and_interact_with_element('//*[@id="SubmitCreds"]')

    print("🔓 We're In")

def seleccionar_propuesta(n=1):
    print("📚 Seleccionando propuesta académica")
    driver.execute_script(f"document.querySelector('#js-dropdown-menu-carreras li:nth-child({n}) a').click();")


def scrape_subjects():
    driver.get("https://siu.austral.edu.ar/portal/cursada/")
    parent_xpath = '//*[@id="js-listado-materias"]/ul/li/a'
    output = {}
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, parent_xpath)))
    elements = driver.find_elements(By.XPATH, parent_xpath)

    for element in elements:
        output[element.text] = {
            'url': element.get_attribute('href')
        }

    for subject_name, subject_data in output.items():
        driver.get(subject_data['url'])
        time.sleep(0.3)
        try:
            cupos = driver.find_element(By.XPATH, '//*[@id="comisiones"]/li/div/ul/li[1]/div[1]/div[2]').text
        except:
            cupos = ''
        try:
            description = driver.find_element(By.XPATH, '//*[@id="comisiones"]/li/div/ul/div/div[2]').text
        except:
            description = ''
        output[subject_name] = {
            'url': subject_data['url'],
            'cupos': cupos,
            'description': description,
        }

    return output

def iterate_over_sons(url_location, parent_xpath):
    driver.get(url_location)
    output = []
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, parent_xpath)))
    elements = driver.find_elements(By.XPATH, parent_xpath)

    for element in elements:
        output.append(element.text)
        print(element.text)

    return output

microsoft_login()
seleccionar_propuesta(2)
materias = scrape_subjects()
print(materias)

import csv
import datetime

with open('materias.csv', 'w', newline='') as csvfile:
    fieldnames = ['data', 'current_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for subject_name, subject_data in materias.items():
        writer.writerow({'data': subject_data, 'current_date': datetime.date.today()})

# materias = iterate_over_sons('https://siu.austral.edu.ar/portal/cursada/','//*[@id="js-listado-materias"]/ul/li/a')









# def print_pestañas_reportes():
#     # Obtén los enlaces de los reportes
#     global report_links
#     report_links = driver.find_elements(By.XPATH, '//*[@id="js-nav"]/li[3]/ul/li/a')

#     # Imprime los ID de los elementos padre
#     for index, link in enumerate(report_links):
#         parent_id = link.find_element(By.XPATH, '..').get_attribute('id')
#         print(f"[{index + 1}] {parent_id}")

# def seleccionar_pestaña_reportes(target):
#     # Verifica que la opción sea válida y haz clic en el enlace correspondiente
#     if 1 <= target <= len(report_links):
#         driver.execute_script(f"document.querySelector('#js-nav li:nth-child(3) ul li:nth-child({target}) a').click();")
#     else:
#         print("Opción inválida. Por favor, seleccione una opción válida.")




# all_materias()
# time.sleep(200)
################################################################################################
###############################  VER NOTIFICACIONES SIU  #######################################
################################################################################################
# # VER NOTIFICACIONES => DAR CLICK EN INBOX
# wait_and_interact_with_element('/html/body/div[1]/div/div/div[2]/div[1]/div/div/ul/li[2]/a')

# time.sleep(3)

# # Iterate over //*[@id="tr8837"] and print each one separated
# message_elements = driver.find_elements(By.XPATH, '//*[@id="lista_mensajes"]/table/tbody/tr')

# unread_count = 0
# read_count = 0
# for message_element in message_elements:
#     if "leido" in message_element.get_attribute('class'):
#         print(message_element.text)
#         unread_count += 1
#     else:
#         print(message_element.text + " NEW")
#         read_count += 1

# print(f"Unread messages: {unread_count}")
# print(f"Read messages: {read_count}")

# time.sleep(5)
################################################################################################
################################################################################################
################################################################################################
