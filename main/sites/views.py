from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
import random

# from yoomoney import Quickpay
# from yoomoney import Client
import string
# import asyncio
import spacy
import psycopg2

from .forms import userFormREG, userSearchEngine, userFormAUTH, select_theme

# Удалить session object
# del request.session['userName']


# Изображение пользователя если нет своего фото
img_src = "https://brend-mebel.ru/image/no_image.jpg"


dct_courses = {
    ("Frontend Development", "Фронтенд разработка", "Разработка пользовательского интерфейса", "Фронтенд программирование", "Фронтэнд верстка", "HTML", "CSS"): 0,
    ("Data Science", "Анализ данных", "Машинное обучение", "Статистика", "Нейронные сети", "Большие данные", "Python"): '',
    ("Backend Development", 'backend', "Бэкэнд разработка", "Серверная разработка", "Django", "Flask", "REST API"): '',
    ("Цифровой маркетинг", "реклама", "аналитика", "SEO", "SEM", "Email-маркетинг", "Контент-маркетинг"): '',
    ("Финансовый анализ", "баланс", "доходность", "рентабельность", "Финансовое планирование", "Инвестиции", "Аудит"): '',
    ("Blockchain и криптовалюты", "технология", "достоверность", "декентрализация", "майнинг", "Smart contracts", "Ethereum"): '',
    ("UX/UI дизайн", "интерфейс", "прототипирование", "визуальный", "Графический дизайн", "Motion design", "Adobe Photoshop"): '',
    ("IOS разработчик", 'Разработка приложений для IOS', 'Swift', "Objective-C", "Xcode", "UIKit", "Core Data"): '',
    ("SQL", 'Реляционные базы данных', 'Запросы SQL', "MySQL", "PostgreSQL", "Oracle", "Microsoft SQL Server"): '',
    ("Кибербезопасность", "Cyber security", 'Защита информации', 'Киберзащита', "Пентестинг", "Шифрование", "Firewall"): ''
}

dct_res_text = {
    0: ["Frontend Development", "Фронтенд-разработчики занимаются созданием пользовательского интерфейса для веб-приложений и сайтов, используя языки программирования HTML, CSS и JavaScript.", "Frontend_разработка/"],
    1: ["Data Science", "Этот курс расскажет о базовых принципах анализа данных и машинного обучения. Студенты изучат методы сбора, обработки и интерпретации данных, а также научатся применять статистические модели для прогнозирования и принятия решений.", "Data_science/"],
    2: ["Backend Development", "Этот курс предлагает изучение серверной разработки, языков программирования и инструментов для создания мощных веб-приложений. Вы освоите Python, Ruby или Node.js, а также научитесь работать с базами данных, разрабатывать API и обеспечивать безопасность приложения.", "Backend_разработка/"],
    3: ["Цифровой маркетинг", "Курс по цифровому маркетингу научит вас использовать социальные сети, контент-маркетинг и SEO для привлечения трафика и достижения бизнес-целей. Вы освоите создание и оптимизацию цифровых маркетинговых кампаний.", "Цифровой_маркетинг/"],
    4: ["Финансовый анализ", "Этот курс представляет изучение основ финансового анализа и оценки состояния компаний. Студенты освоят различные инструменты и модели, необходимые для принятия обоснованных финансовых решений.", "Финансовый_анализ/"],
    5: ["Blockchain и криптовалюты", "Курс, который позволяет понять концепции и технологии блокчейн, а также различные типы криптовалют. Вы научитесь использовать блокчейн для создания безопасных и надежных систем передачи данных и управления с децентрализованной структурой.", "Blockchain/"],
    6: ["UX/UI дизайн", "Этот курс научит создавать удобные и привлекательные пользовательские интерфейсы. Обучение включает основы UI/UX-дизайна, а также применение современных инструментов и методов для создания и тестирования дизайна.", "UX_UI_дизайн/"],
    7: ["IOS разработчик", "Курс по разработке мобильных приложений для устройств iOS с использованием языка программирования Swift и инструментов Apple. Студенты научатся создавать, поддерживать и обновлять приложения для iPhone, iPad и других устройств, работающих на iOS.", "IOS_разработка/"],
    8: ["SQL", "Декларативный язык программирования, применяемый для создания, модификации и управления данными в реляционной базе данных, управляемой соответствующей системой управления базами данных.", "SQL_разработка/"],
    9: ["Кибербезопасность", "Направление связанное с разработкой и управлением систем информационной безопасности в организации.", "Cyber_security/"]
}

