# Импорты django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.http import HttpResponseServerError

# Импорты для рассылки email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random

# from yoomoney import Quickpay
# from yoomoney import Client
# import asyncio

# Либа для работы со строками
import string

# Либа для модели ml
import spacy
# Либа для postgresql
import psycopg2

# Импорты форм для дальнейшего вывода пользователю
from .forms import userFormREG, userSearchEngine, userFormAUTH, select_theme

# Строка для удаления сессии
# del request.session['userName']


# """ Задачи LFtB для Максимки """
# """ 
# 1. Нужно постараться сделать версии страниц сайта для телефона, планшета
# 2. Исправить ошибки и pep8 в коде views
# 3. Через некоторое время создать датасет
# 4. По возможности создать бота (Над этим еще стоит порассуждать)(Будем делать вместе)
# 5. Оптимизировать код и улучшить читабельность
# """


# """ Задачи LFtB для WhatIsLove """
# """
# 1. По возможности создать бота (Над этим еще стоит порассуждать)(Будем делать вместе) 
# 2. Продолжать украшать страницы с помощью frontend стека(html, css, js)
# 3. Буду начинать создавать модель для поисковой строки 
# 4. Нужно будет поработать с бд(Уйма изменений)
# """

# Изображение пользователя если нет своего фото
img_src = "https://brend-mebel.ru/image/no_image.jpg"

# Словарь курсов для сравнения ввода пользователя с каждым из этих слов.
# Значением является коэффицент схожести слов 
dct_courses = {
    ("Frontend Development", "Фронтенд разработка", "Разработка пользовательского интерфейса", "Фронтенд программирование", "Фронтэнд верстка", "HTML", "CSS"): 0,
    ("Data Science", "Анализ данных", "Машинное обучение", "Статистика", "Нейронные сети", "Большие данные", "Python"): 0,
    ("Backend Development", 'backend', "Бэкэнд разработка", "Серверная разработка", "Django", "Flask", "REST API"): 0,
    ("Цифровой маркетинг", "реклама", "аналитика", "SEO", "SEM", "Email-маркетинг", "Контент-маркетинг"): 0,
    ("Финансовый анализ", "баланс", "доходность", "рентабельность", "Финансовое планирование", "Инвестиции", "Аудит"): 0,
    ("Blockchain и криптовалюты", "технология", "достоверность", "декентрализация", "майнинг", "Smart contracts", "Ethereum"): 0,
    ("UX/UI дизайн", "интерфейс", "прототипирование", "визуальный", "Графический дизайн", "Motion design", "Adobe Photoshop"): 0,
    ("IOS разработчик", 'Разработка приложений для IOS', 'Swift', "Objective-C", "Xcode", "UIKit", "Core Data"): 0,
    ("SQL", 'Реляционные базы данных', 'Запросы SQL', "MySQL", "PostgreSQL", "Oracle", "Microsoft SQL Server"): 0,
    ("Кибербезопасность", "Cyber security", 'Защита информации', 'Киберзащита', "Пентестинг", "Шифрование", "Firewall"): ''
}

# Словарь для вывода данных на страницу где пользователь может почитать о курсе и перейти к прохождению курса 
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

# Словарь для хранения
dct = {}

security_db = {"dbname": "LFtB", "user": "postgres", "password": "31415926", "host": "127.0.0.1"}


def MainPage(request):
    """ Вывод главной страницы курса.
    Когда пользователь еще не зарегистрирован или не вошел в уч запись"""

    use = userSearchEngine()
# Если юзер зайдет через обычную ссылку и не выйдет из учетной записи, то 
# перейдет сразу на страницу после регистрации
# В общем работае как авто сохранение в учетке
    try:
        request.session["userName"]
        return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")
    except Exception as e:
        print(e)
        return render(request, "main.html", {'forms': use})
    

