import os
import pandas as pd
import requests

from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# ================= CONFIGURAÇÕES =================
ARQUIVO = "dados/ocorrencias.xlsx"

# DADOS WHATSAPP CLOUD API
WHATSAPP_TOKEN = "COLE_SEU_TOKEN_AQUI"
PHONE_NUMBER_ID = "COLE_SEU_PHONE_ID_AQUI"
DESTINO = "5561992686413"
# =================================================

# ---------- GARANTE PASTA ----------
if not os.path.exists("dados"):
    os.makedirs("dados")

# ---------- GARANTE PLANILHA ----------
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=[
        "Data",
        "Cliente",
        "Telefone",
        "Local",
        "Tipo",
        "Urgencia",
        "Descricao"
    ])
    df.to_excel(ARQUIVO, index=False)

# ---------- FUNÇÃO ENVIO WHATSAPP ----------
def enviar_whatsapp(mensagem):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": DESTINO,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    requests.post(url, headers=headers, json=payload)

# ---------- ROTA PRINCIPAL ----------
@app.route("/", methods=["GET", "POST"])
def ocorrencia():
    if request.method == "POST":
        cliente = request.form["cliente"]
        telefone = request.form["telefone"]
        local = request.form["local"]
        tipo = request.form["tipo"]
        urgencia = request.form["urgencia"]
        descricao = request.form["descricao"]

        data = datetime.now().strftime("%d/%m/%Y %H:%M")

        df = pd.read_excel(ARQUIVO, engine="openpyxl")

        df.loc[len(df)] = [
            data, cliente, telefone, local,
            tipo, urgencia, descricao
        ]

        df.to_excel(ARQUIVO, index=False)

        mensagem = (
            "🚨 *NOVA OCORRÊNCIA*\n\n"
            f"👤 Cliente: {cliente}\n"
            f"📞 Telefone: {telefone}\n"
            f"📍 Local: {local}\n"
            f"🔧 Tipo: {tipo}\n"
            f"⚠️ Urgência: {urgencia}\n\n"
            f"📝 {descricao}"
        )

        enviar_whatsapp(mensagem)

        return redirect("/")

    return render_template("ocorrencia.html")

# ---------- INICIALIZAÇÃO (DETALHE QUE FALTAVA) ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