dct_res = {}

dct = {}


def MainPage(request):
    """ Вывод обычной главной страницы """
    use = userSearchEngine()
    if request.method == "POST":
        if use.is_valid():
            # userRequest = use.cleaned_data["search_engine"]
            return render(request, "search_results.html")

    return render(request, "main.html", {'forms': use})


def res_search(request):
    """ Результаты поиска """
    global dct_res, dct_courses, dct_res_text

    userNameSession = request.session.get("userName")

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    u_theme = cursor.fetchone()[0] or "theme1"
    print(u_theme)
    cursor.close()
    conn.close()

    
    lst = []
    if request.method == "POST":
        userReqqq = userSearchEngine(request.POST)
        if userReqqq.is_valid():
            user_req = userReqqq.cleaned_data['search_engine']
            nlp = spacy.load("en_core_web_sm")
            word1 = nlp(user_req)

            dct_res = {}  # добавлено объявление словаря dct_res
            for i in dct_courses.keys():
                res_num = 0
                for j in i:
                    word2 = nlp(j)
                    k = word1.similarity(word2)
                    res_num += k
                dct_courses[i] = str(res_num)

            for k, v in dct_courses.items():
                if k[0] == "Frontend Development" and float(v) > 2.5:
                    lst.append(dct_res_text[0])
                if k[0] == "Data Science" and float(v) > 2.5:
                    lst.append(dct_res_text[1])
                if k[0] == "Backend Development" and float(v) > 2.5:
                    lst.append(dct_res_text[2])
                if k[0] == "Цифровой маркетинг" and float(v) > 2.5:
                    lst.append(dct_res_text[3])
                if k[0] == "Финансовый анализ" and float(v) > 2.5:
                    lst.append(dct_res_text[4])
                if k[0] == "Blockchain и криптовалюты" and float(v) > 2.5:
                    lst.append(dct_res_text[5])
                if k[0] == "UX/UI дизайн" and float(v) > 2.5:
                    lst.append(dct_res_text[6])
                if k[0] == "IOS разработчик" and float(v) > 2.5:
                    lst.append(dct_res_text[7])
                if k[0] == "SQL" and float(v) > 2.5:
                    lst.append(dct_res_text[8])
                if k[0] == "Кибербезопасность" and float(v) > 2.5:
                    lst.append(dct_res_text[9])

            # исправлено использование переменной data.items
            return render(request, "search_results.html", {"collection": lst, "u_theme": u_theme})
    return render(request, "search_results.html")


