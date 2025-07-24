# uploader.py
import os
import re
import requests

# Variables globales accesibles para todas las funciones
urlExtraer = "https://miguelcas.app.n8n.cloud/webhook/extraer"
urlFiltrar = "https://miguelcas.app.n8n.cloud/webhook/filtrar"

carpeta_archivos_s3 = os.path.join(os.path.dirname(__file__), "../output/s3Files")



def crear_direcciones_texto_plano(texto: str, ruta_salida: str, nombre_archivo: str):
    """
    Crea un archivo direccionesTextoPlano.txt a partir de un texto
    con formato de response.text y lo guarda en la ruta indicada.
    """
    # Crear carpeta si no existe
    os.makedirs(ruta_salida, exist_ok=True)
    output_file = os.path.join(ruta_salida, nombre_archivo)

    # Buscar todos los pares original-homonimas
    pattern = r'"original":"(.*?)","homonimas":\[(.*?)\]'
    matches = re.findall(pattern, texto)

    with open(output_file, "w", encoding="utf-8") as f:
        for original, homonimas_str in matches:
            homonimas = re.findall(r'"(.*?)"', homonimas_str)
            f.write(f"Original: {original}\n")
            for h in homonimas:
                f.write(f"  - {h}\n")
            f.write("\n")

    print(f"Archivo creado en: {output_file}")



def filtrar_direcciones(url: str = urlFiltrar):
    """
    Sube el archivo direccionesTextoPlano.txt desde ../output/direcciones al webhook.
    Lo que reciba como respuesta se guarda en ../output/direccionesFiltradas/direccionesFiltradas.txt
    """
    # Ruta del archivo a subir
    archivo_origen = os.path.join(os.path.dirname(__file__), "../output/direcciones/direccionesTextoPlano.txt")

    if not os.path.exists(archivo_origen):
        print(f"No se encontró el archivo a subir: {archivo_origen}")
        return

    try:
        with open(archivo_origen, "rb") as f:
            files = {"file": (os.path.basename(archivo_origen), f)}
            print(f"Enviando archivo al webhook {url}...")
            response = requests.post(url, files=files)

        if response.status_code == 200:
            print("Respuesta guardada en:", response.text)
            # Guardar respuesta
            carpeta_destino = os.path.join(os.path.dirname(__file__), "../output/direccionesFiltradas")
            os.makedirs(carpeta_destino, exist_ok=True)
            archivo_destino = os.path.join(carpeta_destino, "direccionesFiltradas.txt")
            with open(archivo_destino, "w", encoding="utf-8") as f_out:
                f_out.write(response.text)
            print(f"Respuesta guardada en: {archivo_destino}")
        else:
            print(f"Error al enviar archivo: {response.status_code} - {response.text}")

    except Exception as e:
        print(f" Ocurrió un error al subir y filtrar direcciones: {e}")



def extraer_direcciones(url: str = urlExtraer, carpeta: str = carpeta_archivos_s3, extension_filtro: str = None):
    """
    Envía todos los archivos de una carpeta a un webhook mediante POST multipart/form-data.

    Si recibe 200, extrae las direcciones del texto de respuesta y crea un archivo plano con ellas.

    Parámetros:
        url (str): URL del webhook al que se enviarán los archivos.
        carpeta (str): Ruta a la carpeta que contiene los archivos.
        extension_filtro (str, opcional): Si se indica, solo envía archivos con esa extensión (por ejemplo ".pdf").
    """


    files = []
    try:
        # Construcción de la lista de archivos
        for nombre in os.listdir(carpeta):
            ruta = os.path.join(carpeta, nombre)
            if os.path.isfile(ruta):
                if extension_filtro and not nombre.lower().endswith(extension_filtro.lower()):
                    continue
                files.append(("files", (nombre, open(ruta, "rb"))))

        print(f"Enviando {len(files)} archivos al webhook {url}...")
        response = requests.post(url, files=files)
        print("Código de estado:", response.status_code)
        print("Respuesta del webhook:", response.text)

        if response.status_code == 200:
            print("Archivos enviados correctamente.")
            crear_direcciones_texto_plano(response.text, os.path.join(os.path.dirname(__file__), "../output/Direcciones"), "direccionesTextoPlano.txt")
        else:
            print(f"Error al enviar archivos: {response.status_code} - {response.text}")

    finally:
        # Cerrar todos los archivos abiertos
        for _, file_tuple in files:
            file_tuple[1].close()
    