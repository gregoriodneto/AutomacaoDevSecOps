import requests
import time

time.sleep(5)

print("Fazendo requisição para o servidor Go...")
res = requests.get("http://go-server:8080")
print("Resposta do servidor:", res.text)