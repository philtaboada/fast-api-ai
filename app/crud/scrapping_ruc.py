from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from unidecode import unidecode
from selenium.common.exceptions import TimeoutException
from app.schemas.user_by_ruc import save_user_ruc_data
from app.models.user_by_ruc import UserByRuc
# from app.crud.sunatinfo import SunatInfo

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def search_ruc(driver, ruc_number):
    try:
        uri_one = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
        driver.get(uri_one)

        input_ruc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control"))
        )
        input_ruc.send_keys(ruc_number)
        
        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        btn_buscar.click()
    except TimeoutException:
        raise TimeoutException("Timeout while navigating to supplier page")
    
def clean_text(text):
    # Eliminar tildes
    #text = unidecode(text)
    # Convertir a minúsculas
    text = text.lower()
    # Reemplazar espacios en blanco con guiones bajos
    text = text.replace(' ', '_')
    # Reemplazar caracteres especiales como ' con _
    # text = text.replace('\'', '_')
    return text

def extract_data_ruc(driver):
    try:
        # Esperar a que el elemento principal esté presente en la página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-primary"))
        )

        # Obtener todos los elementos de la lista de datos
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "list-group-item"))
        )

        # Mapeo de claves procesadas a claves del diccionario de datos
        mapping = {
            'numero_de_ruc': 'numeroRuc',
            'tipo_contribuyente': 'tipoContribuyente',
            'tipo_de_documento': 'tipoDeDocumento',
            'nombre_comercial': 'nombreComercial',
            'fecha_de_inscripcion': 'fechaDeInscripcion',
            'estado_del_contribuyente': 'estadoDelContribuyente',
            'condicion_del_contribuyente': 'condicionDelContribuyente',
            'domicilio_fiscal': 'domicilioFiscal',
            'sistema_emision_de_comprobante': 'sistemaEmisionDeComprobante',
            'actividad_comercio_exterior': 'actividadComercioExterior',
            'sistema_contabilidad': 'sistemaContabilidad',
            'actividad(es)_economica(s)': 'actividadesEconomicas',
            'comprobantes_de_pago_c/aut._de_impresion_(f._806_u_816)': 'comprobantesDePagoCuImpresos',
            'sistema_de_emision_electronica': 'sistemaDeEmisionElectronica',
            'emisor_electronico_desde': 'emisorElectronicoDesde',
            'comprobantes_electronicos': 'comprobantesElectronicos',
            'afiliado_al_ple_desde': 'afiliadoAlPleDesde',
            'padrones': 'padrones'
        }

        # Inicializar el diccionario para almacenar los datos
        dataRuc = {value: '' for value in mapping.values()}

        for item in items:
            # Limpiar y dividir el texto del elemento en clave y valor
            arrayClean = item.text.replace('\n', '').split(':')
            
            # Verificar que hay al menos una clave y un valor
            if len(arrayClean) < 2:
                continue

            # Limpiar la clave y extraer el valor
            key = clean_text(arrayClean[0])
            value = arrayClean[1].strip()

            # Verificar si la clave está en el mapeo y procesar el valor
            if key in mapping:
                if key == 'fecha_de_inscripcion':
                    # Procesar el valor para 'fecha_de_inscripcion'
                    dataRuc[mapping[key]] = value.replace('Fecha de Inicio de Actividades', '')
                    if len(arrayClean) > 2:
                        dataRuc['fechaDeInicioDeActividades'] = arrayClean[2]
                elif key == 'sistema_emision_de_comprobante':
                    # Procesar el valor para 'sistema_emision_de_comprobante'
                    dataRuc[mapping[key]] = value.replace('Actividad Comercio Exterior', '')
                    if len(arrayClean) > 2:
                        dataRuc['actividadComercioExterior'] = arrayClean[2]
                elif key == 'comprobantes_de_pago_c/aut._de_impresion_(f._806_u_816)':
                    # Procesar el valor para 'comprobantes_de_pago_c/aut._de_impresion_(f._806_u_816)'
                    dataRuc[mapping[key]] = value
                else:
                    # Procesar otros valores
                    dataRuc[mapping[key]] = value
        
        return dataRuc
    except Exception as e:
        # Manejar excepciones e imprimir el error
        print(f"Error en extract_data: {e}")

