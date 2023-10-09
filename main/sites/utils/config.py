import json
from pathlib import Path


config_path = Path("config.json")


def create():
    """Создание конфигурации"""

    print("Настройки сервера.")
    user = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    host = input("Введите host: ")
    port = input("Введите port: ")

    with open(config_path, "w") as f:
        json.dump(
            {
                "user": user,
                "password": password,
                "host": host,
                "port": port,
            },
            f,
        )


def read():
    """Чтение конфигурации"""

    with open(config_path, "r") as f:
        data = json.load(f)

    return data


def update(key, value):
    """Обновление конфигурации"""
    
    data =  read()
    
    data[key] = value
    
    with open(config_path, "w") as f:
        json.dump(data, f)

if not config_path.exists():
    create()
