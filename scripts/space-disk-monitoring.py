import requests
from dotenv import load_dotenv
import os
import paramiko

load_dotenv()

REMOTE_HOST         = os.getenv("REMOTE_HOST")
REMOTE_USER         = os.getenv("REMOTE_USER")
SSH_KEY_PATH        = os.path.expanduser(os.getenv("SSH_KEY_PATH", "~/.ssh/id_rsa"))
SLACK_WEBHOOK       = os.getenv("SLACK_WEBHOOK")
FILE_DISK_REPORT    = os.getenv("FILE_DISK_REPORT", "disk_report.txt")

def send_slack_alert(message):
    try:
        requests.post(SLACK_WEBHOOK, json={"text": message})
    except Exception as e:
        print(f"❌ Falha ao enviar alerta para o Slack: {e}")

def connecting_ssh():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=REMOTE_USER, key_filename=SSH_KEY_PATH, timeout=10)
        print("✅ Conexão SSH bem-sucedida!\n")

        stdin, stdout, stderr = ssh.exec_command("df -h")
        output = stdout.read().decode()
        ssh.close()

        print("📊 Uso do disco:\n")
        print(output)

        with open(FILE_DISK_REPORT, "w", encoding="utf-8") as f:
            f.write(output)

        alert_lines = []
        for line in output.splitlines()[1:]:
            try:
                usage_percent = int(line.split()[4].replace("%", ""))
                if usage_percent >= 80:
                    alert_lines.append(f"📁 `{line.split()[0]}` está usando *{usage_percent}%*")
            except (IndexError, ValueError):
                continue
        
        if alert_lines:
            alert_message = "🚨 *Alerta de uso de disco alto* 🚨\n\n" + "\n".join(alert_lines)
            print(alert_message)
            send_slack_alert(alert_message)
        else:
            print("✅ Nenhuma partição está com uso crítico de disco.")

    except Exception as e:
        print(f"❌ Falha na conexão SSH: {e}")

if __name__ == "__main__":
    print("🔐 Conectando via SSH à máquina remota...\n")
    connecting_ssh()
    print("\n🏁 Finalizando conexão com a máquina.")