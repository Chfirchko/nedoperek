from flask import Flask, render_template, request, url_for, redirect, flash
# from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2


app = Flask(__name__)
FLASK_APP = app
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_db_connection():
    db_name = 'flaskdb'
    user_name = "cham_user"
    passwd = '12345'
    connection = psycopg2.connect(host='localhost',
                                  database=db_name,
                                  user=user_name,
                                  password=passwd)
    return connection


@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select * from Foods;')
    foods = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', foods=foods)


# GET - переход на страницу  POST - кнопка добавления позиции
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        provider = request.form['provider']
        description = request.form['description']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('insert into Foods (title, provider, description)'
                       'values (%s, %s, %s)',
                       (title, provider, description))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/basket/')
def basket():
    return render_template('basket.html')

@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        user_email = request.form['email']
        user_psw = request.form['psw']
        connection = get_db_connection()
        cursor = connection.cursor()

        if user_psw == cursor.execute('SELECT psw FROM users WHERE email = \'' + str(user_email) + '\' LIMIT 1;'):
         pass
        connection.commit()
        cursor.close()
        connection.close()
        return render_template('basket.html')
    return render_template('login.html')

@app.route('/logout/')
def logout():
    return render_template('logout.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        psw = request.form['psw']
        name = request.form['name']
        email = request.form['email']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('insert into users (name, email, psw)'
                       'values (%s, %s, %s)',
                       (name, email, psw))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('register.html')











# @app.route('/login/', methods=('POST', 'GET'))
# def login():
#     log = ''
#     if request.method == 'POST':
#         title = request.form['title']
#         type = request.form['type']
#         passwd = request.form['passwd']
#
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('insert into users (title, type, passwd)'
#                        'values (%s, %s, %s)',
#                        (title, type, passwd))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         if request.cookies.get('logged'):
#             log = request.cookies.get('logged')
#         res = make_response(f'<h1>Форма авторизации</h1><p>logged: {log}' )
#         res.set_cookie("logged", "yes", 600)
#         return res
#     return render_template('login.html')
# @app.route('/logout/')
# def logout():
#     res = make_response("<p>Вы вышли</p>")
#     res.set_cookie("logged", "", 0)
#     return res