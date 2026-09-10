import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def enviar_mensagem(texto: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, data=payload, timeout=15)
