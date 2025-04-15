import subprocess
import paramiko
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações
DOCKER_IMAGE_NAME = os.getenv("DOCKER_IMAGE_NAME")
DOCKER_TAG = os.getenv("DOCKER_TAG", "latest")
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_USER = os.getenv("REMOTE_USER")
SSH_KEY_PATH = os.path.expanduser(os.getenv("SSH_KEY_PATH", "~/.ssh/id_rsa"))
APP_NAME = os.getenv("APP_NAME")
USERNAME_DOCKER_HUB = os.getenv("DOCKER_USERNAME")
PASSWORD_DOCKER_HUB = os.getenv("DOCKER_PASSWORD")

def testar_conexao_ssh():
    print(f"🔌 Testando conexão com {REMOTE_USER}@{REMOTE_HOST}...")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=REMOTE_USER, key_filename=SSH_KEY_PATH, timeout=10)
        ssh.close()
        print("✅ Conexão SSH bem-sucedida!\n")
        return True
    except Exception as e:
        print(f"❌ Falha na conexão SSH: {e}")
        return False
    
def docker_login():
    print("🔐 Realizando login no Docker Hub...")
    result = subprocess.run(
        f"echo {PASSWORD_DOCKER_HUB} | docker login -u {USERNAME_DOCKER_HUB} --password-stdin",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Falha no login: {result.stderr}")
        exit(1)
    else:
        print("✅ Login no Docker Hub realizado com sucesso!")

def run_local(command):
    print(f"🚧 Executando local: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Erro durante execução do comando:")
        print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, command)
    else:
        print(result.stdout)

def deploy_remote():
    print(f"Conectando via SSH em {REMOTE_HOST}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(REMOTE_HOST, username=REMOTE_USER, key_filename=SSH_KEY_PATH)

    cmds = [
        "sudo yum update -y",
        "sudo amazon-linux-extras enable docker",
        "sudo yum install docker -y",
        "sudo systemctl start docker",
        "sudo systemctl enable docker",
        f"sudo docker pull {DOCKER_IMAGE_NAME}:{DOCKER_TAG}",
        f"sudo docker stop {APP_NAME} || true",
        f"sudo docker rm {APP_NAME} || true",
        f"sudo docker run -d --name {APP_NAME} -p 80:80 {DOCKER_IMAGE_NAME}:{DOCKER_TAG}"
    ]

    for cmd in cmds:
        print(f"[REMOTE] {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode(), stderr.read().decode())

    ssh.close()

if __name__ == "__main__":
    if not os.path.exists(SSH_KEY_PATH):
        print(f"❌ Arquivo da chave SSH não encontrado: {SSH_KEY_PATH}")
    elif testar_conexao_ssh():
        docker_login()
        print("🚀 Iniciando deploy...")
        run_local(f"docker build -t {DOCKER_IMAGE_NAME}:{DOCKER_TAG} -f ./nginx-app/Dockerfile ./nginx-app")
        run_local(f"docker push {DOCKER_IMAGE_NAME}:{DOCKER_TAG}")
        deploy_remote()
        print("✅ Deploy concluído!")
    else:
        print("🚫 Deploy cancelado devido à falha na conexão SSH.")