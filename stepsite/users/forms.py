from flask_wtf import FlaskForm
from flask_wtf.file import FileField, file_allowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from stepsite.models import Usuarios
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),length(min=3,max=30,message="Só é permetido nome no intervalo de 3 a 20 dígitos.")])
    email = StringField(label='Email',validators=[DataRequired(),Email(message="Email inválido."),length(min=4,max=100,message="Só é email no intervalo de 4 a 100 dígitos.")])
    # ee= StringField()
    password = PasswordField('Senha',validators=[DataRequired(),length(min=4,max=20,message="Só é permetido senhas no intervalo de 4 a 20 dígitos.")])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password',message="As senhas inseridas não são compactíveis.")])
    submit = SubmitField('Registar')
    
    # # # Verificar se o nome insirido está disponivel
    def validate_username(self,username):
        user = Usuarios.query.filter_by(nome=username.data).first() 
        if user:
            raise ValidationError('este nome não está disponivel')    
        
    # # # Verificar se o email insirido está disponivel
    def validate_email(self,email):
        user = Usuarios.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('este email não está disponivel')    
        
class FormLogin(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(message="Email inválido.")])
    password = PasswordField('Senha')
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class FormPerfil(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),length(min=3,max=30,message="Só é permetido nome no intervalo de 3 a 20 dígitos.")])
    imagem = FileField('Actualizar imagem de perfil', validators=[file_allowed(['jpg','png'],message="Só é permitido ficheiros do tipo .png e .jpg.")])
    email = StringField(label='Email',validators=[DataRequired(),Email(message="Email inválido."),length(min=4,max=100,message="Só é email no intervalo de 4 a 100 dígitos.")])
    password = PasswordField('Senha',validators=[DataRequired()])
    submit = SubmitField('Actualizar')
    
    # # # Verificar se o nome insirido está disponivel
    def validate_username(self,username):
        if current_user.nome != username.data:
            user = Usuarios.query.filter_by(nome=username.data).first() 
            if user:
                raise ValidationError('este nome não está disponivel')    
        
    # # # Verificar se o email insirido está disponivel
    def validate_email(self,email):
        if current_user.email != email.data:
            user = Usuarios.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError('este email não está disponivel')    
