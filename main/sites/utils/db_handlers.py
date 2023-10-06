import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sites.utils import config


def create_db():
    """Создание бд"""
    
    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = f"create database Lftb"
        cursor.execute(sql_create_database)
        config.update("dbname","lftb")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с PostgreSQL закрыто")


def create_table():
    """Создание таблицы"""
    
    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute("CREATE SEQUENCE users_id_seq")
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS public.users
    (
        id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
        user_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
        user_email character varying COLLATE pg_catalog."default" NOT NULL,
        user_passw character varying(50) COLLATE pg_catalog."default" NOT NULL,
        pro boolean DEFAULT false,
        photo_url text COLLATE pg_catalog."default",
        user_desc text COLLATE pg_catalog."default",
        user_courses text COLLATE pg_catalog."default",
        user_certific text COLLATE pg_catalog."default",
        xp integer,
        user_achiv text COLLATE pg_catalog."default",
        user_theme text COLLATE pg_catalog."default",
        PRIMARY KEY (id)
    )"""
        )
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с PostgreSQL закрыто")


def get(user_name, parametr):
    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    try:
        # Авто коммит 
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {parametr} FROM users WHERE user_name = '{user_name}'""")
        user = cursor.fetchone()
        # Закрытие курсора
        cursor.close()
        connection.close()
        return user
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    
