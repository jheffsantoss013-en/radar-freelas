import requests, json, os
from bs4 import BeautifulSoup

# Carrega config
with open("config.json") as f:
    config = json.load(f)

TOKEN = os.getenv("AAGdYTsAajNK4xTpT3vgb5TmfUQikVLrr-c")
CHAT_ID = os.getenv("8269959461")

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def buscar_projetos():
    # Busca no 99freelas
    url = "https://www.99freelas.com.br/projects"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    
    projetos = []
    for card in soup.select("a[href*='/project/']")[:30]:
        titulo = card.get_text(strip=True).lower()
        link = card.get("href")
        if not link.startswith("http"):
            link = "https://www.99freelas.com.br" + link
        
        for kw in config["palavras_chave"]:
            if kw.lower() in titulo:
                projetos.append((card.get_text(strip=True), link))
                break
    return list(set(projetos))[:10]

projetos = buscar_projetos()

if projetos:
    msg = f"🚀 *Radar Freelas - {len(projetos)} novos projetos JR*\n\n"
    for titulo, link in projetos:
        msg += f"• {titulo}\n{link}\n\n"
    enviar_telegram(msg)
    print("Enviado!")
else:
    print("Nenhum projeto novo")

