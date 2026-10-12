import os, json, requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

with open("config.json") as f:
    config = json.load(f)

# Busca 99Freelas
url = "https://www.99freelas.com.br/projects"
params = {"q": " ".join(config["palavras_chave"])}
headers = {"User-Agent": "Mozilla/5.0"}

try:
    r = requests.get(url, params=params, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # pega os primeiros cards
    projetos = soup.select(".result-list .project")[:5]
    
    if not projetos:
        # Se não achou com filtro, manda aviso
        msg = f"🔍 Rodei no 99Freelas com: {config['palavras_chave']} - Nenhum projeto novo no momento. Vou tentar de novo às 19h!"
    else:
        msg = "🚀 *Novos freelas encontrados:*\n\n"
        for p in projetos:
            titulo = p.get_text()[:100]
            link = p.find("a")["href"] if p.find("a") else url
            msg += f"• {titulo}\n{link}\n\n"

    # Envia Telegram
    if TOKEN and CHAT_ID:
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(api_url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        print("Enviado pro Telegram")
    else:
        print("Secrets faltando")

except Exception as e:
    print(f"Erro: {e}")
