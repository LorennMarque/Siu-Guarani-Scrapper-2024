from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


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

driver = webdriver.Chrome(options=options)

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

def seleccionar_propuesta():
    print("📚 Seleccionando propuesta académica")
    try:
        # Esperar a que el menú desplegable esté presente
        dropdown_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="js-dropdown-menu-carreras"]/li/a'))
        )
        print("El menú desplegable está presente.")
        
        # Verificar si el menú tiene elementos
        if dropdown_menu:
            print(f"Se encontraron {len(dropdown_menu)} elementos en el menú desplegable.")
            # Imprimir el texto de cada elemento hijo
            for index, option in enumerate(dropdown_menu):
                print(f"[{index + 1}] {option.get_attribute('title')}")
            # Solicitar al usuario que seleccione una opción
            selected_option = int(input("Por favor, seleccione una opción: "))
            if selected_option > 0 and selected_option <= len(dropdown_menu):
                print(f"Ha seleccionado la opción {selected_option}.")
                driver.execute_script(f"document.querySelector('#js-dropdown-menu-carreras li:nth-child({selected_option}) a').click();")
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
        else:
            print("No se encontraron elementos en el menú desplegable.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

def print_pestañas_reportes():
    # Obtén los enlaces de los reportes
    global report_links
    report_links = driver.find_elements(By.XPATH, '//*[@id="js-nav"]/li[3]/ul/li/a')

    # Imprime los ID de los elementos padre
    for index, link in enumerate(report_links):
        parent_id = link.find_element(By.XPATH, '..').get_attribute('id')
        print(f"[{index + 1}] {parent_id}")

def seleccionar_pestaña_reportes(target):
    # Verifica que la opción sea válida y haz clic en el enlace correspondiente
    if 1 <= target <= len(report_links):
        driver.execute_script(f"document.querySelector('#js-nav li:nth-child(3) ul li:nth-child({target}) a').click();")
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")

def all_materias():
    print("Buscando materias...")
    
    # Esperar hasta que el elemento de navegación esté disponible y hacer clic en él
    wait_and_interact_with_element('//*[@id="cursada"]/a')

    
    print("Seleccionando materias...")
    # Esperar hasta que el elemento de navegación esté disponible y hacer clic en él
    materias = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="js-listado-materias"]/ul/li/a'))
    )

    lista_materias = []

    # Imprimir el título de cada materia
    for materia in materias:
        lista_materias.append(materia.text)
        print(materia.text)

    return lista_materias

microsoft_login()
seleccionar_propuesta()
all_materias()
time.sleep(200)
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
