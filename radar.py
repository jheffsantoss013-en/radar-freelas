import os, requests

token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print(f"Token existe? {bool(token)}")
print(f"Chat ID: {chat_id}")

if token and chat_id:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={"chat_id": chat_id, "text": "✅ TESTE OK! Radar conectado. ID 8269959461"})
    print(f"Status: {r.status_code}")
    print(f"Resposta: {r.text}")
else:
    print("FALTA SECRET")
