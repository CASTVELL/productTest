from s3Utils import process_and_upload_files_s3
#from ragUtils import AddressRAG, model_name
from n8nUtils import extraer_direcciones, crear_direcciones_texto_plano, filtrar_direcciones


def main():

    process_and_upload_files_s3()

    # Inicializar y ejecutar el proceso de extracción y generación de sinónimos
    #rag = AddressRAG(model=model_name)
    #rag.process_all() Noo dio el tiempo pa implementar :(

    # Enviar archivos al webhook, extraer las direcciones y crea archivo plano con ellas
    extraer_direcciones()
    # sube las direcciones en texto plano, filtra por 90% y crea un nuevo texto plano con las direcciones filtradas
    filtrar_direcciones()




if __name__ == '__main__':
   main() 