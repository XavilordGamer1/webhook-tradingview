from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8761556319:AAE62wYPkQ_A5VQg0ZZwJc6pAuilDZuwrNI"
CHAT_ID = "-1003970317817"

@app.route('/webhook', methods=['GET', 'POST']) # Agregamos GET para probar
def webhook():
    if request.method == 'GET':
        # Esto es lo que pasará cuando entres desde el navegador
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": "✅ Prueba desde el Navegador: ¡El servidor está VIVO!"})
        return "Servidor funcionando", 200

    try:
        data = request.get_json(force=True)
        emoji = "🚀" if data.get('side') == "BUY" else "🔥"
        mensaje = (
            f"{emoji} <b>NUEVA SEÑAL: {data.get('side')}</b> {emoji}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 <b>Activo:</b> {data.get('symbol')}\n"
            f"🎯 <b>Entrada:</b> {data.get('entry')}\n"
            f"🛑 <b>Stop Loss:</b> {data.get('sl')}\n"
            f"✅ <b>Take Profit:</b> {data.get('tp')}\n"
            f"━━━━━━━━━━━━━━"
        )
    except Exception as e:
        # Si el JSON falla, enviamos el error para saber qué pasó
        mensaje = f"⚠️ Error en datos recibidos: {str(e)}\nContenido: {request.get_data(as_text=True)}"

    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    return "OK", 200