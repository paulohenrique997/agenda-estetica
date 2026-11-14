from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "agenda_estetica.db"

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True)


class Profissional(db.Model):
    __tablename__ = "profissionais"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    especialidade = db.Column(db.String(120))
    telefone = db.Column(db.String(30))
    ativo = db.Column(db.Boolean, default=True, nullable=False)


class Procedimento(db.Model):
    __tablename__ = "procedimentos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    duracao_minutos = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False, default=0)
    ativo = db.Column(db.Boolean, default=True, nullable=False)


class Agendamento(db.Model):
    __tablename__ = "agendamentos"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    procedimento_id = db.Column(db.Integer, db.ForeignKey("procedimentos.id"), nullable=False)
    data = db.Column(db.String(10), nullable=False)      # YYYY-MM-DD
    horario = db.Column(db.String(5), nullable=False)    # HH:MM
    status = db.Column(db.String(20), nullable=False, default="Agendado")
    observacoes = db.Column(db.Text)
    __table_args__ = (
        UniqueConstraint("profissional_id", "data", "horario",
                         name="uq_profissional_data_horario"),
    )


def erro(mensagem, codigo=400):
    return jsonify({"sucesso": False, "mensagem": mensagem}), codigo


def validar_texto(payload, campo):
    valor = payload.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        return None
    return valor.strip()


def serializar(modelo):
    campos = ["id"] + [c.name for c in modelo.__table__.columns if c.name != "id"]
    return {campo: getattr(modelo, campo) for campo in campos}


@app.get("/")
def inicio():
    return render_template("index.html")


@app.get("/api/clientes")
def listar_clientes():
    return jsonify([serializar(x) for x in Cliente.query.order_by(Cliente.nome).all()])


@app.post("/api/clientes")
def criar_cliente():
    payload = request.get_json(silent=True) or {}
    nome = validar_texto(payload, "nome")
    telefone = validar_texto(payload, "telefone")
    if not nome or not telefone:
        return erro("Informe nome e telefone.")
    cliente = Cliente(nome=nome, telefone=telefone,
                      email=(payload.get("email") or "").strip() or None)
    db.session.add(cliente)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return erro("Não foi possível cadastrar. Verifique se o e-mail já está em uso.", 409)
    return jsonify({"sucesso": True, "cliente": serializar(cliente)}), 201


@app.get("/api/profissionais")
def listar_profissionais():
    return jsonify([serializar(x) for x in Profissional.query.order_by(Profissional.nome).all()])


@app.post("/api/profissionais")
def criar_profissional():
    payload = request.get_json(silent=True) or {}
    nome = validar_texto(payload, "nome")
    if not nome:
        return erro("O nome do profissional é obrigatório.")
    item = Profissional(nome=nome,
                        especialidade=(payload.get("especialidade") or "").strip(),
                        telefone=(payload.get("telefone") or "").strip())
    db.session.add(item)
    db.session.commit()
    return jsonify({"sucesso": True, "profissional": serializar(item)}), 201


@app.get("/api/procedimentos")
def listar_procedimentos():
    return jsonify([serializar(x) for x in Procedimento.query.order_by(Procedimento.nome).all()])


@app.post("/api/procedimentos")
def criar_procedimento():
    payload = request.get_json(silent=True) or {}
    nome = validar_texto(payload, "nome")
    try:
        duracao = int(payload.get("duracao_minutos", 0))
        valor = float(payload.get("valor", 0))
    except (TypeError, ValueError):
        return erro("Duração e valor devem ser numéricos.")
    if not nome or duracao <= 0 or valor < 0:
        return erro("Informe nome, duração positiva e valor igual ou maior que zero.")
    item = Procedimento(nome=nome, descricao=payload.get("descricao", ""),
                        duracao_minutos=duracao, valor=valor)
    db.session.add(item)
    db.session.commit()
    return jsonify({"sucesso": True, "procedimento": serializar(item)}), 201


@app.get("/api/agendamentos")
def listar_agendamentos():
    return jsonify([serializar(x) for x in Agendamento.query.order_by(
        Agendamento.data, Agendamento.horario).all()])


@app.post("/api/agendamentos")
def criar_agendamento():
    payload = request.get_json(silent=True) or {}
    obrigatorios = ["cliente_id", "profissional_id", "procedimento_id", "data", "horario"]
    if any(payload.get(c) in (None, "") for c in obrigatorios):
        return erro("Informe cliente, profissional, procedimento, data e horário.")
    try:
        datetime.strptime(payload["data"], "%Y-%m-%d")
        datetime.strptime(payload["horario"], "%H:%M")
        cliente_id = int(payload["cliente_id"])
        profissional_id = int(payload["profissional_id"])
        procedimento_id = int(payload["procedimento_id"])
    except (ValueError, TypeError):
        return erro("IDs, data ou horário possuem formato inválido.")
    if not Cliente.query.get(cliente_id):
        return erro("Cliente não encontrado.", 404)
    if not Profissional.query.get(profissional_id):
        return erro("Profissional não encontrado.", 404)
    if not Procedimento.query.get(procedimento_id):
        return erro("Procedimento não encontrado.", 404)
    item = Agendamento(
        cliente_id=cliente_id, profissional_id=profissional_id,
        procedimento_id=procedimento_id, data=payload["data"],
        horario=payload["horario"], observacoes=payload.get("observacoes", "")
    )
    db.session.add(item)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return erro("Horário já ocupado para este profissional ou dados inválidos.", 409)
    return jsonify({"sucesso": True, "agendamento": serializar(item)}), 201


@app.patch("/api/agendamentos/<int:item_id>")
def atualizar_agendamento(item_id):
    item = db.session.get(Agendamento, item_id)
    if not item:
        return erro("Agendamento não encontrado.", 404)
    payload = request.get_json(silent=True) or {}
    if "data" in payload:
        try:
            datetime.strptime(payload["data"], "%Y-%m-%d")
        except (ValueError, TypeError):
            return erro("Data inválida. Use AAAA-MM-DD.")
        item.data = payload["data"]
    if "horario" in payload:
        try:
            datetime.strptime(payload["horario"], "%H:%M")
        except (ValueError, TypeError):
            return erro("Horário inválido. Use HH:MM.")
        item.horario = payload["horario"]
    if "status" in payload:
        if payload["status"] not in ["Agendado", "Concluído", "Cancelado"]:
            return erro("Status inválido.")
        item.status = payload["status"]
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return erro("Conflito: este horário já está ocupado.", 409)
    return jsonify({"sucesso": True, "agendamento": serializar(item)})


@app.delete("/api/agendamentos/<int:item_id>")
def excluir_agendamento(item_id):
    item = db.session.get(Agendamento, item_id)
    if not item:
        return erro("Agendamento não encontrado.", 404)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"sucesso": True, "mensagem": "Agendamento removido."})


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
