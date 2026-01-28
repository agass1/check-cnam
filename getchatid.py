import requests

TOKEN = "ТОКЕН_ИЗ_BOTFATHER"

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
resp = requests.get(url).json()

for update in resp.get("result", []):
    chat = update["message"]["chat"]
    if chat["type"] == "private":
        print("Ваш личный chat_id:", chat["id"])
        break  # берём только первый найденный
