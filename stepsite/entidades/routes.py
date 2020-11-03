from flask import render_template, redirect, url_for, flash, request, Blueprint
from stepsite import app, db, or_
from stepsite.entidades.forms import FormEntidades
from stepsite.models import Entidades
from flask_login import current_user, login_required

entidads = Blueprint('entidads', __name__)

# Expor esta função para o template renderizado
@entidads.context_processor
def start_context():
    def getLenght(elemento):
        return len(elemento)
    return dict(getLenght=getLenght)


# # # # Rota de entidades # # # #
@entidads.route("/entidades", methods=['GET','POST'])
@login_required
def entidades():
    form = FormEntidades()            
    
    if form.validate_on_submit():        
        # # # # Passar as dados do formulario no model de entidades
        entidade = Entidades(nome=form.nome.data,email=form.email.data,contacto=form.contacto.data,idUser=current_user.id)
        db.session.add(entidade)
        # # # Enviar os dados na base de dados
        vf = db.session.commit()
        if vf is None: 
            flash('Entidade adicionada com sucesso','colorgreen')
            return redirect(url_for('entidads.entidades'))
        else:
            flash('Houve um erro ao adicionar a entidade, Tente mais tarde.','colorred')
            
    search = request.args.get('search','')
    page = request.args.get('page',1, type=int)
    per_page = 9
    if search:
        result = Entidades.query.filter_by(idUser=current_user.id).filter(or_(Entidades.nome.contains(search),Entidades.email.contains(search))).order_by(Entidades.id.desc()).paginate(page=page,per_page=per_page)
    else:
        result = Entidades.query.filter_by(idUser=current_user.id).order_by(Entidades.id.desc()).paginate(page=page,per_page=per_page)
                
    return render_template("entidades.html",title="STEP | Entidades",result=result,form=form,search=search)


# # # # Rota de Actualizar Entidade # # # #
@entidads.route("/entidades/<int:id>/update",methods=['GET','POST'])
@login_required
def updeteEntidade(id):
    result = Entidades.query.get_or_404(id)
    form = FormEntidades()
    if form.validate_on_submit():   
        result.nome = form.nome.data
        result.email = form.email.data
        result.contacto = form.contacto.data
        db.session.commit()
        flash('Entidade actualizada com sucesso','success')
        return redirect(url_for('entidads.entidades'))
    else:
        flash('Houve um erro ao actualizar a entidade, Tente mais tarde.','danger')
        return redirect(url_for('entidads.entidades'))

        
# # # # Rota de Remover Entidade # # # #
@entidads.route("/entidades/<int:id>/delete")
@login_required
def deleteEntidade(id):
    result = Entidades.query.get_or_404(id)
    db.session.delete(result)
    db.session.commit()
    flash(f'Entidade {result.nome} eliminada com sucesso','success')
    return redirect(url_for('entidads.entidades'))
