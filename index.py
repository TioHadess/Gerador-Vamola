from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Criar a 1º pagina do site
# route -> hastagtreinamentos.com/
# função -> o que vc quer exibir naquela pagina

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        req = request.form

        nome = req['nome']
        email = req.get['email']
        senha = request.form['senha']

        print(nome,email,senha)

        return redirect(request.url)
    return render_template('cadastro.html')

@app.route('/usuarios/<nome_usuario>')
def usuarios(nome_usuario):
    return render_template('usuarios.html', nome_usuario = nome_usuario)

# Colocar o site no ar
if __name__ == '__main__':
    app.run(debug=True)

    # Servidor Heroku
