from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, length, ValidationError
from stepsite.models import Entidades

class FormEntidades(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(),length(min=3,max=50,message="Só é permetido nome no intervalo de 3 a 50 dígitos.")])
    email = StringField(label='Email',validators=[DataRequired(),Email(message="Email inválido."),length(min=4,max=100,message="Só é email no intervalo de 4 a 100 dígitos.")])
    contacto = StringField('Contacto', validators=[DataRequired(),length(min=9,max=20,message="Só é permetido nome no intervalo de 9 a 20 dígitos.")])
    submit = SubmitField('Adicionar')    
    
    # # # Verificar se o nome insirido está disponivel
    def validate_entidade(self,nome):
        entidade = Entidades.query.filter_by(nome=nome.data).first() 
        if entidade:
            raise ValidationError('esta entidade já está inserida na base de dados')    
