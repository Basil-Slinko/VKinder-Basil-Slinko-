import psycopg2
from pprint import pprint


def database_connection():
    connect = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="1604",
        host="127.0.0.1",
        port="5433"
    )
    return connect


def creating_tables_postgres_db():
    connect_to_db = database_connection()
    print("Database opened successfully")
    cur = connect_to_db.cursor()
    cur.execute('''CREATE TABLE user_vk 
                 (id SERIAL PRIMARY KEY,
                 vk_id INTEGER NOT NULL);

                 CREATE TABLE pair_for_vk_user  
                 (id SERIAL PRIMARY KEY,
                 vk_id INTEGER NOT NULL);

                 CREATE TABLE user_vk_and_pair 
                 (id SERIAL PRIMARY KEY,
                 user_vk_id INTEGER NOT NULL REFERENCES user_vk(id),
                 pair_for_user_id INTEGER NOT NULL REFERENCES pair_for_vk_user(id));
                 ''')
    print("Table created successfully")
    connect_to_db.commit()
    connect_to_db.close()


def add_to_database_user_vk(id_user_vk):
    connect_to_db = database_connection()
    print("add_to_database_user_vk -- Database opened successfully")
    cur = connect_to_db.cursor()

    cur.execute(f'INSERT INTO user_vk (vk_id) VALUES ({id_user_vk})')

    connect_to_db.commit()
    print("add_to_database_user_vk -- Record inserted successfully")
    connect_to_db.close()


def add_to_database_pair_for_vk_user(pair_account_id):
    connect_to_db = database_connection()
    print("add_to_database_pair_for_vk_user -- Database opened successfully")
    cur = connect_to_db.cursor()

    cur.execute(f'INSERT INTO pair_for_vk_user (vk_id) VALUES ({pair_account_id})')

    connect_to_db.commit()
    print("add_to_database_pair_for_vk_user -- Record inserted successfully")
    connect_to_db.close()


def add_to_database_user_vk_and_pair(id_user_vk, pair_account_id):
    connect_to_db = database_connection()
    print("add_to_database_user_vk_and_pair -- Database opened successfully")
    cur = connect_to_db.cursor()

    cur.execute(f'INSERT INTO user_vk_and_pair (user_vk_id, pair_for_user_id) '
                f'VALUES ({get_id_column_user_vk_id(id_user_vk)}, {get_id_column_pair_for_vk_user(pair_account_id)})')

    connect_to_db.close()


def get_id_column_user_vk_id(id_user_vk):
    connect_to_db = database_connection()
    print("get_id_column_user_vk_id -- Database opened successfully")
    cur = connect_to_db.cursor()
    cur.execute(f"SELECT id from user_vk WHERE vk_id = {id_user_vk};")
    rows = cur.fetchall()
    connect_to_db.close()
    return rows[0][0]


def get_id_column_pair_for_vk_user(pair_account_id):
    connect_to_db = database_connection()
    print("get_id_column_pair_for_vk_user -- Database opened successfully")
    cur = connect_to_db.cursor()
    cur.execute(f"SELECT id from pair_for_vk_user WHERE vk_id = {pair_account_id};")
    rows = cur.fetchall()
    connect_to_db.close()
    return rows[0][0]


if __name__ == "__main__":
    creating_tables_postgres_db()
   
