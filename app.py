from flask import Flask, render_template, request, url_for, redirect, make_response
import psycopg2


app = Flask(__name__)
FLASK_APP = app


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

@app.route('/login/')
def login():
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')
    res = make_response(f'<h1>Форма авторизации</h1><p>logged: {log}')
    res.set_cookie("logged", "yes", 600)
    return res
@app.route('/logout/')
def logout():
    res = make_response("<p>Вы вышли</p>")
    res.set_cookie("logged", "", 0)
    return res