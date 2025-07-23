# main.py
from s3upload import validar_entorno, procesar_archivos

if __name__ == '__main__':
    validar_entorno()
    procesar_archivos()
