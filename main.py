from flask import Flask, request
import requests

app = Flask(__name__)

# Datos confirmados por tu prueba
TOKEN = "8761556319:AAE62wYPkQ_A5VQg0ZZwJc6pAuilDZuwrNI"
CHAT_ID = "-1003970317817"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recibe la señal de TradingView
    data = request.get_data(as_text=True)
    
    payload = {
        "chat_id": CHAT_ID,
        "text": data,
        "parse_mode": "HTML"
    }
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    return "Recibido", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)