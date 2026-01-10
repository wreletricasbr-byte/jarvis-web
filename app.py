import os
import time
import pywhatkit as kit
from flask import Flask, render_template, request, redirect
from datetime import datetime
from models import db, Ocorrencia

app = Flask(__name__)

# Render injeta DATABASE_URL automaticamente
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

NUMERO_WHATSAPP = "+5561992686413"

@app.route("/", methods=["GET", "POST"])
def ocorrencia():
    if request.method == "POST":
        o = Ocorrencia(
            data=datetime.now().strftime("%d/%m/%Y %H:%M"),
            cliente=request.form["cliente"],
            telefone=request.form["telefone"],
            local=request.form["local"],
            tipo=request.form["tipo"],
            urgencia=request.form["urgencia"],
            descricao=request.form["descricao"]
        )

        db.session.add(o)
        db.session.commit()

        mensagem = (
            "🚨 *NOVA OCORRÊNCIA*\n\n"
            f"👤 Cliente: {o.cliente}\n"
            f"📞 Telefone: {o.telefone}\n"
            f"📍 Local: {o.local}\n"
            f"🔧 Tipo: {o.tipo}\n"
            f"⚠️ Urgência: {o.urgencia}\n\n"
            f"📝 {o.descricao}"
        )

        kit.sendwhatmsg_instantly(NUMERO_WHATSAPP, mensagem, 20, True)
        time.sleep(5)

        return redirect("/")

    return render_template("ocorrencia.html")
@app.route("/painel")
def painel():
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.id.desc()).all()
    return render_template("painel.html", ocorrencias=ocorrencias)

