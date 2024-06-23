from flask import Flask, render_template, request, url_for, redirect
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
