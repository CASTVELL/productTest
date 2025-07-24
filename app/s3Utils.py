# s3_uploader.py
import os
import hashlib
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Cargar variables de entorno
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'sa-east-1')

BUCKET = os.getenv('S3_BUCKET')
LOCAL_DIR = os.getenv('LOCAL_DIR', 's3Files')
STATE_FILE = os.getenv('STATE_FILE', 'state.json')

# Validar variables de entorno requeridas
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not BUCKET:
    logging.error("Faltan variables de entorno requeridas (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET).")
    raise SystemExit(1)

# Inicializar cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Cargar o inicializar estado con manejo de errores
try:
    if Path(STATE_FILE).exists():
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {'hashes': []}
except (json.JSONDecodeError, OSError) as e:
    logging.warning(f"No se pudo leer el archivo de estado, se inicializa uno nuevo. Error: {e}")
    state = {'hashes': []}

# Usar un conjunto para búsqueda más rápida
hash_set = set(state.get('hashes', []))


def file_hash(path, chunk_size=8192):
    """Calcula SHA256 de un archivo."""
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha.update(chunk)
    return sha.hexdigest()


def upload_file(path: Path, key: str) -> bool:
    """Sube un archivo individual a S3."""
    try:
        s3.upload_file(str(path), BUCKET, key)
        logging.info(f"Subido: {key}")
        return True
    except ClientError as e:
        logging.error(f"Error subiendo {key}: {e}")
        return False


def process_and_upload_files_s3(local_dir: str = LOCAL_DIR):
    """
    Procesa todos los archivos en `local_dir` y los sube a S3 si no están duplicados.
    """
    base = Path(local_dir)
    if not base.exists():
        logging.error(f"El directorio local {local_dir} no existe.")
        return

    for file in base.rglob('*'):
        if file.is_file():
            h = file_hash(file)
            if h in hash_set:
                logging.info(f"Omitido (duplicado): {file}")
                continue

            key = str(file.relative_to(base))
            if upload_file(file, key):
                hash_set.add(h)
                state['hashes'].append(h)
                # Guardar estado incremental
                try:
                    with open(STATE_FILE, 'w') as f:
                        json.dump(state, f, indent=2)
                except OSError as e:
                    logging.error(f"Error guardando el estado en {STATE_FILE}: {e}")

    logging.info("Proceso completado.")
