from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)
FLASK_APP = app

def get_db_connection(db_name, user_name, passwd):
    connection = psycopg2.connect(host='localhost',
                                  database=db_name,
                                  user=user_name,
                                  password=passwd)
    return connection


@app.route('/')
def index():
    db_name = 'flaskdb'
    user_name = "cham_user"
    passwd = '12345'
    connection = get_db_connection(db_name, user_name, passwd)
    cursor = connection.cursor()
    cursor.execute('select * from Foods;')
    foods = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', foods=foods)
