from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, Email, DataRequired,ValidationError
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///geren_servicos.db"
app.config["SECRET_KEY"] = "hu6&hfg756@ui673%467"

db = SQLAlchemy(app)

# Modelos
class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=50), nullable=False, unique=True)
    telefone = db.Column(db.String(length=11), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    endereco = db.Column(db.String(length=50))

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False, unique=True)
    preco = db.Column(db.Integer, nullable=False)
    duracao = db.Column(db.String(length=50), nullable=False)

class Agendamento(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.String(length=50), nullable=False, unique=True)
    id_servico = db.Column(db.String(length=50), nullable=False, unique=False)
    id_data = db.Column(db.String(length=11), nullable=False)
    hora = db.Column(db.String(length=5), nullable=False)
    status = db.Column(db.String(length=10), nullable=False)

# Formulário
class ClientesForm(FlaskForm):
    def validate_nome(self, check_nome):
        nome = Cliente.query.filter_by(nome=check_nome.data).first()
        if nome:
            raise ValidationError("nome de usuário já existe, tente outro nome de usuário")
            
    def validate_telefone(self, check_telefone):
        telefone = Cliente.query.filter_by(telefone=check_telefone.data).first()
        if telefone:
            raise ValidationError("telefone já existe, tente outro número de telefone")
            
    def validate_email(self, check_email):
        email = Cliente.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError("email já existe, tente outro email por favor")
    
    nome = StringField(label="Nome", validators=[Length(max=60), DataRequired()])
    telefone = StringField(label="Telefone", validators=[Length(max=11), DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    endereco = StringField(label="Endereço", validators=[Length(max=70), DataRequired()])
    submit = SubmitField(label="Cadastrar")
    
class Agendamento_servisso(FlaskForm):
  def validate_agendamento(self, check_agenda):
        agendam = Agendamento.query.filter_by(id_cliente=check_agenda.data).first()
        if agendam:
            raise ValidationError("nome de usuário já existe, tente outro nome de usuário")
            
    
  cliente = StringField(label="Nome do Cliente", validators=[Length(max=60),DataRequired()])
  servico = StringField(label="Tipo de Serviço",validators=[Length(max=1043),DataRequired()])
  Data_servico = StringField(label="Data do Agendamento",validators=[Length(max=10),DataRequired()])
  hora = StringField(label="Horario para realização do seviço",validators=[Length(max=5),DataRequired()])
  status = StringField(label="Status", validators=[Length(max=103),DataRequired()])
  submit = SubmitField(label="agendar Serviço",)

    
class Loginform(FlaskForm):
    usuario = StringField(label="usuario", validators=[DataRequired()])
    senha = PasswordField(label="senha", validators=[DataRequired()])
    submit = SubmitField(label="log in", validators=[DataRequired()])

# Rotas
@app.route("/")
def home_page():
  total_clientes = Cliente.query.count()
  total_agenda = Agendamento.query.count()
  return render_template("index.html", total_clientes=total_clientes, total_agenda=total_agenda)

@app.route("/clientes")
def clientes_page():
    cliente = Cliente.query.all()
    return render_template("Clientes.html",cliente=cliente)

@app.route("/servicos")
def servico_page():
    return render_template("Servicos.html")

@app.route("/Agendar")
def agendamento_page():
  agend = Agendamento.query.all()
  return render_template("Agendamentos.html",agend=agend)

@app.route("/agendamentos", methods=["POST", "GET"])
def form_agendamento_page():
    form = Agendamento_servisso()
    if form.validate_on_submit():
      agen = Agendamento(
          id_cliente = form.cliente.data,
          id_servico = form.servico.data,
          id_data = form.Data_servico.data,
          hora = form.hora.data,
          status = form.status.data
        )
      db.session.add(agen)
      db.session.commit()
      flash("agendamento realizado com sucesso",category="success" )
      return redirect(url_for("agendamento_page"))
      if form.errors != {}:
        for err in form.errors.values():
            flash(f"{err}", category="danger")
    return render_template("agendar.html",form=form)

@app.route("/cad_cliente", methods=["POST", "GET"])
def cadastro_cliente():
    form = ClientesForm()
    if request.method == "POST" and form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            telefone=form.telefone.data,
            email=form.email.data,
            endereco=form.endereco.data
        )
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", category="info")
        return redirect(url_for("clientes_page"))
   
    if form.errors != {}:
      for err in form.errors.values():
         flash(f"{err}", category="danger")
    return render_template("form-cliente.html",form=form)
    
@app.route("/login")
def Login_user():
  form = Loginform()
  return render_template("login_page.html",form=form)
  
@app.route('/delete/<int:agendamento_id>', methods=['POST'])
def delete_agendamento(agendamento_id):
    agendamento = Agendamento.query.get(agendamento_id)
    if agendamento:
        db.session.delete(agendamento)
        db.session.commit()
        flash('Agendamento excluído com sucesso!', 'success')
    else:
        flash('Agendamento não encontrado.', 'danger')
    return redirect(url_for('agendamento_page'))
    
    
@app.route('/delete/<int:cliente_id>', methods=['POST'])
def delete_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        flash('cliente excluído', 'success')
    else:
        flash('cliente não encontrado.', 'danger')
    return redirect(url_for('clientes_page'))
    

# Inicialização do Banco de Dados
if __name__ == "__main__":
  with app.app_context():
    db.create_all()  #cria as tabelas
  app.run(debug=True)