def end_user_course(request, course):
    """ Закончить курс """
    userNameSession = request.session.get("userName")

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT xp FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    exp_num = cursor.fetchone()[0]
    print(type(exp_num))

    cursor.close()
    conn.close()
    
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    # Получаем set курсов из бд. Тип данных: str
    cursor.execute(
        """SELECT user_courses FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()
    # Перевод курсов из str в set
    courses = eval(cursor.fetchone()[0])
    print(courses)

    cursor.close()
    conn.close()

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    # Получаем set законченых курсов из бд. Тип данных: str
    cursor.execute(
        """SELECT user_certific FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()
    # Перевод курсов из str в set
    # set_end_courses = eval(cursor.fetchone()[0]) if cursor.fetchone()[0] else set()
    set_end_courses = cursor.fetchone()[0]

    if set_end_courses:
        set_end_courses = eval(set_end_courses)
    else:
        set_end_courses = set()

    print(set_end_courses)

    cursor.close()
    conn.close()

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    if course == "Backend" and "Backend разработка" not in set_end_courses:
        courses.remove("Backend разработка")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
    
        set_end_courses.add("Backend разработка")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Blockchain_и_криптовалюты" and "Blockchain и криптовалюты" not in set_end_courses:
        courses.remove("Blockchain и криптовалюты")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("Blockchain и криптовалюты")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Цифровой_маркетинг" and "Цифровой маркетинг" not in set_end_courses:
        courses.remove("Цифровой маркетинг")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("Цифровой маркетинг")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Кибербезопасность" and "Кибербезопасность" not in set_end_courses:
        courses.remove("Кибербезопасность")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("Кибербезопасность")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Data_science" and "Data science" not in set_end_courses:
        print("Я В DS")
        courses.remove("Data science")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("Data science")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Финансовый_анализ" and "Финансовый анализ" not in set_end_courses:
        courses.remove("Финансовый анализ")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("Финансовый анализ")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")
    if course == "Frontend" and "Frontend разработка" not in set_end_courses:
        print("Я В FRONTEND!!!!!")
        courses.remove("Frontend разработка")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()

        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("Frontend разработка")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "IOS_разработчик" and "IOS разработчик" not in set_end_courses:
        courses.remove("IOS разработчик")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("IOS разработчик")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "SQL" and "SQL" not in set_end_courses:
        courses.remove("SQL")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("SQL")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "UX/UI_дизайн" and "UX/UI дизайн" not in set_end_courses:
        courses.remove("UX/UI дизайн")
        courses = str(courses)

        cursor.execute(
            """UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        set_end_courses.add("UX/UI дизайн")
        set_end_courses = str(set_end_courses)

        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        exp_num+=1000
        cursor.execute(
            """UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")
    else:
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def send_user_courses(request, course):
    """ Добавление курсов в бд """
    userNameSession = request.session.get("userName")

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    u_theme = cursor.fetchone()[0] or "theme1"
    print(u_theme)
    cursor.close()
    conn.close()

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_courses FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    courses = cursor.fetchone()[0]
    print(courses)
    if courses:
        courses = eval(courses)
    else:
        courses = {}
    course_set = set()

    course_set.update(courses)
    cursor.close()
    conn.close()

    print("User courses from db:", course_set)

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    if course == "UX_UI_дизайн":
        course_set.add("UX/UI дизайн")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                    (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "UX/UI дизайн", 
                                                           "course_url": "Закончить_UX/UI_дизайн", "u_theme": u_theme})
    
    if course == "Backend":
        if course not in end_user_course:
            course_set.add("Backend разработка")
            course_set = str(course_set)
            cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""", (course_set, userNameSession))

            conn.commit()

            cursor.close()
            conn.close()
            return render(request, "study_courses_page.html", {"course_name": "Backend разработка", 
                                    "course_url": "Закончить_Backend", "u_theme": u_theme})

        else:
            return render(request, "study_courses_page.html", {"course_name": "Backend разработка", 
                                                            "course_url": "Закончить_Backend", "u_theme": u_theme})

    if course == "Blockchain_и_криптовалюты":
        course_set.add("Blockchain и криптовалюты")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "Blockchain и криптовалюты",
                                                            "course_url": "Закончить_Blockchain_и_криптовалюты", "u_theme": u_theme})

    if course == "Цифровой_маркетинг":
        course_set.add("Цифровой маркетинг")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "Цифровой маркетинг",
                                                           "course_url": "Закончить_Цифровой_маркетинг", "u_theme": u_theme})

    if course == "Кибербезопасность":
        course_set.add("Кибербезопасность")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        conn.close()
        return render(request, "study_courses_page.html", {"course_name": "Кибербезопасность", 
                                                           "course_url": "Закончить_Кибербезопасность", "u_theme": u_theme})

    if course == "Data_science":
        course_set.add("Data science")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "Data science", 
                                                           "course_url": "Закончить_Data_science", "u_theme": u_theme})

    if course == "Финансовый_анализ":
        course_set.add("Финансовый анализ")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "Финансовый анализ", 
                                                           "course_url": "Закончить_Финансовый_анализ", "u_theme": u_theme})

    if course == "Frontend":
        course_set.add("Frontend разработка")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "Frontend разработка", 
                                                           "course_url": "Закончить_Frontend", "u_theme": u_theme})

    if course == "IOS_разработчик":
        course_set.add("IOS разработчик")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "IOS разработчик",
                                                           "course_url": "Закончить_IOS_разработчик", "u_theme": u_theme})

    if course == "SQL":
        course_set.add("SQL")
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                       (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        
        return render(request, "study_courses_page.html", {"course_name": "SQL", 
                                                           "course_url": "Закончить_SQL", "u_theme": u_theme})


def User_page(request):
    """ Вывод всей информации о пользователе на домашней странице """
    global img_src
    userNameSession = request.session.get("userName")

# ...Подтверждение pro у пользователя
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    dataPRO = (userNameSession, True)
    cursor.execute(
        """SELECT 1 FROM users WHERE user_name = %s AND pro = %s""", dataPRO)

    conn.commit()

    pro = cursor.fetchone()
    cursor.close()
    conn.close()

# ...Вывод url фото пользователя
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT photo_url FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()
    img_src = "https://brend-mebel.ru/image/no_image.jpg"
    res_img = cursor.fetchall()[0][0]
    print(res_img, "res_img")
    if res_img:
        img_src = res_img

    cursor.close()
    conn.close()

# ...Вывод описания профиля
    
    func_desc = take_desc(userNameSession)

    print(func_desc, "desc_")
    if func_desc is None:
        func_desc = "Hello world!"

# ...Вывод курсов пользователя
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT user_courses FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    user_courses = cursor.fetchone()[0]

    print(user_courses)
    if user_courses:
        user_courses = eval(user_courses)
    print(user_courses)

    cursor.close()
    conn.close()


# ...Вывод сертефикатов пользователя
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute("""SELECT user_certific FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    user_certific = cursor.fetchone()[0]

    if user_certific:
        user_certific = eval(user_certific)
    print(".............", user_certific)
    cursor.close()
    conn.close()

# ...Вывод и изменение темы сайта
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("u.............", u_theme)
    cursor.close()
    conn.close()

# ...Вывод xp пользователя
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT xp FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    exp = cursor.fetchone()[0]

    xp = 0
    if exp:
        xp = exp 

    cursor.close()
    conn.close()

# ...Вывод данных об достижениеях/ачивках
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute("""SELECT user_achiv FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    user_achievments = cursor.fetchone()[0]
    
    if user_achievments:
        user_achievments = eval(user_achievments)
    else:
        user_achievments = set()
    cursor.close()
    conn.close()

# ...Добавление в бд ачивки
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    if user_certific:
        if len(user_certific) == 1:
            user_achievments.add("Начало путешествия")
        if len(user_certific) == 3:
            user_achievments.add("Рыцарь знаний")
        if len(user_certific) == 5:
            user_achievments.add("Гений инноваций")
        if len(user_certific) == 8:
            user_achievments.add("Покоритель предметов")
    # Преобразование данных перед вставкой в html
    user_achievments = str(user_achievments)

    cursor.execute(
        """UPDATE users SET user_achiv = %s 
        WHERE user_name = %s""", (user_achievments, userNameSession))

    conn.commit()

    cursor.close()
    conn.close()

    user_achievments = eval(user_achievments)

    if pro:
        print("Есть pro")
        if func_desc:
            print("Есть описание")
            data = {"userName": userNameSession, "add": True,
                    "desc": func_desc, "img_src": img_src, "courses": user_courses, 
                    "user_certific": user_certific, "xp": xp, "user_achievments": user_achievments,
                    "u_theme": u_theme}
            return render(request, "user_room.html", context=data)

        # подтверждаем транзакцию
        data = {"userName": userNameSession, "add": True,
                "img_src": img_src, "courses": user_courses, "user_certific": user_certific, 
                "xp": xp, "user_achievments": user_achievments, "u_theme": u_theme}
        return render(request, "user_room.html", context=data)
    else:
        print("Нет про")
        if func_desc:
            print("Есть функция, без pro")
            data = {"userName": userNameSession, "add": False,
                    "desc": func_desc, "img_src": img_src, "courses": user_courses, 
                    "user_certific":user_certific, "xp": xp, "user_achievments": user_achievments,
                    "u_theme": u_theme}
            return render(request, "user_room.html", context=data)
        # подтверждаем транзакцию
        print("Нет описания")
        data = {"userName": userNameSession, "add": False,
                "img_src": "https://uhd.name/uploads/posts/2023-03/1678237559_uhd-name-p-kris-massolia-vkontakte-95.jpg", 
                "courses": user_courses, "user_certific": user_certific, "xp": xp, "user_achievments": user_achievments,
                "u_theme": u_theme}
        return render(request, "user_room.html", context=data)


def Auth(request):
    """ Страница аутенцикации """
    ufa = userFormAUTH()
    if request.method == "POST":
        userName = request.POST.get("_user_name")
        userPassword = request.POST.get("_password")
        
        request.session['userName'] = userName

        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                password="31415926", host="127.0.0.1")
        cursor = conn.cursor()

        user_data = (userName, userPassword)

        cursor.execute(
            "SELECT 1 FROM users WHERE user_name = %s AND user_passw = %s", user_data)
        result = cursor.fetchone()

        if result:
            return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")
        u_excp = "Проверьте правильность ввода."
        return render(request, "exception.html", context={"u_excp": u_excp})

    return render(request, "auth.html", {"forms": ufa})


def reg(request):
    """ Страница регестрации """
    userform = userFormREG()
    if request.method == "POST":
        if userform.is_valid():
            userName = userform.cleaned_data['user_name_']
            userEmail = userform.cleaned_data['user_email_']
            userPassw = userform.cleaned_data['password_']
            request.session['userNameREG'] = userName
            request.session['userEmailREG'] = userEmail
            request.session['userPasswREG'] = userPassw

    return render(request, "reg.html", {"form": userform})


def conf_to_reg(request):
    """ Отправка кода пользователю! Сейчас в связи с двойной аутенфикацией мне нельзя получить код.
    Код выводится в консоли """
    try:
        if request.method == "POST":
            userform = userFormREG(request.POST)

            if userform.is_valid():
                userName = userform.cleaned_data["user_name_"]
                userEmail = userform.cleaned_data["user_email_"]
                userPassw = userform.cleaned_data["password_"]
                print(userName, userEmail, userPassw)

                conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                        password="31415926", host="127.0.0.1")
                cursor = conn.cursor()
                print("Входим в проверку на дубликат")
                cursor.execute(
                    """SELECT COUNT(user_email) FROM users WHERE user_email = %s;""", (userEmail,))
                conn.commit()
                res = cursor.fetchone()
                print("All commit good!!!!!!!!")
                cursor.close()
                conn.close()
                print("выходим")

                if res[0] >= 1:
                    return render(request, "email_InDB_exception.html")
                
                # from_email = 'justkiddingboat@gmail.com'  #email
                # to_email = userEmail
                # password = "just123kidding"  # пароль двухфакторной аутенцикации

                # Рандомные 6 символов. Нужны для отправки и подтверждения email пользователя
                random_code = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=6))
                
                # # Эта часть кода нужна для тестирования. 
                # # Все сообщения при использовании этого кода будут появлятся в консоли
                subject = 'Ключ доступа LFtB'
                from_email = 'vladnety134@gmail.com'
                recipient_list = [userEmail]
                send_mail(subject, random_code, from_email,
                          recipient_list, fail_silently=False)
                
                # smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                # smtp_server.starttls()
                # smtp_server.login(from_email, password)

                # mime = MIMEText(f'Ваш код подтверждения: {random_code}', 'plain', 'utf-8')
                # print("CODE1111111", random_code)
                
                # # smtp_server.sendmail(from_email, to_email, mime.as_string())
                # # smtp_server.quit()
                request.session['generated_password'] = random_code
                request.session['userNameREG'] = userName
                request.session['userEmailREG'] = userEmail
                request.session['userPasswREG'] = userPassw
                data = {"userName": userName}
                return render(request, "confirmTOreg.html", context=data)

    except Exception as exc:
        print(f"Exception: {exc}")
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def confirm(request):
    """ Проверка кода из email """
    try:
        if request.method == "POST":

            # Получаем введенный пользователем код из формы
            userEnteredCode = request.POST.get("code6")

            # Получаем сгенерированный код из сессии
            generatedCode = request.session.get("generated_password")

            userNameSession = request.session.get("userNameREG")
            userEmailSession = request.session.get("userEmailREG")
            userPasswSession = request.session.get("userPasswREG")

            print(userNameSession, userEmailSession, userPasswSession)
            print("Начинается проверка пароля!!!!!!")
            if userEnteredCode == generatedCode:
                print("Пароль подошел!")
                conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                        password="31415926", host="127.0.0.1")
                cursor = conn.cursor()

                datatodb = (userNameSession, userEmailSession,
                            userPasswSession, None, False, 1, None, None, False)

                cursor.execute("""
                    INSERT INTO users (user_name, user_email, user_passw, 
                        user_courses, author, level, certif, 
                        achievements, pro)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, datatodb)
                # поддверждаем транзакцию
                conn.commit()
                print("All commit good!!!!!!!!")

                cursor.close()
                conn.close()
                return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")

            else:
                print("Пароль не подошел!(")
                # Коды не совпадают, выводим ошибку
                u_excp = "Неверный код."
                return render(request, "exception.html", context={"u_excp": u_excp})
    except Exception:
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def main_b_a(request):
    """ Главная страница после регестрации """
    use = userSearchEngine()

    userNameSession = request.session.get("userName")
    
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    u_theme = cursor.fetchone()[0] or "theme1"
    print(u_theme)
    cursor.close()
    conn.close()
    data = {"forms": use, "userName": userNameSession, "u_theme": u_theme}
    if request.method == "POST":
        if use.is_valid():
            # userRequest = use.cleaned_data["search_engine"]
            return render(request, "search_results.html")

    return render(request, "main_before_reg.html", context=data)


def catalog(request):
    """ Каталог курсов """
    userNameSession = request.session.get("userName")
    if userNameSession:
        try:
            conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                    password="31415926", host="127.0.0.1")
            cursor = conn.cursor()

            cursor.execute(
                """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

            conn.commit()

            u_theme = cursor.fetchone()[0] or "theme1"
            print(u_theme)
            cursor.close()
            conn.close()
            return render(request, "catalog.html", {"userName": userNameSession, "u_theme": u_theme})
        except Exception as e:
            print(e)
            # http://127.0.0.1:8000/Регистрация/
            u_excp = "Произошла какая-то ошибка."
            return render(request, "exception.html", context={"u_excp": u_excp})
    else:
        return render(request, 'catalog_exc.html')
    

def catalog_Frontend(request):
    userNameSession = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    print(u_theme)
    cursor.close()
    conn.close()
    return render(request, r"all_courses/CFrontend.html", context={"u_theme": u_theme})


def catalog_Cyber_security(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                        password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE user_name = %s and pro = true", (username, ))
    conn.commit()
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    print(result)
    if result is not None:
        return render(request, r"all_courses/Ccyber_security.html", context={"u_theme": u_theme})
    else:
        return render(request, "exception.html")


def catalog_Backend(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                        password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE user_name = %s and pro = true", (username, ))

    conn.commit()
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return render(request, r"all_courses/Cbackend.html", context={"u_theme": u_theme})
    return render(request, "exception.html")


def catalog_Cifra_marketing(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                        password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE user_name = %s and pro = true", (username, ))

    conn.commit()
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    print(result)
    return render(request, r"all_courses/Ccm.html", context={"u_theme": u_theme})


def catalog_Data_scince(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                        password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE user_name = %s and pro = true", (username, ))

    conn.commit()
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return render(request, r"all_courses/Cdata_science.html", context={"u_theme": u_theme})
    return render(request, "exception.html", context={'u_excp': "Приобретите Pro версию."})


def catalog_Fin_analitic(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    return render(request, r"all_courses/Cfa.html", context={"u_theme": u_theme})


def catalog_IOS(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    return render(request, r"all_courses/Cios.html", context={"u_theme": u_theme})


def catalog_SQL(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE user_name = %s and pro = true", (username, ))

    conn.commit()
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    print(result)
    return render(request, r"all_courses/Csql.html", context={"u_theme": u_theme})


def catalog_UX(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()
    return render(request, r"all_courses/CuxUi.html", context={"u_theme": u_theme})


def catalog_Blockchain(request):
    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]
    cursor.close()
    conn.close()

    username = request.session.get("userName")
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                        password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE user_name = %s and pro = true", (username, ))

    conn.commit()
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return render(request, r"all_courses/Cbc.html", context={"u_theme": u_theme})
    return render(request, "exception.html")


def pro(request):
    try:
        userNameSession = request.session.get("userName")

        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                password="31415926", host="127.0.0.1")
        cursor = conn.cursor()

        cursor.execute(
            """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

        conn.commit()

        u_theme = cursor.fetchone()
        print(u_theme)
        if u_theme is None:
            u_theme = "theme1"
        else:
            u_theme = u_theme[0]
        cursor.close()
        conn.close()
        return render(request, "ADDpro.html", context={"u_theme": u_theme})
    
    except Exception as e:
        print(e)
        u_excp = "Пожалуйста, войдите в учетную запись."
        return render(request, "exception.html", context={"u_excp": u_excp})


def quest(request):
    userNameSession = request.session.get("userName")

    if userNameSession:
        try:
            print(userNameSession)

            conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                    password="31415926", host="127.0.0.1")
            cursor = conn.cursor()

            cursor.execute(
                """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

            conn.commit()

            u_theme = cursor.fetchone()
            print(u_theme)
            if u_theme is None:
                u_theme = "theme1"
            else:
                u_theme = u_theme[0]
            cursor.close()
            conn.close()
            return render(request, "quest.html", context={"u_theme": u_theme})
        except Exception as e:
            print(e)
            u_excp = "Произошла какая-то ошибка."
            return render(request, "exception.html", context={"u_excp": u_excp})
    else:
        return render(request, 'quest.html', context={"u_theme": "theme1"})


def theme(request):
    """ Вывод и работа с настройками """

    userNameSession = request.session.get("userName")

    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    u_theme = cursor.fetchone()[0] or "theme1"
    print(u_theme)
    cursor.close()
    conn.close()

    st = select_theme()
    if request.method == "POST":

        user_name = request.POST.get("usernameSET")
        user_desc = request.POST.get("description")
        user_photo = request.POST.get("user_photo_url")
        user_theme = request.POST.get("user_theme")

        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                password="31415926", host="127.0.0.1")
        cursor = conn.cursor()
        conn.set_client_encoding('UTF8')

        if user_name:
            cursor.execute(
                "UPDATE users SET user_name = %s WHERE user_name = %s", (user_name, userNameSession))
            
            request.session['userName'] = user_name
        if user_desc:
            print(user_desc)
            cursor.execute(
                "UPDATE users SET user_desc = %s WHERE user_name = %s", (user_desc, userNameSession))
        if user_photo:
            cursor.execute(
                "UPDATE users SET photo_url = %s WHERE user_name = %s", (user_photo, userNameSession))
            print("changes photo")
        if user_theme:
            cursor.execute(
                "UPDATE users SET user_theme = %s WHERE user_name = %s", (user_theme, userNameSession))
        conn.commit()

        cursor.close()
        conn.close()
        return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./Профиль/")

    return render(request, "themes.html", {"form": st, "u_theme": u_theme})


def test(request):
    """ Тестовая функция """
    subject = 'Test Email'
    message = 'Hello, this is a test email.'
    from_email = 'vladnety134@gmail.com'
    recipient_list = ['vladnety134@gmail.com']
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)
    return HttpResponse("Hello")


def take_desc(username):
    """ Получить описание пользователя из бд """
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_desc FROM users WHERE user_name = %s", (username, ))

    result = cursor.fetchone()[0]
    print(result, "desc_res")

    cursor.close()
    conn.close()

    return result


def quit(request):
    del request.session['userName']
    return HttpResponseRedirect("http://127.0.0.1:8000/")


def payments(request):
    # username = request.session.get("userName")
    try:
        userNameSession = request.session.get("userName")
        print("UserNameSession", userNameSession)
        
        if userNameSession is not None:
            return render(request, "payments.html")
        else:
            u_excp = "Перед покупкой нужно зарегистрироваться!"
            return render(request, "exception.html", context={"u_excp": u_excp})
    except Exception as e:
        print(e)
        return render(request, "exception.html", context={"u_excp": "Произошла какая-то ошибка!"})