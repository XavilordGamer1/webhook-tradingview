from flask import Flask, request
import requests
import json

app = Flask(__name__)

TOKEN = "8761556319:AAE62wYPkQ_A5VQg0ZZwJc6pAuilDZuwrNI"
CHAT_ID = "-1003970317817"

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return "Servidor activo", 200

    # Capturamos el contenido crudo para evitar el error 400
    raw_data = request.get_data(as_text=True)
    
    try:
        # Intentamos parsear manualmente para mayor seguridad
        data = json.loads(raw_data)
        
        side = data.get('side', 'N/A')
        strength_val = data.get('prediction', data.get('strength', 0))
        strength = abs(int(float(strength_val)))
        
        # Clasificación de probabilidad mejorada
        if strength >= 7:
            prob = "🟢 ALTA PROBABILIDAD"
        elif strength >= 4:
            prob = "🟡 MEDIA PROBABILIDAD"
        else:
            prob = "🔴 ALTO RIESGO / BAJA FUERZA"

        emoji = "🚀" if "BUY" in side.upper() else "🔥"
        
        mensaje = (
            f"{emoji} <b>ALERTA DE TRADING: {side}</b> {emoji}\n"
            f"📊 <b>Probabilidad:</b> {prob} (Fuerza {strength})\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 <b>Activo:</b> {data.get('symbol', 'N/A')}\n"
            f"🎯 <b>Entrada:</b> {data.get('entry', '0')}\n"
            f"🛑 <b>Stop Loss:</b> {data.get('sl', '0')}\n"
            f"✅ <b>Take Profit:</b> {data.get('tp', '0')}\n"
            f"━━━━━━━━━━━━━━"
        )
    except Exception as e:
        # Si algo falla, el bot te avisará qué dato causó el problema
        mensaje = f"⚠️ <b>Error de Formato:</b> El servidor recibió datos incompletos.\n\nContenido recibido:\n<code>{raw_data}</code>"

    # Envío a Telegram
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"})
    
    return "OK", 200