from flask import Flask, jsonify, request
from flask_cors import CORS
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


# DATOS PARA MOSTRAR
materias = []

# Verificar si las variables de entorno están definidas
if not CAMPUS_URL or not USER_EMAIL or not USER_PASSWORD:
    raise ValueError("Asegúrate de que las variables de entorno CAMPUS_URL, USER_EMAIL y USER_PASSWORD estén definidas")

# Initialize the Chrome driver with options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode if desired
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

app = Flask(__name__)
CORS(app)

##############################################
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

def iterate_over_sons(url_location, parent_xpath):
    driver.get(url_location)
    output = []
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, parent_xpath)))
    elements = driver.find_elements(By.XPATH, parent_xpath)

    for element in elements:
        output.append(element.text)
        print(element.text)

    return output

##############################################

@app.route('/api/materias', methods=['GET'])
def get_materias():
    return jsonify(materias)

if __name__ == '__main__':
    app.run(debug=True)

# microsoft_login()
# seleccionar_propuesta(2)
# materias = iterate_over_sons('https://siu.austral.edu.ar/portal/cursada/','//*[@id="js-listado-materias"]/ul/li/a')