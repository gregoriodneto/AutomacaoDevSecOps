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