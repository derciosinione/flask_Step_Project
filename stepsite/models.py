from datetime import datetime
from stepsite import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

# # # # Model de Usuario # # # #
class Usuarios(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), unique=False, nullable=False)
    imagem = db.Column(db.String(30), nullable=False, default='defaultUser.jpg')
    categorias = db.relationship('Categorias', backref='usuarios', lazy=True)
    entidades = db.relationship('Entidades', backref='usuarios', lazy=True)
    projectos = db.relationship('Projectos', backref='usuarios', lazy=True)
    
    def __repr__(self):
        return f"Usuarios('{self.nome}','{self.email}','{self.imagem}')"

# # # # Model de Categorias # # # #
class Categorias(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)    
    projectos = db.relationship('Projectos', backref='categorias', lazy=True)
    
    def __repr__(self):
        return f"Categorias('{self.nome}','{self.idUser}')"

# # # # Model de Notificacoes # # # #
class Notificacoes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String(100), unique=True, nullable=False)
    categoria = db.Column(db.String(20))
    projecto = db.Column(db.String(50))
    idUser = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)    
    
    def __repr__(self):
        return f"Notificacoes('{self.titulo}','{self.idUser}')"

    
# # # # Model de Entidades # # # #
class Entidades(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(20), nullable=False)
    imagem = db.Column(db.String(50), nullable=False, default='defaultEntidade.jpg')
    idUser = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)    
    projectos = db.relationship('Projectos', backref='entidades', lazy=True)
    
    def __repr__(self):
        return f"Entidades('{self.nome}','{self.email}','{self.contacto}','{self.imagem}')"

# # # # Model de Projectos # # # #
class Projectos(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    idcategoria = db.Column(db.Integer, db.ForeignKey('categorias.id'),nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    custos = db.Column(db.Integer, default=0)
    dataEntrega = db.Column(db.Date)
    dataRegisto = db.Column(db.DateTime,default=datetime.utcnow)
    estado = db.Column(db.String(20),nullable=False,default='prado')
    progresso = db.Column(db.Integer,default='0')    
    dataConclusao = db.Column(db.DateTime,default=None)
    idEntidade = db.Column(db.Integer, db.ForeignKey('entidades.id'),nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'),nullable=False)
    categoria = db.relationship('Categorias', backref='categoria', lazy=True)
    entidade = db.relationship('Entidades', backref='entidade', lazy=True)
    
    def __repr__(self):
        return f"Projecto('{self.descricao}','{self.estado}','{self.progresso}','{self.dataEntrega}')"

