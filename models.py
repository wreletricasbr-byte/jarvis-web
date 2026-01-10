from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ocorrencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20))
    cliente = db.Column(db.String(100))
    telefone = db.Column(db.String(30))
    local = db.Column(db.String(150))
    tipo = db.Column(db.String(50))
    urgencia = db.Column(db.String(30))
    descricao = db.Column(db.Text)