def res_search(request):
    """ Вывод результатов поиска """
    """ Тут было бы неплохо из запросов сделать транзакции """

    global dct_courses, dct_res_text

    # Получение имени пользователя из сессии
    userNameSession = request.session.get("userName")

    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    # Выполнение SQL-запроса для получения темы пользователя
    cursor.execute("""SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    u_theme = cursor.fetchone()
    print(u_theme)
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    # Закрытие курсора и соединения с базой данных
    cursor.close()
    conn.close()

    lst = []
    print(f"lst: {lst}")
    if request.method == "POST":
        # Обработка данных, полученных из формы
        userReqqq = userSearchEngine(request.POST)
        if userReqqq.is_valid():
            # Получение введенного пользователем запроса
            user_req = userReqqq.cleaned_data['search_engine']

            # Загрузка модели NLP
            nlp = spacy.load("en_core_web_sm")
            word1 = nlp(user_req)

            # Создание пустого словаря dct_res

            for i in dct_courses.keys():
                res_num = 0
                for j in i:
                    word2 = nlp(j)
                    k = word1.similarity(word2)
                    res_num += k
                dct_courses[i] = str(res_num)

            # Проверка результатов поиска и добавление соответствующих текстов в список lst
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

            # Возвращение шаблона "search_results.html" с передачей списка lst и темы пользователя u_theme
            return render(request, "search_results.html", {"collection": lst, "u_theme": u_theme})

    # Возврат шаблона "search_results.html" без данных
    return render(request, "search_results.html")


def end_user_course(request, course):
    """ Функция для окончания курса. """

    # Получение ника из сессий
    userNameSession = request.session.get("userName")

    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    # Запрос к бд для вывода
    cursor.execute("""SELECT xp FROM users WHERE user_name = %s""", (userNameSession, ))

    # Коммит для подтверждения запроса
    conn.commit()

    # Получение exp пользователя и отправка в бд
    exp_num = cursor.fetchone()[0]

    # Закрытие курсора и подключения
    cursor.close()
    conn.close()

    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()
    # async
    # Получаем set курсов из бд. Тип данных: str
    cursor.execute("""SELECT user_courses FROM users WHERE user_name = %s""", (userNameSession, ))

    # Подтверждение запроса
    conn.commit()

    # Перевод курсов из str в set
    courses = eval(cursor.fetchone()[0])
    print(courses)

    # Закрытие курсора и подключения
    cursor.close()
    conn.close()

    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()
# async
    # Получаем set законченных курсов из бд. Тип данных: str
    cursor.execute("""SELECT user_certific FROM users WHERE user_name = %s""", (userNameSession, ))

    # Подтверждение запроса
    conn.commit()

    # Вносим законченные курсы в переменную
    set_end_courses = cursor.fetchone()[0]

    if set_end_courses:
        # Перевод курсов из str в set
        set_end_courses = eval(set_end_courses)
    else:
        set_end_courses = set()

    print(set_end_courses)

    # Закрытие курсора и подключения
    cursor.close()
    conn.close()

    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    def close_course(name_course):
        global exp_num
        # Мы удаляем его из действующих курсов
        courses.remove(name_course)
        # множество курсов переводим в str формат для бд
        courses = str(courses)
        # Вносим изменения в бд
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""", (courses, userNameSession))
        conn.commit()
        
        # Закрытие курсора и подключения
        cursor.close()
        conn.close()

        conn = psycopg2.connect(**security_db)
        cursor = conn.cursor()

        set_end_courses.add(name_course)
        set_end_courses = str(set_end_courses)
        # Добавляем в законченные курсы, чтобы пользователь мог получить сертификат
        cursor.execute("""UPDATE users SET user_certific = %s WHERE user_name = %s""", (set_end_courses, userNameSession))
        conn.commit()

        # Закрытие курсора и подключения
        cursor.close()
        conn.close()

        conn = psycopg2.connect(**security_db)
        cursor = conn.cursor()
        # За прохождение курса полльзователю +1000 к xp
        exp_num += 1000
        cursor.execute("""UPDATE users SET xp = %s WHERE user_name = %s""", (exp_num, userNameSession))
        conn.commit()

        # Закрытие курсора и подключения
        cursor.close()
        conn.close()
        # Возвращаем на страницу пользователя
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")
    
    if course == "Backend" and "Backend разработка" not in set_end_courses:
        close_course("Backend разработка")

    elif course == "Цифровой_маркетинг" and "Цифровой маркетинг" not in set_end_courses:
        close_course("Цифровой маркетинг")

    elif course == "Кибербезопасность" and "" not in set_end_courses:
        close_course("Кибербезопасность")

    elif course == "Data_science" and "Data science" not in set_end_courses:
        print("Я В DS")
        close_course("Data science")
        
    elif course == "Финансовый_анализ" and "Финансовый анализ" not in set_end_courses:
        close_course("Финансовый анализ")
        
    elif course == "Frontend" and "Frontend разработка" not in set_end_courses:
        close_course("Frontend разработка")

    elif course == "IOS_разработчик" and "IOS разработчик" not in set_end_courses:
        close_course("IOS разработчик")

    elif course == "SQL" and "SQL" not in set_end_courses:
        close_course("SQL")

    elif course == "UX/UI_дизайн" and "UX/UI дизайн" not in set_end_courses:
        close_course("UX/UI дизайн")
        
    else:
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def send_user_courses(request, course):
    """ Добавление курсов в бд """
    """ Тут было бы неплохо из запросов сделать транзакции """

    userNameSession = request.session.get("userName")

    # Получаем тему пользователя
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    u_theme = cursor.fetchone()[0] or "theme1"
    print(u_theme)
    cursor.close()
    conn.close()

    # Получаем действующие курс
    conn = psycopg2.connect(**security_db)
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

    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()
    
    def course_add(name_course, url_cource):
        # В сет с курсами добавляется это
        course_set.add(name_course)
        # Переводим в str для бд
        # Потому что в postgres тип данных этого столбца text
        course_set = str(course_set)
        cursor.execute("""UPDATE users SET user_courses = %s WHERE user_name = %s""",
                        (course_set, userNameSession))

        conn.commit()

        cursor.close()
        conn.close()
        # Переносим юзера на страницу с курсом
        return render(request, f"study_courses_page/{url_cource}.html", {"u_theme": u_theme})
    
