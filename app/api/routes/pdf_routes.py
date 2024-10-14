from fastapi import APIRouter, UploadFile, File, HTTPException
from app.crud.pdf_utils import save_pdf, convert_pdf_to_image, ocr_images

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """
        Carga de un archivo PDF con imagenes y lo almacena en la raiz del backend dentro de la carpeta uploads.
    Args:
        debemos enviar un form-data con la "key" -> file.

    Returns:
        Dict: Diccionario con un mensaje y la ruta donde se almaceno el archivo.
    """
    try:
        pdf_path = save_pdf(file)
        return {"message": "PDF uploaded successfully", "pdf_path": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/convert_pdf_to_image/")
async def convert_pdf_to_image_endpoint():
    """
       En este paso solo debemos ejecutar una peticion POST a la ruta y el codigo se encarga de procesar cada pagina del PDF y convertirlas a imagenes.
    Args:
        Ninguno.

    Returns:
        Dict: Diccionario con un mensaje y la ruta donde se almacenaron las imagenes.
    """
    try:
        images = convert_pdf_to_image()
        return {"message": "PDF converted to images successfully", "image_paths": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/extract_text_from_pdf/")
async def ocr_images_endpoint():
    """
        Antes de ejecutar la peticion debes verificar que tengas instalado en tu sistema operativo Tesseract.
        En mi caso tengo Windows, lo descargue desde aqui: https://github.com/UB-Mannheim/tesseract/wiki

        Una vez que tengamos instalado Tesseract en nuestro sistema operativo, nos dirigimos a la carpeta de instalacion,
        en mi caso tuve que navegar hasta: /equipo/C/Users/exede/AppData/local/Programs/Tesseract-OCR (dentro de exede habilite la opcion para que muestre los archivos ocultos.)

        Copiamos la direccion y nos vamos a nuestras variables de entorno y agregamos esta direccion a nuestro path.
        Luego abrimos nuestra CMD y corremos el siguiente comando -> tesseract, nos deberia salir algo como esto:
        
        C:\Windows\system32>tesseract
        Usage:
        tesseract --help | --help-extra | --version
        tesseract --list-langs
        tesseract imagename outputbase [options...] [configfile...] ...
    Args:
        Ninguno, solo ejecutamos la peticion POST a la ruta.

    Returns:
        Dict: Diccionario con el texto de cada imagen separados uno del otro.
    """
    try:
        ocr_results = ocr_images()
        return {"message": "OCR performed successfully", "ocr_results": ocr_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))