def extract_legal_agent(driver):
    try:
        # Espera a que el botón sea clicable y luego hace clic en él
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btnInfRepLeg"))
        )
        button.click()

        # Espera a que la tabla sea visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )

        # Extrae los encabezados de la tabla
        headers = driver.find_elements(By.XPATH, "//table/thead/tr/th")
        header_texts = [header.text.strip() for header in headers]

        # Extrae las filas de datos de la tabla
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        data = {}
        
        for row in rows:
            # Extrae las celdas de la fila
            cells = row.find_elements(By.XPATH, "./td")
            row_data = [cell.text.strip() for cell in cells]
            
            # Convierte la fila en un diccionario usando los encabezados
            if row_data:
                data = dict(zip(header_texts, row_data))

        return data
    except Exception as e:
        # Maneja y reporta errores
        print(f"Error en extract_data: {e}")
        return {}
        
def get_info_ruc(ruc_number):
    driver = initialize_driver()
    try:
        search_ruc(driver, ruc_number)
        data_ruc = extract_data_ruc(driver)
        data_legal_agent = extract_legal_agent(driver)

        # Crear la instancia de UserByRuc
        user_data = UserByRuc(
            consulta_ruc=data_ruc,
            legal_agent=data_legal_agent
        )
        
        # Guardar en la base de datos
        save_user_ruc_data(user_data)

        return user_data
    except Exception as e:
        print(f"Error al obtener información del RUC: {e}")
        return {"error": str(e)}

    finally:
        driver.quit()


# Configuración de las opciones de Edge
# def get_info_ruc(ruc_number):
#     chrome_options = Options()
#     #chrome_options.add_argument('--headless') 
#     #chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--no-sandbox')
    
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
    
#     try:
#         driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')
#         numero_aleatorio = random.randint(4, 10)
        
#         # ####################
#         # Pagina principal
#         # ####################
#         input_ruc = WebDriverWait(driver, numero_aleatorio).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control"))
#         )
#         time.sleep(numero_aleatorio)
#         input_ruc.click()
#         input_ruc.send_keys(ruc_number)
        
#         btn_buscar = WebDriverWait(driver, numero_aleatorio).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
#         )
#         btn_buscar.click()
#         time.sleep(numero_aleatorio)


#         # ####################
#         # Pagina de resultados
#         # ####################
#         items = WebDriverWait(driver, numero_aleatorio).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.list-group-item"))
#         )

#         # Variable para la creacion del objeto
#         numeroRuc = ''
#         tipoContribuyente = ''
#         tipoDeDocumento = ''
#         nombreComercial = ''
#         fechaDeInscripcion = ''
#         fechaDeInicioDeActividades = ''
#         estadoDelContribuyente = ''
#         condicionDelContribuyente = ''
#         domicilioFiscal = ''
#         sistemaEmisionDeComprobante = ''
#         actividadComercioExterior = ''
#         sistemaContabilidad = ''
#         actividadesEconomicas = ''
#         comprobantesDePagoCuImpresos = ''
#         sistemaDeEmisionElectronica = ''
#         emisorElectronicoDesde = ''
#         comprobantesElectronicos = ''
#         afiliadoAlPleDesde = ''
#         padrones = ''
        
        
#         for item in items:
#             arrayClean = item.text.replace('\n','').split(':')
#             # Aplicar la función al primer valor del array
#             arrayClean[0] = clean_text(arrayClean[0])
#             print(arrayClean)

#             if arrayClean[0] == 'numero_de_ruc':
#                 numeroRuc = arrayClean[1]
#                 # print(numeroRuc)

#             if arrayClean[0] == 'tipo_contribuyente':
#                 tipoContribuyente = arrayClean[1]
#                 # print(tipoContribuyente)

#             if arrayClean[0] == 'tipo_de_documento':
#                 tipoDeDocumento = arrayClean[1]
#                 # print(tipoDeDocumento)
        
#             if arrayClean[0] == 'nombre_comercial':
#                 nombreComercial = arrayClean[1]
#                 # print(nombreComercial)
        
#             if arrayClean[0] == 'fecha_de_inscripcion':
#                 fechIncrLimpiar1 = arrayClean[1].replace('Fecha de Inicio de Actividades','')
#                 fechaDeInscripcion = fechIncrLimpiar1
#                 # print(fechaDeInscripcion)
        
#             # Fecha de inicio de actividades
#             if arrayClean[0] == 'fecha_de_inscripcion':
#                 fechaDeInicioDeActividades = arrayClean[2]
#                 # print(fechaDeInicioDeActividades)

#             if arrayClean[0] == 'estado_del_contribuyente':
#                 estadoDelContribuyente = arrayClean[1]
#                 # print(estadoDelContribuyente)

