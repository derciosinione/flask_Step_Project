from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint
from stepsite import db, or_
from stepsite.projectos.forms import FormProjectos
from stepsite.models import Categorias, Projectos, Entidades, Notificacoes
from datetime import date, datetime
from flask_login import current_user, login_required

projects = Blueprint('projects', __name__)

# # # # Rota de admin # # # #
@projects.route("/admin")
@login_required
def admin():    
    idUser = current_user.id
    pr_parados = Projectos.query.filter_by(idUsuario=idUser,estado="parado").count()
    pr_producao = Projectos.query.filter_by(idUsuario=idUser,estado="em produção").count()
    pr_concluido = Projectos.query.filter_by(idUsuario=idUser,estado="concluído").count()
    pr_total = Projectos.query.filter_by(idUsuario=idUser).count()
    gr_Projectos = {'total': pr_total,'parados': pr_parados, 'producao': pr_producao, 'concluidos': pr_concluido}

    alert = Notificacoes.query.filter_by(idUser=current_user.id).all() 
    return render_template("admin.html",title="STEP | Admin",gr_Projectos=gr_Projectos,alert=alert)

# # # # Rota de Projectos # # # #
@projects.route("/projectos",methods=['GET','POST'])
@login_required
def projectos():
            
    search = request.args.get('search','')
    page = request.args.get('page',1, type=int)
    per_page = 10
    result = None
    if search:
        result = Projectos.query.filter_by(idUsuario=current_user.id).filter(or_(Projectos.descricao.contains(search),Projectos.estado.contains(search))).order_by(Projectos.id.desc()).paginate(page=page,per_page=per_page)
    else:
        result = Projectos.query.order_by(Projectos.id.desc()).filter_by(idUsuario=current_user.id).paginate(page=page,per_page=per_page)
                
    return render_template("projectos.html",title="STEP | Projectos",result=result,search=search)


# # # # Rota de Projectos / ADD # # # #
@projects.route("/projectos/add",methods=['GET','POST'])
@login_required
def addprojectos():
    page = request.args.get('page',1, type=int)
    # Id da entidade
    en = request.args.get('en',0, type=int)
    form = FormProjectos()
    # Pesquisar a entidade com Id enviado
    if en is not 0:
        form.custos.data = 0
        form.progresso.data = 0
        entidade = Entidades.query.get(en)
        form.idEntidade.data = entidade.id
        form.entidade.data = entidade.nome

    per_page = 4
    result = Categorias.query.order_by(Categorias.id.desc()).filter_by(idUser=current_user.id).paginate(page=page,per_page=per_page)
            
    if request.method == 'POST':
        form.custos.data = request.form['custos']
        form.progresso.data = request.form['progresso']
        form.dataEntrega.data = request.form['dataEntrega']
        form.estado.data = request.form['estado']
        
    if form.validate_on_submit():  
        try:
            dataEntrega = datetime.strptime(form.dataEntrega.data,"%Y-%m-%d")          
            # # # # Passar as dados do formulario no model de Projectos
            projecto = Projectos(idcategoria=form.idCategoria.data,descricao=form.descricao.data,custos=form.custos.data,dataEntrega=dataEntrega,estado=form.estado.data,progresso=form.progresso.data,idEntidade=form.idEntidade.data,idUsuario=current_user.id)
            db.session.add(projecto)
            # # # Enviar os dados na base de dados
            vf = db.session.commit()
            if vf is None: 
                flash('Projecto adicionado com sucesso','success')
                # Criar Notificacoes
                titulo_not = f"Novo Projecto! Foi adicionado recentemente o projecto {form.descricao.data}."
                create_notificacao = Notificacoes(titulo=titulo_not,categoria='info',projecto=form.descricao.data,idUser=current_user.id)
                db.session.add(create_notificacao)
                db.session.commit()
                return redirect(url_for('projects.projectos'))
            else:
                flash('Houve um erro ao adicionar projecto, Tente mais tarde.','danger')
        except:
            flash('Houve um erro ao adicionar projecto, Tente mais tarde.','danger')
                            
    return render_template("addprojectos.html",title="STEP | Adicionar Projectos",result=result,form=form,en=en,curpage=page)

# # # # Rota de Projectos / Update # # # #
@projects.route("/projectos/update",methods=['GET','POST'])
@login_required
def updateprojecto():        
    page = request.args.get('page',1, type=int)
    en = request.args.get('en',0, type=int)
    projecto = Projectos.query.get(en)

    form = FormProjectos()
    per_page = 4
    result = Categorias.query.order_by(Categorias.id.desc()).filter_by(idUser=current_user.id).paginate(page=page,per_page=per_page)

    if request.method == 'POST':
        form.custos.data = request.form['custos']
        form.progresso.data = request.form['progresso']
        form.dataEntrega.data = request.form['dataEntrega']
        form.estado.data = request.form['estado']
    else:
        if projecto is not None:
            form.idProjecto.data = projecto.id
            form.idCategoria.data = projecto.idcategoria
            form.categoria.data = projecto.categoria.nome
            form.descricao.data = projecto.descricao
            form.idEntidade.data = projecto.idEntidade
            form.entidade.data = projecto.entidade.nome
            form.custos.data = projecto.custos
            form.progresso.data = projecto.progresso
            form.dataEntrega.data = projecto.dataEntrega
            form.estado.data = projecto.estado
        else:
            return redirect(url_for('projects.projectos'))

        
    if form.validate_on_submit():  
        
        projecto = Projectos.query.get(int(form.idProjecto.data))

        dataEntrega = datetime.strptime(form.dataEntrega.data,"%Y-%m-%d")          

        projecto.idcategoria = form.idCategoria.data
        projecto.descricao = form.descricao.data
        projecto.custos = form.custos.data
        projecto.estado = form.estado.data
        projecto.progresso = form.progresso.data
        projecto.dataEntrega = dataEntrega
        
        titulo_not = None 
        if(projecto.estado=="concluído"):
            projecto.dataConclusao = datetime.utcnow()
            titulo_not = f"Well done! Projecto {form.descricao.data} concluído com sucesso."
            create_notificacao = Notificacoes(titulo=titulo_not,categoria='success',projecto=form.descricao.data,idUser=current_user.id)
            db.session.add(create_notificacao)
        else:
            projecto.dataConclusao = None
            
        # # Enviar os dados na base de dados
        db.session.commit()
        flash('Projecto actualizado com sucesso','success')
        return redirect(url_for('projects.projectos'))
        
    return render_template("updateprojectos.html",title="STEP | Actualizar Projectos",result=result,form=form,curpage=page)


# # # # Rota de Remover Projecto # # # #
@projects.route("/projectos/<int:id>/delete")
@login_required
def delete(id):
    result = Projectos.query.get_or_404(id)
    db.session.delete(result)
    db.session.commit()
    flash(f'Projecto {result.descricao} eliminado com sucesso','success')
    return redirect(url_for('projects.projectos'))