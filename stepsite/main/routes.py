from flask import render_template, redirect, url_for, Blueprint

main = Blueprint('main', __name__)

# # # # Rota de Inicial da pagina (Home) # # # #
@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html",title="STEP | Home")


