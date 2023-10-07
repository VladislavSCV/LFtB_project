import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sites.utils import config
from loguru import logger


def check_db():
    """Проверка существования базы данных"""

    security_db = config.read()
    check_security_db = security_db

    if not check_security_db.get("dbname"):
        check_security_db["dbname"] = "lftb"
    try:
        connection = psycopg2.connect(**check_security_db)
        logger.info(
            f"Удачное подключение к базе данных {connection.get_dsn_parameters()['dbname']}"
        )
        connection.close()
        config.update("dbname", "lftb")
    except psycopg2.OperationalError:
        logger.debug("База данных создается.")
        create_db()
        create_table()
        check_db()


def create_db():
    """Создание бд"""

    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE lftb")
        cursor.close()
        connection.close()
        logger.debug("Создана база данных lftb")
    except (Exception, Error):
        logger.exception("Ошибка при работе с PostgreSQL")


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
        cursor.close()
        connection.close()
        logger.debug("Таблица users создана.")
    except (Exception, Error) as error:
        logger.exception("Ошибка при работе с PostgreSQL")


def get_one(user_name, parametr):
    """Получение данных из бд, одной записи"""

    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    try:
        # Авто коммит
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT {parametr} FROM users WHERE user_name = '{user_name}'"""
        )
        result = cursor.fetchone()
        # Закрытие курсора
        cursor.close()
        connection.close()
        return result
    except (Exception, Error) as error:
        logger.exception("Ошибка при работе с PostgreSQL")
        return False


def check_repeat_email(user_email):
    """Проверка повтора почты"""

    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    try:
        # Авто коммит
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(
            """SELECT COUNT(user_email) FROM users WHERE user_email = %s;""",
            (user_email,),
        )
        result = cursor.fetchone()
        # Закрытие курсора
        cursor.close()
        connection.close()
        return result
    except (Exception, Error) as error:
        logger.exception("Ошибка при работе с PostgreSQL")
        return False


def update_one_parametr(user_name, key, value):
    """Обновление данных по одному параметру"""

    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    connection.set_client_encoding("UTF8")
    try:
        # Авто коммит
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(
            f"""UPDATE users SET {key} = '{value}' WHERE user_name = '{user_name}'"""
        )
        # Закрытие курсора
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        logger.exception("Ошибка при работе с PostgreSQL")
        return False


def update_all_parametr(user_name, data):
    """Обновление данных всех параметров"""

    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    connection.set_client_encoding("UTF8")
    try:
        # Авто коммит
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        for key, value in data:
            cursor.execute(
                f"""UPDATE users SET {key} = '{value}' WHERE user_name = {user_name}"""
            )
        # Закрытие курсора
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        logger.exception("Ошибка при работе с PostgreSQL")
        return False


def add(data):
    # Подключение к существующей базе данных
    security_db = config.read()
    connection = psycopg2.connect(**security_db)
    connection.set_client_encoding("UTF8")
    try:
        # Авто коммит
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO users (user_name, user_email, user_passw, xp, pro)
                    VALUES(%s, %s, %s, %s, %s)""",
            data,
        )
        # Закрытие курсора
        cursor.close()

        connection.close()
    except (Exception, Error) as error:
        logger.exception("Ошибка при работе с PostgreSQL")
        return False
