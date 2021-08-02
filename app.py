import sqlite3
from hashids import Hashids
from flask_session import Session
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, redirect, url_for, session


def get_db_connection():
    #abre a conexão para o banco de dados
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretString' 
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)  # pacote para lidar com sessão de usuário

# range do hashid abcd...ABCD...0123...9 62 caracteres em 6 posicoes = 44 bilhoes de possibilides 
hashids = Hashids(min_length=6, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    
    if not session.get("name"):
        return redirect("/login")

    if request.method == 'POST':
        url = request.form['url']

        if not url: #se vazio 
            flash('Digite uma URL!')
            return redirect(url_for('index'))
        if not validators.url(url): # checa se a url é válida 
            flash('A URL é invalida! Digite uma URL válida')
            return redirect(url_for('index'))

        username = session["name"]
        url_data = conn.execute('INSERT INTO urls (original_url, username, short_url) VALUES (?,?,?)'
                                                                ,(url,session["name"],url))
        conn.commit()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        conn.execute('UPDATE urls SET short_url = ? WHERE id = ?',
                                                  (short_url, url_id))
        conn.commit()
        conn.close()

        return render_template('index.html', short_url=short_url, username=username)

    return render_template('index.html', username=session["name"])

@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]

        url_data = conn.execute('SELECT original_url FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']

        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method=='GET': 
        return render_template('login.html')
    else: # checar usuario e senha
          
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT username, senha FROM users'
                                ' WHERE email = (?)', (email,)
                                ).fetchone()
        conn.close()

        # checar se o usuário existe
        # se o usuário existir, verificar se a senha está correta. 
        # compara a senha enviada com a senha salva no banco de dados (senha com hash_256)      
        if not user:
            flash('Usuário não cadastrado!')
            return redirect(url_for('login'))
        elif not check_password_hash(user['senha'], password):
            flash(f'Verifique suas informações de acesso.')
            return redirect(url_for('login'))  
              
        session["name"] = user['username']
        return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/stats')
def stats():

    if not session.get("name"):
        return redirect("/login")
    conn = get_db_connection()

    db_urls = conn.execute('SELECT id, datetime(created,"localtime") as created, original_url, username, short_url FROM urls'
                           ' WHERE username = (?)', (session["name"],)
                            ).fetchall()
    conn.close()

    urls = db_urls

    return render_template('stats.html', urls=urls, username=session["name"])