#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from sites.utils import config  as config, db_handlers as db

def main():
    """Run administrative tasks."""
    # Проверка конфигурации
    if not config.config_path.exists():
        config.create()
    
    # Проверка бд
    db.check_db()
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
