import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required, current_user, logout_user


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'f3cfe9ed8fae309f02079dbf'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    is_authenticated = True
    is_active = True
    is_anonymous = False
    def get_id(self):
        return str(self.id)
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha
        }

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

# Criar a 1º pagina do site
# route -> hastagtreinamentos.com/
# função -> o que vc quer exibir naquela pagina

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        req = request.form

        email = req['email']
        senha = req['senha']

        user_with_email = User.query.filter_by(email = email).first()
        if not user_with_email:
            error = "Este email ou senha não existem. Tente novamente!."
            return render_template('login.html', error=error)

        user_alpha = user_with_email
        user_alpha.is_authenticated = True
        login_user(user_alpha, remember=False)
        return redirect('/perfil')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        req = request.form

        nome = req['nome']
        email = req['email']
        senha = req['senha']

        user_with_email = User.query.filter_by(email=email).first()
        user_with_password = User.query.filter_by(senha=senha).first()

        if user_with_email or user_with_password:
            error = "Este email ou senha já está em uso. Escolha um diferente."
            return render_template('cadastro.html', error=error)

        db_user = User(nome = nome, email = email, senha = senha)
        db.session.add(db_user)
        db.session.commit()

        return redirect('/')
    return render_template('cadastro.html')

@app.route('/perfil', methods=['GET'])
@login_required
def perfil():

    

    return render_template('perfil.html', nome_usuario=current_user.nome)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar():
    if request.method == 'POST':
        req = request.form
        to_edit_user = User.query.filter_by(id = current_user.id).first()
        to_edit_user.nome = req['nome']
        current_user.nome = req['nome']
        to_edit_user.email = req['email']
        current_user.email = req['email']
        to_edit_user.senha = req['senha']
        db.session.commit()
        current_user.senha = req['senha']
        return redirect('/perfil')

    return render_template('editar.html', nome_usuario=current_user.nome)


@app.route('/perfil/sair', methods=['GET'])
@login_required
def sair():
    logout_user()
    return redirect('/')

@app.route('/perfil/delete', methods=['GET','POST'])
@login_required
def delete():
    if request.method == 'POST':
        user_to_delete = User.query.get(current_user.id)
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    return render_template('delete.html')


# Colocar o site no ar
if __name__ == '__main__':
    app.run(debug=True)

    # Servidor Heroku
