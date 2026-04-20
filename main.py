from flask import Flask, request
import requests

app = Flask(__name__)

# Tus credenciales
TOKEN = "8761556319:AAE62wYPkQ_A5VQg0ZZwJc6pAuilDZuwrNI"
CHAT_ID = "-1003970317817"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": "✅ Prueba desde el Navegador: ¡El servidor está VIVO!"})
        return "Servidor funcionando", 200

    try:
        data = request.get_json(force=True)
        side = data.get('side', 'UNKNOWN')
        emoji = "🚀" if side == "BUY" else "🔥"
        
        # --- NUEVA LÓGICA DE PROBABILIDAD ---
        # Leemos la fuerza (prediction) y la pasamos a número positivo con abs()
        fuerza_cruda = data.get('strength', data.get('prediction', 0))
        strength = abs(int(float(fuerza_cruda))) 
        
        if strength >= 7:
            probabilidad = "🟢 ALTA PROBABILIDAD"
        elif strength >= 4:
            probabilidad = "🟡 MEDIA PROBABILIDAD"
        else:
            probabilidad = "🔴 ALTO RIESGO"
        # ------------------------------------

        mensaje = (
            f"{emoji} <b>NUEVA SEÑAL: {side}</b> {emoji}\n"
            f"📊 <b>Filtro ML:</b> {probabilidad} (Fuerza {strength})\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 <b>Activo:</b> {data.get('symbol')}\n"
            f"🎯 <b>Entrada:</b> {data.get('entry')}\n"
            f"🛑 <b>Stop Loss:</b> {data.get('sl')}\n"
            f"✅ <b>Take Profit:</b> {data.get('tp')}\n"
            f"━━━━━━━━━━━━━━"
        )
    except Exception as e:
        mensaje = f"⚠️ Error en datos recibidos: {str(e)}\nContenido: {request.get_data(as_text=True)}"

    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    return "OK", 200