# Если пользователь нажмет на кнопку 'начать курс' то он переходит в эти условия
# В зависимости от кнопки пользователю добавляется определенный курс в бд
    if course == "UX_UI_дизайн":
        # В сет с курсами добавляется это
        course_add("UX/UI дизайн", "study_courses_page_ux_ui")
        
    elif course == "Backend":
        course_add("Backend разработка", "study_courses_page_Backend")

    elif course == "Blockchain_и_криптовалюты":
        course_add("Blockchain и криптовалюты", "study_courses_page_Blockchain")

    elif course == "Цифровой_маркетинг":
        course_add("Цифровой маркетинг", "study_courses_page_Cifrov_mark")

    elif course == "Кибербезопасность":
        course_add("Кибербезопасность")

    elif course == "Data_science":
        course_add("Data science", "study_courses_page_DataScience")

    elif course == "Финансовый_анализ":
        course_add("Финансовый анализ", "study_courses_page_Finn_analiz")

    elif course == "Frontend":
        course_add("Frontend разработка", "study_courses_page_Frontend")

    elif course == "IOS_разработчик":
        course_add("IOS разработчик", "study_courses_page_IosDev")

    elif course == "SQL":
        course_add("SQL","study_courses_page_Sql")


def User_page(request):
    """ Вывод всей информации о пользователе на домашней странице """

    global img_src
    userNameSession = request.session.get("userName")

# ...Подтверждение pro у пользователя
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    dataPRO = (userNameSession, True)
    cursor.execute(
        """SELECT 1 FROM users WHERE user_name = %s AND pro = %s""", dataPRO)

    conn.commit()

    pro = cursor.fetchone()
    cursor.close()
    conn.close()

# ...Вывод url фото пользователя
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT photo_url FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()
    img_src = "https://brend-mebel.ru/image/no_image.jpg"
    res_img = cursor.fetchone()[0]
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
    conn = psycopg2.connect(**security_db)
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
    conn = psycopg2.connect(**security_db)
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
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("u.............", u_theme)
    cursor.close()
    conn.close()

