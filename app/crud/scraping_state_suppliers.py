from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import tempfile
import os
import glob
import pandas as pd
from app.models.user_by_state_suppliers import UserByStateSupplier, ConformationSocietaria
from app.schemas.user_by_state_suppliers import save_state_supplier_data
import math

download_dir = tempfile.mkdtemp()

def initialize_driver(download_dir):

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False, 
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def navigate_to_supplier_page(driver, ruc):
    try:
        uri_one = 'https://apps.osce.gob.pe/perfilprov-ui/'
        driver.get(uri_one)
        
        input_ruc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "textBuscar"))
        )
        input_ruc.send_keys(ruc)
        
        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnBuscar"))
        )
        btn_buscar.click()

        card_content = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[routerlinkactive="active"]'))
        )
        card_content.click()
    except TimeoutException:
        raise TimeoutException("Timeout while navigating to supplier page")

def extract_supplier_name(driver):
    try:
        wait = WebDriverWait(driver, 10)
        supplier_name_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page__title')))
        return supplier_name_element.text.strip()
    except TimeoutException:
        raise TimeoutException("Timeout while extracting supplier name")

def extract_current_tags(driver):
    current = {}
    try:
        tags = driver.find_elements(By.XPATH, '//div[@class="tag tag--active"]')
        for idx, tag in enumerate(tags):
            key = f"{idx + 1}" 
            current[key] = tag.text
    except NoSuchElementException:
        pass
    return current

def extract_additional_info(driver):
    additional_info = {}

    # Mapeo de nombres de campos de scraping a nombres esperados en el modelo
    field_mapping = {
        'RUC(*)': 'RUC',
        'Teléfono(*)': 'Teléfono',
        'Email(*)': 'Email',
        'Domicilio(**)': 'Domicilio',
        'CMC(*)': 'CMC',
        'CLC(*)': 'CLC',
        'Estado(**)': 'Estado',
        'Condición(**)': 'Condición',
        'Tipo de Contribuyente(**)': 'Tipo_de_Contribuyente'
    }

    try:
        profile_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="profile-content reduced"]'))
        )
        view_more = profile_content.find_element(By.XPATH, '//span[@class="see-more flex"]')
        view_more.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '(//div[@class="profile-content"]/ul[@class="green-circle"])[2]//span[@class="info-label"]'))
        )
        
        labels = driver.find_elements(By.XPATH, '//span[@class="info-label"]')
        values = driver.find_elements(By.XPATH, '//span[@class="info-value"] | //div[@class="emails-list"]')

        for label, value in zip(labels, values):
            field_name = field_mapping.get(label.text.strip(), label.text.strip())
            
            if field_name == 'Email':
                try:
                    email_anchor = value.find_element(By.TAG_NAME, 'a')
                    email_value = email_anchor.get_attribute('href').replace('mailto:', '').strip()
                    additional_info[field_name] = email_value
                except NoSuchElementException:
                    additional_info[field_name] = ""
            else:
                additional_info[field_name] = value.text.strip()

    except TimeoutException:
        pass

    return additional_info

def extract_performance(driver):
    performance = {}
    
    # Mapeo de nombres de campos de scraping a nombres esperados en el modelo
    field_mapping = {
        'Sanciones del TCE': 'Sanciones_del_TCE',
        'Penalidades': 'Penalidades',
        'Inhabilitación por\nMandato Judicial': 'Inhabilitación_por_Mandato_Judicial',
        'Inhabilitación\nAdministrativa': 'Inhabilitación_Administrativa',
        'SUNAT': 'SUNAT',
        'SBS': 'SBS'
    }

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="hovertext"]'))
        )
        stars_img_element = driver.find_element(By.XPATH, '//span[@class="hovertext"]/img')
        src_value = stars_img_element.get_attribute('src')
        stars_number = int(re.search(r'img/(\d)Estrellas', src_value).group(1))
        performance["stars"] = stars_number
    except (TimeoutException, NoSuchElementException, AttributeError):
        performance["stars"] = 0

    try:
        score_legend_elements = driver.find_elements(By.XPATH, '//div[@class="score-data d-flex flex-wrap"]//span[@class="score-legend"]')
        score_value_elements = driver.find_elements(By.XPATH, '//div[@class="score-data d-flex flex-wrap"]//span[@class="score-value"]')
        
        for legend, value in zip(score_legend_elements, score_value_elements):
            legend_text = legend.text.strip()
            value_text = value.text.strip()
            
            # Mapea el nombre del campo al nombre esperado en el modelo
            field_name = field_mapping.get(legend_text, legend_text)
            performance[field_name] = value_text
    except NoSuchElementException:
        pass

    return performance

