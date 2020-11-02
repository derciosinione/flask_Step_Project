from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, length, ValidationError
# from stepsite.models import Projectos

class FormProjectos(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired(),length(min=3,max=100,message="Só é permetido nome no intervalo de 3 a 100 dígitos.")])
    idCategoria = StringField('Id da Categoria',validators=[DataRequired()])
    idProjecto = IntegerField('Identificador')
    categoria = StringField('Categoria', validators=[DataRequired()])
    custos = DecimalField('Custos', validators=[DataRequired(message="Este campo é obrigatório.")])
    estado = StringField('estado', validators=[DataRequired()])
    progresso = IntegerField('Progresso', validators=[DataRequired(message="Este campo é obrigatório."),length(max=3,message="O progresso de um projecto vai de 0 a 100%.")])
    idEntidade = StringField('Id da Entidade',validators=[DataRequired()])
    entidade = StringField('Entidade', validators=[DataRequired()])
    dataEntrega = DateField('Data Entrega',validators=[DataRequired(message="Este campo é obrigatório.")])
    submit = SubmitField('Adicionar')