# ...Вывод xp пользователя
    conn = psycopg2.connect(**security_db)
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
    conn = psycopg2.connect(**security_db)
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
    conn = psycopg2.connect(**security_db)
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

# 3 круга ада
# Дай бог разобраться 
# Я думаю это стоит упростить, хотя кода может прибавиться
    if pro:

        if func_desc:
            data = {"userName": userNameSession, "add": True,
                    "desc": func_desc, "img_src": img_src, "courses": user_courses, 
                    "user_certific": user_certific, "xp": xp, "user_achievments": user_achievments,
                    "u_theme": u_theme}
            return render(request, "user_room.html", context=data)

        data = {"userName": userNameSession, "add": True,
                "img_src": img_src, "courses": user_courses, "user_certific": user_certific, 
                "xp": xp, "user_achievments": user_achievments, "u_theme": u_theme}
        return render(request, "user_room.html", context=data)
    else:

        if func_desc:
            # Описание профиля есть
            print("Есть функция, без pro")
            data = {"userName": userNameSession, "add": False,
                    "desc": func_desc, "img_src": img_src, "courses": user_courses, 
                    "user_certific": user_certific, "xp": xp, "user_achievments": user_achievments,
                    "u_theme": u_theme}
            return render(request, "user_room.html", context=data)

        data = {"userName": userNameSession, "add": False,
                "img_src": "https://uhd.name/uploads/posts/2023-03/1678237559_uhd-name-p-kris-massolia-vkontakte-95.jpg", 
                "courses": user_courses, "user_certific": user_certific, "xp": xp, "user_achievments": user_achievments,
                "u_theme": u_theme}
        return render(request, "user_room.html", context=data)


def Auth(request):
    """Страница аутентификации"""

    ufa = userFormAUTH()
    if request.method == "POST":
        userName = request.POST.get("_user_name")
        userPassword = request.POST.get("_password")
        # Добавление в сессию ник юзера
        request.session['userName'] = userName

        conn = psycopg2.connect(**security_db)
        cursor = conn.cursor()
        # Вывод 1 если юзер есть в бд
        cursor.execute("SELECT 1 FROM users WHERE user_name = %s AND user_passw = %s", (userName, userPassword))
        result = cursor.fetchone()

        conn.close()
        # Если пользователь в бд, то переходим на главную страницу для авторизованных
        if result:
            return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")
        else:
            # Иначе выводим ошибку
            u_excp = "Проверьте правильность ввода."
            return render(request, "exception.html", context={"u_excp": u_excp})

    return render(request, "auth.html", {"forms": ufa})


def reg(request):
    """ Страница регистрации """
    userform = userFormREG()
    return render(request, "reg.html", {"form": userform})


def send_email(to_email, subj, text):
    """ Отпрака email пользователю
    Первый параметр это email нужного нам пользователя
    Второй - Тема письма
    Третий - Текст письма"""
    msg = MIMEMultipart()
    msg['From'] = 'mighty.hiper@yandex.ru'
    msg['To'] = to_email
    msg['Subject'] = subj
    msg.attach(
        MIMEText(text, 'plain')
    )
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo('mighty.hiper@yandex.ru')
    server.login('mighty.hiper@yandex.ru', 'rtuctelaovikxwfs')
    server.auth_plain()
    server.send_message(msg)
    server.quit()