def extract_conformation_societaria(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="top-spaced border-box pt-2 pr-4 pb-2"]//div[@class="left-spaced"]'))
        )

        sections = driver.find_elements(By.XPATH, '//div[@class="top-spaced border-box pt-2 pr-4 pb-2"]//div[@class="left-spaced"]')

        section_dicts = {
            "Socios_Accionistas": {},
            "Representantes": {},
            "Órganos_de_Administración": {}
        }

        for section in sections:
            title_element = section.find_element(By.XPATH, './/span[@class="contract-title"]/strong')
            section_title = title_element.text.strip()

            contract_details = section.find_elements(By.XPATH, './/span[@class="contract-details"]')

            for detail in contract_details:
                key = detail.find_element(By.TAG_NAME, 'strong').text.strip()
                value = detail.get_attribute('innerText').replace(key, '').strip().replace('\n', ' ')
                if section_title == "Socios/Accionistas":
                    section_dicts["Socios_Accionistas"][key] = value
                elif section_title == "Representantes":
                    section_dicts["Representantes"][key] = value
                elif section_title == "Órganos de Administración":
                    section_dicts["Órganos_de_Administración"][key] = value

        # Crear la instancia de ConformationSocietaria
        conformation_societaria_instance = ConformationSocietaria(
            Socios_Accionistas=section_dicts["Socios_Accionistas"],
            Representantes=section_dicts["Representantes"],
            Organos_Administracion=section_dicts["Órganos_de_Administración"]
        )

        return [conformation_societaria_instance]

    except NoSuchElementException:
        return []
    
def clean_excel_data_value(value):
    if pd.isna(value):
        return ''
    if isinstance(value, (float, int)):
        return str(value)
    return str(value)

def download_excel(driver, download_dir: str):
    try:
        contracts = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="col-sm-12 contracts-container pt-2 pb-2"]'))
        )

        view_details_contracts = contracts.find_element(By.XPATH, '//a[@class="view-detail" and contains(@href, "/contratos")]')
        view_details_contracts.click()

        driver.implicitly_wait(20)

        download_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="excel-button"]'))
        )
        download_link.click()

        WebDriverWait(driver, 20).until(
            lambda d: any(filename.endswith('.xlsx') for filename in os.listdir(download_dir))
        )
    except TimeoutException:
        raise TimeoutException("Timeout while downloading Excel file")

    downloaded_files = glob.glob(os.path.join(download_dir, '*.xlsx'))
    if downloaded_files:
        excel_file_path = downloaded_files[0]

        try:
            df = pd.read_excel(excel_file_path)
            df = df.fillna('')

            for column in df.columns:
                df[column] = df[column].map(clean_excel_data_value)

            expected_columns = [
                "OBJETO",
                "DESCRIPCION",
                "ENTIDAD",
                "MONEDA_DEL_MONTO_DEL_CONTRATO_ORIGINAL",
                "MONTO_DEL_CONTRATO_ORIGINAL",
                "FECHA_DE_FIRMA_DE_CONTRATO",
                "FECHA_PREVISTA_DE_FIN_DE_CONTRATO",
                "MIEMBROS_CONSORCIO",
                "ESTADO"
            ]
            
            df.columns = df.columns.str.replace(' ', '_').str.upper()

            for col in expected_columns:
                if col not in df.columns:
                    df[col] = None

            df = df[expected_columns]

            return df.to_dict(orient='records')
        except Exception as e:
            print("Error reading Excel file:", e)
            return []
    else:
        print("No downloaded Excel file found.")
        return []



def get_file_state_suppliers(ruc: str):
    driver = initialize_driver(download_dir)

    try:
        navigate_to_supplier_page(driver, ruc)
        supplier_name = extract_supplier_name(driver)
        current = extract_current_tags(driver)
        additional_info = extract_additional_info(driver)
        performance = extract_performance(driver)
        conformation_societaria = extract_conformation_societaria(driver)
        excel_data = download_excel(driver, download_dir)
        
        user_data = UserByStateSupplier(
            name=supplier_name,
            current=current,
            performance=performance, 
            additional_info=additional_info,
            conformation_societaria=conformation_societaria,
            excel_data=excel_data
        )

        save_state_supplier_data(user_data)

        return user_data

    except TimeoutException as e:
        return {"error": "Timeout while waiting for elements"}
    finally:

        driver.quit()
