import os

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Página do formulário
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

        return redirect("/")

    return render_template("ocorrencia.html")

# Painel administrativo
@app.route("/painel")
def painel():
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.id.desc()).all()
    return render_template("painel.html", ocorrencias=ocorrencias)

if __name__ == "__main__":
    app.run()