def conf_to_reg(request):
    """ Отправка кода подтверждения пользователю! """
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
                # Генерируем рандомный пароль
                random_code = ''.join(random.choices(string.ascii_uppercase+string.digits, k=6))
                
                send_email(userEmail, 'LFtB-код подтверждение', random_code)
                
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
                request.session['userName'] = userNameSession
                print("Пароль подошел!")

                conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                        password="31415926", host="127.0.0.1")
                cursor = conn.cursor()

                datatodb = (userNameSession, userEmailSession,
                            userPasswSession, 0, False)
                # Вставляем в бд данные юзера
                cursor.execute("""
                    INSERT INTO users (user_name, user_email, user_passw, xp, pro)
                        VALUES(%s, %s, %s, %s, %s)
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
    except Exception as e:
        print(e)
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def main_b_a(request):
    """ Главная страница после регестрации """
    try:
        use = userSearchEngine()

        userNameSession = request.session.get("userName")
        
        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                password="31415926", host="127.0.0.1")
        cursor = conn.cursor()

        cursor.execute(
            """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

        conn.commit()

        u_theme = cursor.fetchone()
        print(u_theme)
        if u_theme[0] is None:
            u_theme = "theme1"
        else:
            u_theme = u_theme[0]
        cursor.close()
        conn.close()
        data = {"forms": use, "userName": userNameSession, "u_theme": u_theme}
        if request.method == "POST":
            if use.is_valid():
                # userRequest = use.cleaned_data["search_engine"]

                return render(request, "search_results.html")

        return render(request, "main_before_reg.html", context=data)
    except HttpResponseServerError("Server Error") as e:
        print(e)
        HttpResponseServerError("Server Error")


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

            u_theme = cursor.fetchone()[0]
            print("Theme", u_theme)
            if u_theme is None:
                u_theme = "theme1"
            else:
                u_theme = u_theme

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
    """ Страница Frontend разработки """
    userNameSession = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

    print(u_theme)
    cursor.close()
    conn.close()

    return render(request, r"all_courses/CFrontend.html", context={"u_theme": u_theme})


def catalog_Cyber_security(request):
    """ Страница Кибербезопасности """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

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
    """ Страница Backend """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

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
    """ Страница Цифрового маркетинга """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

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
    """ Страница Data science """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

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
    """ Страница Финансовой аналитики """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

    cursor.close()
    conn.close()
    
    return render(request, r"all_courses/Cfa.html", context={"u_theme": u_theme})


def catalog_IOS(request):
    """ Страница IOS """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

    cursor.close()
    conn.close()

    return render(request, r"all_courses/Cios.html", context={"u_theme": u_theme})


def catalog_SQL(request):
    """ Страница SQL """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT user_theme FROM users WHERE user_name = %s""", (username, ))
    conn.commit()

    u_theme = cursor.fetchone()[0]
    print("Theme", u_theme)
    if u_theme is None:
        u_theme = "theme1"

    cursor.close()
    conn.close()
    
    conn = psycopg2.connect(**security_db)
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
    """ Страница UX/UI """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
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
    """ Страница Блокчейна """
    username = request.session.get("userName")
    conn = psycopg2.connect(**security_db)
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
    """ Страница с плюсами про версии """
    try:
        userNameSession = request.session.get("userName")

        conn = psycopg2.connect(dbname="LFtB", user="postgres",
                                password="31415926", host="127.0.0.1")
        cursor = conn.cursor()

        cursor.execute(
            """SELECT user_theme FROM users WHERE user_name = %s""", (userNameSession, ))

        conn.commit()

        u_theme = cursor.fetchone()[0]
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
    """ Квесты """

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

            u_theme = cursor.fetchone()[0]
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

    conn = psycopg2.connect(**security_db)
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
        # Если пользователь изменит хотя бы один параметр, то изменения уйдут в бд
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
    """ Тестовая функция | ДЛя проверки фич"""
    subject = 'Test Email'
    message = 'Hello, this is a test email.'
    from_email = 'vladnety134@gmail.com'
    recipient_list = ['vladnety134@gmail.com']
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)
    return HttpResponse("Hello")


def take_desc(username):
    """ Получить описание пользователя из бд """
    conn = psycopg2.connect(**security_db)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_desc FROM users WHERE user_name = %s", (username, ))

    result = cursor.fetchone()[0]
    print(result, "desc_res")

    cursor.close()
    conn.close()

    return result


# Выход из учетной записи на главной странице
def quit(request):

    del request.session['userName']

    return HttpResponseRedirect("http://127.0.0.1:8000/")


def payments(request):
    """ Страница с вводом данных карты """
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