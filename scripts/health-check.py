import requests
from dotenv import load_dotenv
import os

load_dotenv()

FILE_SERVICES       = os.getenv("FILE_SERVICES")
FILE_HEALTH_REPORT  = os.getenv("FILE_HEALTH_REPORT")
SLACK_WEBHOOK       = os.getenv("SLACK_WEBHOOK")

def send_slack_alert(message):
    try:
        requests.post(SLACK_WEBHOOK, json={"text": message})
    except Exception as e:
        print(f"❌ Falha ao enviar alerta para o Slack: {e}")

def health():
    with open(FILE_SERVICES, 'r') as file_services:
        urls = [line.strip() for line in file_services if line.strip()]

    with open(FILE_HEALTH_REPORT, 'w', encoding='utf-8') as report_file:
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                status_code = response.status_code
                if status_code == 200:
                    result = f"✅ [OK] {url} - Status: {status_code}"
                else:
                    result = f"⚠️ [FAIL] {url} - Status: {status_code}"
                    send_slack_alert(result)
            except Exception as e:
                result = f"❌ [ERROR] {url} - {str(e)}"

            print(result)
            report_file.write(result + "\n")

if __name__ == "__main__":
    print("🔍 Realizando o monitoramento dos endpoints...\n")
    health()
    print("\n🏁 Finalizando o monitoramento dos endpoints...")