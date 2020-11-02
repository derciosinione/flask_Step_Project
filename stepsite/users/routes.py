import os 
import secrets
from flask import render_template, redirect, url_for, flash, request, Blueprint
from stepsite import db, bcrypt, app
from stepsite.users.forms import FormCriarConta, FormLogin, FormPerfil
from stepsite.models import Usuarios
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

users = Blueprint('users', __name__)

# # # # Rota de login # # # #
@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects.admin'))
        
    form = FormLogin()
    if form.validate_on_submit():        
        # Selecionar o Usuarios da base de dados com as credenciais passadas no formulario
        user = Usuarios.query.filter_by(email=form.email.data).first()
        # # # Verificar se a lista de Usuarios esta vasia
        if user is None:
            flash('Por favor verifica o nome de usuário','danger')
        else:
            # # # Verificar se a senha é compactivel
            if bcrypt.check_password_hash(user.senha,form.password.data):
                # Criar a sessão do usuário logado
                login_user(user,form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('projects.admin'))
            else:
                flash('Senha incorrecta','danger')        
    return render_template("login.html",title="STEP | Login",form=form)

# # # # Rota de criação de conta # # # #
@users.route("/criarconta",methods=['GET','POST'])
def criarconta():
    
    if current_user.is_authenticated:
      return redirect(url_for('users.perfil'))
    
    form = FormCriarConta()        
    if form.validate_on_submit():
        senha = bcrypt.generate_password_hash(form.password.data).decode('utf-8') ## Criptografando a senha

        # # # # Passar as dados do formulario no model de Usuarios
        user = Usuarios(nome=form.username.data,email=form.email.data,senha=senha)
        db.session.add(user)
        # # # Enviar os dados na base de dados
        db.session.commit() 
        
        flash('Conta criada com sucesso','success')
        return redirect(url_for('users.login'))
    return render_template("criarconta.html",title="STEP | Criar Conta",form=form)

# # # # Rota de logout # # # #
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

def save_picture(form_picture):
    randon_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randon_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_img',picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@users.route("/perfil",methods=['GET','POST'])
@login_required
def perfil():
    form = FormPerfil() 
    # form.imagem.data = url_for('static',filename='userImg/'+current_user.imagem)
    
    if request.method == 'GET':
        form.username.data = current_user.nome
        form.email.data = current_user.email
    else:
        if form.validate_on_submit():
            old = current_user.imagem
            # # # Verificar se a senha é compactivel
            if bcrypt.check_password_hash(current_user.senha,form.password.data):
                if form.imagem.data:
                    picture_file = save_picture(form.imagem.data)
                    current_user.imagem = picture_file
                    
                current_user.nome = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                flash('Perfil actualizado com sucesso.','success')
                return redirect(url_for('users.perfil'))                        
            else:
                flash('Senha incorrecta, Não podes actualizar o perfil.','danger')                        
    image_file = url_for('static',filename='profile_img'+current_user.imagem)    
    return render_template("perfil.html",title="STEP | Perfil",form=form)
