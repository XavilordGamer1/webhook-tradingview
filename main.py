from flask import Flask, request
import requests
import json

app = Flask(__name__)

TOKEN = "8761556319:AAE62wYPkQ_A5VQg0ZZwJc6pAuilDZuwrNI"
CHAT_ID = "-1003970317817"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Intentamos leer el JSON que envía tu estrategia
        data = request.get_json(force=True)
        
        # Formateamos el mensaje para que se vea profesional en Notifyforex
        emoji = "🚀" if data['side'] == "BUY" else "🔥"
        fuerza = "⭐" * (int(abs(float(data['prediction']))) // 2) # Estrellas según fuerza

        mensaje = (
            f"{emoji} <b>NUEVA SEÑAL: {data['side']}</b> {emoji}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 <b>Activo:</b> {data['symbol']} ({data['timeframe']})\n"
            f"💪 <b>Fuerza ML:</b> {data['strength']} {fuerza}\n"
            f"🎯 <b>Entrada:</b> {data['entry']}\n"
            f"🛑 <b>Stop Loss:</b> {data['sl']}\n"
            f"✅ <b>Take Profit:</b> {data['tp']}\n"
            f"━━━━━━━━━━━━━━\n"
            f"<i>Lorentzian Classification Strategy</i>"
        )
    except Exception as e:
        # Si no es JSON (una prueba simple), enviamos el texto tal cual
        mensaje = request.get_data(as_text=True)

    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)