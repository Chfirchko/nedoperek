import os
import psycopg2

# соединение с БД
db_name = 'flaskdb'
user_name = "cham_user"
passwd = '12345'

connection = psycopg2.connect(host='localhost',
                              database=db_name,
                              user=user_name,
                              password=passwd)

# курсор для взаимодействия с БД
cursor = connection.cursor()

# создание таблицы товаров
cursor.execute('DROP TABLE IF EXISTS Foods;')
cursor.execute('create table Foods (id serial primary key,'
               'title varchar (150) not null,'
               'provider varchar (150) not null,'
               'description text,'
               'date_added date default current_timestamp);')


# создание таблицы корзины пользователя
cursor.execute('create table Basket (id serial primary key,'
               'title varchar (150) not null,'
               'provider varchar (150) not null,'
               'description text,'
               'date_added date default current_timestamp);')
# вставка строки

cursor.execute('insert into Foods (title, provider, description)'
               'values (%s, %s, %s)',
               ('Хлеб',
                'Госнаркоконтроль',
                'Это хлеб. Самый обычный хлеб.')
               )


connection.commit()
cursor.close()
connection.close()