import subprocess
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

FILE_CONTAINER_NAMES    = os.getenv("FILE_CONTAINER_NAMES")
FILE_RESTART_LOG        = os.getenv("FILE_RESTART_LOG")
SLACK_WEBHOOK           = os.getenv("SLACK_WEBHOOK")

def send_slack_alert(message):
    try:
        requests.post(SLACK_WEBHOOK, json={"text": message})
    except Exception as e:
        print(f"❌ Falha ao enviar alerta para o Slack: {e}")

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)
    return result.stdout.strip()

def log_restart(container, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{timestamp}] {container} - {status}"
    with open(FILE_RESTART_LOG, "a", encoding="utf-8") as f:
        f.write(log + "\n")

def monitoring():
    with open(FILE_CONTAINER_NAMES, "r") as file_containers:
        containers = [line.strip() for line in file_containers if line.strip()]
    
    if len(containers) == 0:
        print("❌ Nenhum container especificado.")
        return
    
    for container in containers:
        try:
            print(f"🔎 Verificando container: `{container}`")
            inspect_output = run_command(f"docker inspect {container}")
            inspect_data = json.loads(inspect_output)[0]
            is_running = inspect_data["State"]["Running"]

            if is_running:
                print(f"✅ Container `{container}` está em execução.")
            else:
                print(f"🔁 Container `{container}` está parado. Tentando reiniciar...")
                try:
                    run_command(f"docker start {container}")
                    print(f"✅ Container `{container}` reiniciado com sucesso.")
                    log_restart(container, "reiniciado com sucesso ✅")
                    send_slack_alert(f"🔁 Container `{container}` estava parado e foi *reiniciado com sucesso*! ✅")
                except Exception as restart_err:
                    print(f"❌ Falha ao reiniciar `{container}`: {restart_err}")
                    log_restart(container, "falha ao reiniciar ❌")
                    send_slack_alert(f"🚨 Falha ao reiniciar o container `{container}` ❌")
        except Exception as e:
            print(f"❌ Erro ao inspecionar `{container}`: {e}")
            log_restart(container, "não encontrado ou erro na inspeção ❌")
            send_slack_alert(f"🚨 Container `{container}` não encontrado ou erro ao inspecionar ❌")

if __name__ == "__main__":
    print("🔍 Realizando o monitoramento dos containers...\n")
    monitoring()
    print("\n🏁 Finalizando o monitoramento dos containers...")