import requests
from dotenv import load_dotenv
import os
import subprocess
import boto3
from datetime import datetime

load_dotenv()

FILE_VOLUMES_DOCKER_BACKUP      = os.getenv("FILE_VOLUMES_DOCKER_BACKUP")
SLACK_WEBHOOK                   = os.getenv("SLACK_WEBHOOK")
BACKUP_DIR                      = os.getenv("BACKUP_DIR")

AWS_ACCESS_KEY_ID               = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY           = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION                      = os.getenv("AWS_REGION")
S3_BUCKET_NAME                  = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client("s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

os.makedirs(BACKUP_DIR, exist_ok=True)

def send_slack_alert(message):
    try:
        requests.post(SLACK_WEBHOOK, json={"text": message})
    except Exception as e:
        print(f"❌ Falha ao enviar alerta para o Slack: {e}")

def upload_to_s3(file_path, volume_name):
    try:
        s3_key = f"docker-backups/{volume_name}/{os.path.basename(file_path)}"
        s3.upload_file(file_path, S3_BUCKET_NAME, s3_key)
        print(f"☁️ Enviado para S3: {s3_key}")
    except Exception as e:
        print(f"❌ Erro ao enviar para o S3: {e}")
        send_slack_alert(f":x: Falha ao enviar o backup de `{volume_name}` para o S3.\n{e}")

def volume_exists(volume_name):
    result = subprocess.run(f"docker volume inspect {volume_name}", shell=True, capture_output=True)
    return result.returncode == 0

def backup_volumes(volume_name):
    backup_path = os.path.join(BACKUP_DIR, f"{volume_name}.tar.gz")
    command = (
        f"docker run --rm "
        f"-v {volume_name}:/volume "
        f"-v {os.path.abspath(BACKUP_DIR)}:/backup "
        f"alpine sh -c \"tar czf /backup/{volume_name}.tar.gz -C /volume .\""
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Backup salvo em: {backup_path}")
        upload_to_s3(backup_path, volume_name)
    else:
        print(f"❌ Erro ao fazer backup do volume {volume_name}")
        print(result.stderr)
        send_slack_alert(f":x: Falha no backup do volume `{volume_name}`\n{result.stderr}")

def backup():
    with open(FILE_VOLUMES_DOCKER_BACKUP, 'r', ) as volumes_containers:
        volumes = [line.strip() for line in volumes_containers if line.strip()]

    for volume in volumes:
        print(f"📦 Fazendo backup do volume: {volume}...")
        if volume_exists(volume):
            backup_volumes(volume)
        else:
            print(f"⚠️ Volume não encontrado: {volume}")
            send_slack_alert(f":warning: Volume não encontrado: `{volume}`")    


if __name__ == "__main__":
    print("🔍 Realizando o backup do volume dos containers...\n")
    backup()
    print("\n🏁 Finalizando o backup do volume dos containers...")