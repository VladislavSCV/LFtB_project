import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

security_db = {
    "user": "maks",
    "password": "1576",
    "host":"127.0.0.1",
    "dbname":"lftb"
}

def create_db():
    """Создание бд"""
    # Подключение к существующей базе данных
    connection = psycopg2.connect(**security_db)
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = f"create database LFtB"
        cursor.execute(sql_create_database)
        security_db["dbname"] = "LFtB"
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def test():
    # Подключение к существующей базе данных
    connection = psycopg2.connect(
        **security_db
    )
    try:
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def create_table():
    """Создание таблицы"""

    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()
    cursor.execute("CREATE SEQUENCE users_id_seq")
    conn.commit()
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
    conn.commit()
    cursor.close()
