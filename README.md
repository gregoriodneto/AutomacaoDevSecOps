# DevOps Automation Scripts

Este repositório contém scripts em Python para automação de tarefas DevOps, como deploy, gerenciamento de containers, SSH remoto e mais.

## Estrutura

- `scripts/`: Pasta com todos os scripts.
- `.env`: Arquivo com variáveis sensíveis (NÃO subir no Git).
- `.env.example`: Modelo de variáveis.
- `requirements.txt`: Dependências Python.

## Como usar

1. Clone o repositório
2. Crie seu `.env` com base no `.env.example`
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Execute o script:
```bash
python scripts/deploy.py
```

## Scripts disponíveis

- `deploy.py`: Faz build, push e deploy remoto via SSH com Docker.
- `health-check.py`: Verifica a saúde de endpoints listados em um arquivo .txt, registra os resultados e envia alertas para o Slack em caso de falhas.
- `auto-restart.py`: Monitora containers Docker listados em um arquivo `.txt` e reinicia automaticamente os que estiverem com problemas.
- `space-disk-monitoring.py`: Conecta via SSH a um servidor remoto, verifica o uso de disco com `df -h`, salva um relatório e envia alerta para o Slack se alguma partição estiver acima de 80% de uso.


## Exemplo de .env.example
```bash
# Deploy Docker e AWS
DOCKER_IMAGE_NAME=my-image
DOCKER_TAG=latest
DOCKER_USERNAME=my-docker-user
DOCKER_PASSWORD=my-docker-pass
REMOTE_HOST=192.168.0.1
REMOTE_USER=ec2-user
SSH_KEY_PATH=~/.ssh/id_rsa
APP_NAME=my-app

# Health Check
FILE_SERVICES=scripts/services.txt
FILE_HEALTH_REPORT=scripts/health_report.txt
SLACK_WEBHOOK=https://hooks.slack.com/services/SEU/WEBHOOK/URL

# Monitoring Containers Auto Restart
FILE_CONTAINER_NAMES=
FILE_RESTART_LOG=

# Space disk monitoring
FILE_DISK_REPORT=
```