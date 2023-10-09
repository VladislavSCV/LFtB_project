"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from sites import views as siVi


""" Маршрутизация """
urlpatterns = [
    path('admin/', admin.site.urls),
    # Добавление в бд выбранный курс и вывод содержимого курса
    re_path(r".*Изучение_(?P<course>[\w-]+)/$", siVi.send_user_courses, name='send_user_courses'),
    re_path(r".*Закончить_(?P<course>[\w-]+)/$", siVi.end_user_course, name='end_user_course'),
    # Страницы курса
    re_path(r".*Курс_pro_(?P<course>[\w-]+)/$", siVi.catalog_courses_pro, name='catalog_courses_pro'),
    re_path(r".*Курс_(?P<course>[\w-]+)/$", siVi.catalog_courses, name='catalog_courses'),
    
    # Выход из учет. записи
    re_path(r".*Выход/$", siVi.quit),
    # Темы
    re_path(r".*Настройки/$", siVi.theme),
    # Страница с PRO
    re_path(r".*PRO/$", siVi.pro),
    # Оплата и ввод данных с карты
    re_path(r".*Оплата/$", siVi.payments),
    # Результаты поиска
    re_path(r".*Search/$", siVi.res_search),
    # Квесты
    re_path(r".*Квесты/$", siVi.quest),
    # Профиль
    re_path(r".*Профиль/$", siVi.User_page),
    # Подтверждение почты
    re_path(r".*Подтверждение_почты/$", siVi.conf_to_reg),  # type: ignore
    # Авторизация
    re_path(r".*Авторизация/$", siVi.Auth),
    # Регистрация
    re_path(r".*Регистрация/$", siVi.reg),
    # Проверка пароля
    re_path(r".*Проверка/$", siVi.confirm),
    # Каталог курсов
    re_path(r".*Каталог_курсов/", siVi.catalog),
    # Главная траница
    re_path(r".*Главная_страница/$", siVi.MainPage),
    re_path(r".*Главная_страница./$", siVi.main_b_a),
    path("", siVi.MainPage),

    # Тестирование новых фич
    re_path(r".*test/$", siVi.test)
]