#             if arrayClean[0] == 'condicion_del_contribuyente':
#                 condicionDelContribuyente = arrayClean[1]
#                 # print(condicionDelContribuyente)

#             if arrayClean[0] == 'domicilio_fiscal':
#                 domicilioFiscal = arrayClean[1]
#                 # print(domicilioFiscal)

#             if arrayClean[0] == 'sistema_emision_de_comprobante':
#                 fechIncrLimpiar2 = arrayClean[1].replace('Actividad Comercio Exterior','')
#                 sistemaEmisionDeComprobante = fechIncrLimpiar2
#                 # print(sistemaEmisionDeComprobante)

#             # Actividad comercio exterior
#             if arrayClean[0] == 'sistema_emision_de_comprobante':
#                 actividadComercioExterior = arrayClean[2]
#                 # print(actividadComercioExterior)

#             if arrayClean[0] == 'sistema_contabilidad':
#                 sistemaContabilidad = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'actividad(es)_economica(s)':
#                 actividadesEconomicas = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'comprobantes_de_pago_c/aut._de_impresión_(F._806_u_816)':
#                 comprobantesDePagoCuImpresos = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'sistema_de_emision_electronica':
#                 sistemaDeEmisionElectronica = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'emisor_electronico_desde':
#                 emisorElectronicoDesde = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'comprobantes_electronicos':
#                 comprobantesElectronicos = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'afiliado_al_ple_desde':
#                 afiliadoAlPleDesde = arrayClean[1]
#                 # print(sistemaContabilidad)

#             if arrayClean[0] == 'padrones':
#                 padrones = arrayClean[1]
#                 # print(sistemaContabilidad)

#         sunatInfo = SunatInfo(
#             numeroRuc,
#             tipoContribuyente,
#             tipoDeDocumento,
#             nombreComercial,
#             fechaDeInscripcion,
#             fechaDeInicioDeActividades,
#             estadoDelContribuyente,
#             condicionDelContribuyente,
#             domicilioFiscal,
#             sistemaEmisionDeComprobante,
#             actividadComercioExterior,
#             sistemaContabilidad,
#             actividadesEconomicas,
#             comprobantesDePagoCuImpresos,
#             sistemaDeEmisionElectronica,
#             emisorElectronicoDesde,
#             comprobantesElectronicos,
#             afiliadoAlPleDesde,
#             padrones
#             )
#         # print(sunatInfo)
#         # time.sleep(5)
#         return {
#             'ruc' : sunatInfo.numero_de_ruc,
#             'tipoContribuyente' : sunatInfo.tipo_contribuyente,
#             'tipoDeDocumento' : sunatInfo.tipo_de_documento,
#             'nombreComercial' : sunatInfo.nombre_comercial,
#             'fechaDeInscripcion' : sunatInfo.fecha_de_inscripcion,
#             'fechaDeInicioDeActividades' : sunatInfo.fecha_de_inicio_de_actividades,
#             'estadoDelContribuyente' : sunatInfo.estado_del_contribuyente,
#             'condicionDelContribuyente' : sunatInfo.condicion_del_contribuyente,
#             'domicilioFiscal' : sunatInfo.domicilio_fiscal,
#             'sistemaEmisionDeComprobante' : sunatInfo.sistema_emision_de_comprobante,
#             'actividadComercioExterior' : sunatInfo.actividad_comercio_exterior,
#             'sistemaContabilidad' : sunatInfo.sistema_contabilidad,
#             'actividadesEconomicas' : sunatInfo.actividades_economicas,
#             'comprobantesDePagoCuImpresos' : sunatInfo.comprobantes_de_pago_cu_impresos,
#             'sistemaDeEmisionElectronica' : sunatInfo.sistema_de_emision_electronica,
#             'emisorElectronicoDesde' : sunatInfo.emisor_electronico_desde,
#             'comprobantesElectronicos' : sunatInfo.comprobantes_electronicos,
#             'afiliadoAlPleDesde' : sunatInfo.afiliado_al_ple_desde,
#             'padrones' : sunatInfo.padrones
#         }
    
#     except Exception as e:
#         print(f"Error al obtener información del RUC: {e}")
#         return {"error": str(e)}
    
#     finally:
#         driver.quit()

# def convert_sunat_obj(table_info, ruc):
#     try:
#         sunat_info = SunatInfo()
#     except Exception as e:
#         print(f"Error al crear objeto SunatInfo: {e}")
#         return {"error": str(e)}


# Función para limpiar el primer valor del array
