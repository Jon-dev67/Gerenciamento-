# fazendo importações para construir aplicação
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, Email, DataRequired,ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
import csv
from flask import make_response
from fpdf import FPDF

#configurando a aplicção
app = Flask(__name__)
login_manager = LoginManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///geren_servicos.db"
app.config["SECRET_KEY"] = "hu6&hfg756@ui673%467"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view="page_login"
login_manager.login_message="por favor faça o login"
login_manager.login_message_category="info"

#rota que gerencia o login e verifica se o usuario esta logado 
@login_manager.user_loader
def load_user(user_id):
    return Usu.query.get(int(user_id))

# Modelos
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=50), nullable=False, unique=True)
    telefone = db.Column(db.String(length=11), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    endereco = db.Column(db.String(length=50))
    user_id = db.Column(db.Integer, db.ForeignKey('usu.id'), nullable=False)  # Adiciona a referência
    user = db.relationship('Usu', backref=db.backref('clientes', lazy=True))

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False, unique=True)
    preco = db.Column(db.Integer, nullable=False)
    duracao = db.Column(db.String(length=50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usu.id'), nullable=False)  # Adiciona a referência
    user = db.relationship('Usu', backref=db.backref('agend_servico', lazy=True))

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.String(length=50), nullable=False)
    id_servico = db.Column(db.String(length=50), nullable=False)
    id_data = db.Column(db.String(length=11), nullable=False)
    hora = db.Column(db.String(length=5), nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usu.id'), nullable=False)  # Adiciona a referência
    user = db.relationship('Usu', backref=db.backref('agendamentos', lazy=True))
    
class Usu(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  usuario = db.Column(db.String(length=50), nullable=False, unique=True)
  email = db.Column(db.String(length=50), nullable=False, unique=True)
  senha = db.Column(db.String(length=50), nullable=False, unique=False)
#criptografando senha com flask_bcrypt  
  @property
  def senhacrip(self):
      return self.senhacrip

  @senhacrip.setter
  def senhacrip(self, password_text):
      self.senha = bcrypt.generate_password_hash(password_text).decode('utf-8')
#convertendo senha para "texto claro" para checar senha para ver se ja esta no canvi de dados        
  def converte_senha(self,senha_texto_claro):
      return bcrypt.check_password_hash(self.senha,senha_texto_claro)
  

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
    
class Editar_clientesForm(FlaskForm):
  nome = StringField(label="Nome", validators=[Length(max=60), DataRequired()])
  telefone = StringField(label="Telefone", validators=[Length(max=11), DataRequired()])
  email = StringField(label="Email", validators=[Email(), DataRequired()])
  endereco = StringField(label="Endereço", validators=[Length(max=70), DataRequired()])
  submit = SubmitField(label="editar dados do cliente")
  
    
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
  
  class editar_agendamento_servisso(FlaskForm):
    cliente = StringField(label="Nome do Cliente", validators=[Length(max=60),DataRequired()])
    servico = StringField(label="Tipo de Serviço",validators=[Length(max=1043),DataRequired()])
    Data_servico = StringField(label="Data do Agendamento",validators=[Length(max=10),DataRequired()])
    hora = StringField(label="Horario para realização do seviço",validators=[Length(max=5),DataRequired()])
    status = StringField(label="Status", validators=[Length(max=103),DataRequired()])
    submit = SubmitField(label="agendar Serviço",)

    
class Loginform(FlaskForm):
  usuario = StringField(label="usuario",validators=[DataRequired(),Length(max=60)])
  senha = PasswordField(label="senha", validators=[DataRequired()])
  submit = SubmitField(label="log in")
    
class Usuarios(FlaskForm):
  def validate_email(self, check_email):
        email = Usu.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError("email já existe, tente outro email por favor")

          
  def validate_usuario(self, check_usuario):
        usuario = Usu.query.filter_by(usuario=check_usuario.data).first()
        if usuario:
            raise ValidationError("usuario já existe, tente outro nome de usuario")
            
  def validate_senha(self, check_senha):
        senha = Usu.query.filter_by(senha=check_senha.data).first()
        if senha:
            raise ValidationError("senha já cadastrada, tente outra senha por favor")
  usuario = StringField(label="usuario", validators=[DataRequired()])
  email = StringField(label="email", validators=[DataRequired()])
  senha = PasswordField(label="senha", validators=[DataRequired()])
  submit = SubmitField(label="cadastrar")
  
  
class Cad_servico(FlaskForm):
  descricao = StringField(label="fassa uma descrição sobre o serviço.", validators=[DataRequired()])
  preco = StringField(label="quanto dezeja cobrar pelo serviço?", validators=[DataRequired()])
  duracao = StringField(label="quanto tempo em media leva para o serviço ficar pronto?", validators=[DataRequired()])
  submit = SubmitField(label="cadastrar serviço")
  

# Rotas
@app.route("/")
def home_page():
  total_clientes = Cliente.query.count()
  total_agenda = Agendamento.query.count()
  return render_template("Index.html", total_clientes=total_clientes, total_agenda=total_agenda)

@app.route("/clientes")
@login_required
def clientes_page():
    cliente = Cliente.query.filter_by(user_id=current_user.id).all()
    return render_template("Clientes.html",cliente=cliente)

@app.route("/servicos",methods=["POST","GET"])
@login_required
def servico_page():
  form = Cad_servico()
  if form.validate_on_submit():
    add_dados = Servico(
      descricao = form.descricao.data,
      preco = form.preco.data,
      duracao = form.duracao.data,
      user_id=current_user.id
      )
    db.session.add(add_dados)
    db.session.commit()
    flash("serviço cadastrado com sucesso!",category="success")
    return redirect(url_for("Servico_agendamento"))
  return render_template("Servicos.html",form=form)
  
@app.route("/serv-agendado")
@login_required
def Servico_agendamento():
  agend = Servico.query.filter_by(user_id=current_user.id).all()
  return render_template("servicos-cadastrados.html",agend=agend)

@app.route("/Agendar")
@login_required
def agendamento_page():
  agend = Agendamento.query.filter_by(user_id=current_user.id).all()
  return render_template("Agendamentos.html",agend=agend)

@app.route("/agendamentos", methods=["POST", "GET"])
@login_required
def form_agendamento_page():
    form = Agendamento_servisso()
    if form.validate_on_submit():
      agen = Agendamento(
          id_cliente = form.cliente.data,
          id_servico = form.servico.data,
          id_data = form.Data_servico.data,
          hora = form.hora.data,
          status = form.status.data,
          user_id=current_user.id
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
@login_required
def cadastro_cliente():
    form = ClientesForm()
    if request.method == "POST" and form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            telefone=form.telefone.data,
            email=form.email.data,
            endereco=form.endereco.data,
            user_id=current_user.id
        )
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", category="info")
        return redirect(url_for("clientes_page"))
   
    if form.errors != {}:
      for err in form.errors.values():
         flash(f"{err}", category="danger")
    return render_template("form-cliente.html",form=form)
    

  
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
    


@app.route('/delete_clientes/<int:id_cliente>', methods=['POST'])
def delete_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        flash('cliente deletado com sucesso!', 'success')
    else:
        flash('cliente não encontrado.', 'danger')
    return redirect(url_for('clientes_page')) 
     
@app.route("/cad_usuario", methods=["POST", "GET"])
def cad_usu_page():
    form = Usuarios()
    if form.validate_on_submit():
        novo_usuario = Usu(
            usuario=form.usuario.data,
            email=form.email.data
        )
        novo_usuario.senhacrip = form.senha.data  # Criptografa a senha
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso!",category="success")
        return redirect(url_for("home_page"))

    if form.errors != {}:
        for err in form.errors.values():
            flash(f"{err}", category="danger")
    return render_template("cad_usuarios_page.html", form=form)


@app.route("/login", methods=["GET","POST"])
def page_login():
    form = Loginform()
    if form.validate_on_submit():
        usuario_logado = Usu.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            flash(f"login realizado com sucesso! Olá  {usuario_logado.usuario}",category="success")
            return redirect(url_for("home_page"))      
        else:
            flash(f"senha ou email inválido", category="danger")
    return render_template("login_page.html",form=form)

@app.route("/logout")
def page_logout():
  logout_user()
  flash(f"até logo", category="info")
  return redirect(url_for("home_page"))
  
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
  editar = Agendamento.query.get_or_404(id)
  if request.method == "POST":
    editar.id_cliente = request.form["id_cliente"]
    editar.id_servico = request.form["id_servico"]
    editar.id_data = request.form["id_data"]
    editar.hora = request.form["hora"]
    editar.status = request.form["status"]
    db.session.commit()
    flash("alterações realizadas com sucesso!",category="success")
    return redirect(url_for("agendamento_page"))
  return render_template("page_editar_angendamento.html",editar=editar)
  
  
@app.route("/cliente_update/<int:id>", methods=["GET", "POST"])
def update_Cliente(id):
  editar = Cliente.query.get_or_404(id)
  if request.method == "POST":
    editar.nome = request.form["nome"]
    editar.telefone = request.form["telefone"]
    editar.email = request.form["email"]
    editar.endereco = request.form["endereco"]
    db.session.commit()
    flash("alterações realizadas com sucesso!",category="success")
    return redirect(url_for("clientes_page"))
  return render_template("form_editar_clientes.html",editar=editar)


import csv
import io
from flask import make_response

@app.route("/download/csv/<string:modelo>")
@login_required
def download_csv(modelo):
    if modelo == "clientes":
        dados = Cliente.query.filter_by(user_id=current_user.id).all()
        headers = ["ID", "Nome", "Telefone", "Email", "Endereço"]
        rows = [[dado.id, dado.nome, dado.telefone, dado.email, dado.endereco] for dado in dados]
    elif modelo == "agendamentos":
        dados = Agendamento.query.filter_by(user_id=current_user.id).all()
        headers = ["ID", "Cliente", "Serviço", "Data", "Hora", "Status"]
        rows = [[dado.id, dado.id_cliente, dado.id_servico, dado.id_data, dado.hora, dado.status] for dado in dados]
    else:
        flash("Modelo inválido!", category="danger")
        return redirect(url_for("home_page"))

    # Usar io.StringIO para criar um buffer de arquivo em memória
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)  # Escreve os cabeçalhos no CSV
    writer.writerows(rows)    # Escreve os dados no CSV
    output.seek(0)  # Move o cursor para o início do arquivo

    # Configurar a resposta para download
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={modelo}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route("/download/pdf/<string:modelo>")
@login_required
def download_pdf(modelo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if modelo == "clientes":
        dados = Cliente.query.filter_by(user_id=current_user.id).all()
        pdf.cell(200, 10, txt="Lista de Clientes", ln=True, align="C")
        for dado in dados:
            pdf.cell(200, 10, txt=f"{dado.id} - {dado.nome} - {dado.telefone} - {dado.email} - {dado.endereco}", ln=True)
    elif modelo == "agendamentos":
        dados = Agendamento.query.filter_by(user_id=current_user.id).all()
        pdf.cell(200, 10, txt="Lista de Agendamentos", ln=True, align="C")
        for dado in dados:
          pdf.cell(200, 10, txt=f"{dado.id} - Cliente: {dado.id_cliente} - Serviço: {dado.id_servico} - Data: {dado.id_data} - Hora: {dado.hora} - Status: {dado.status}", ln=True)
    else:
        flash("Modelo inválido!", "danger")
        return redirect(url_for("home_page"))

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={modelo}.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response


if __name__ == "__main__":
  with app.app_context():
    db.create_all()  
  app.run(debug=True)