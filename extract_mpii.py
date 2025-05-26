import os
import tarfile
import hashlib
import shutil
from datetime import datetime

# CONFIGURAÇÕES
FILE_PATH = "mpii_human_pose_v1.tar.gz"
EXTRACTION_DIR = "mpii_dataset"
LOG_FILE = "extraction_log.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
    print(message)

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def extract_tar_gz(file_path, destination):
    try:
        if not tarfile.is_tarfile(file_path):
            log("Arquivo não é um tar.gz válido.")
            return

        log(f"Iniciando extração de {file_path} para {destination}...")
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(destination)
        log("Extração concluída com sucesso.")
    except Exception as e:
        log(f"Erro ao extrair: {e}")

def organize_folders(base_dir):
    log("Organizando diretórios...")

    image_dir = os.path.join(base_dir, "images")
    annotation_dir = os.path.join(base_dir, "annotations")

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(annotation_dir, exist_ok=True)

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                shutil.move(os.path.join(root, file), os.path.join(image_dir, file))
            elif file.lower().endswith(('.mat', '.json', '.xml', '.csv')):
                shutil.move(os.path.join(root, file), os.path.join(annotation_dir, file))

    log("Organização concluída.")

def main():
    log("==== INÍCIO DO PROCESSO ====")

    if not os.path.exists(FILE_PATH):
        log(f"Arquivo não encontrado: {FILE_PATH}")
        return

    # Calcular hash SHA256
    log("Calculando SHA256 para verificação de integridade...")
    file_hash = calculate_sha256(FILE_PATH)
    log(f"SHA256: {file_hash}")

    # Extrair arquivos
    extract_tar_gz(FILE_PATH, EXTRACTION_DIR)

    # Organizar estrutura
    organize_folders(EXTRACTION_DIR)

    log("==== PROCESSO FINALIZADO ====")

if __name__ == "__main__":
    main()
