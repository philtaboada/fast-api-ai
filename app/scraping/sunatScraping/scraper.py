from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# Configuración de las opciones de Edge
options = webdriver.EdgeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# Inicializar el WebDriver de Edge usando webdriver_manager
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)


# Abrir la página web
driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')


# ------- Pagina principal ------- 

# Esperar a que el elemento esté presente en el DOM
wait = WebDriverWait(driver, 10)

inputRuc = driver.find_element(By.CSS_SELECTOR, "input.form-control")
inputRuc.click()
# 20611519347 10238960342
inputRuc.send_keys("20611519347")

time.sleep(10)

btnBuscar = driver.find_element(By.CSS_SELECTOR, "button.btn btn-primary".replace(" ", "."))
btnBuscar.click()



# ------- Pagina de resultados ------- 

print("-------------------")

tbody_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tbody')))

firts = tbody_elements[0].find_element(By.TAG_NAME, 'tr')
# print(firts.text)

# print(tbody_elements[0].text)

# tresPrimeros = td_elements[:3]
# print(tbody_elements[0])
for tbody_element in tbody_elements[0]:
    print(tbody_element)



# Esperar a que el elemento esté presente en el DOM
wait = WebDriverWait(driver, 10)
h4_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h4')))

# h4_elementsNew = h4_elements[:]
# del h4_elements[1]

for h4_element in h4_elements:
    print(h4_element.text)



# time.sleep(2)

# p_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'p')))

# del p_elements[-1]
# p_elements.insert(0, h4_elementsNew[1])
# p_elements.insert(11, tresPrimeros)
# p_elements[12:12] = tresPrimeros

# for p_element in p_elements:
#     print(p_element.text)


# Opcional: Esperar un poco para ver la página cargada
time.sleep(5)

# Cerrar el navegador
# driver.quit()
