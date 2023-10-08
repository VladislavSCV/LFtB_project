""" Hello, world! This is main branch!!!"""
# Импорты django
from pprint import pformat
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

from loguru import logger

# Импорты форм для дальнейшего вывода пользователю
from .forms import userFormREG, userSearchEngine, userFormAUTH, select_theme

# Другие импорты
from sites.utils import db_handlers as db

# Строка для удаления сессии
# del request.session['userName']


""" Задачи """
""" 1. Нормализовать словари в json и собрать нормальное кол-во слов 
2. Решить все проблемы безопасности
3. Написать алгоритм рекомендации
4. Сделать красивый код на странице Cfrontend
5. Повторить доступ к описанию курса ко всем курсам(Frontend готов)
6. Возможность входить в описание курса даже без pro. Но начать pro курс можно только с pro или по цене
7. Добавить цены к курсам
8. Добавить градиент фоном для темной темы в каталоге"""


# Изображение пользователя если нет своего фото
img_src = "https://brend-mebel.ru/image/no_image.jpg"

# Словарь курсов для сравнения ввода пользователя с каждым из этих слов.
# Значением является коэффицент схожести слов
dct_courses = {
    (
        "Frontend Development",
        "Фронтенд разработка",
        "Разработка пользовательского интерфейса",
        "Frontend",
    ): 0,
    (
        "Data Science",
        "Анализ данных",
        "Машинное обучение",
        "Статистика",
        "Нейронные сети",
        "Большие данные",
        "Python",
    ): 0,
    (
        "Backend Development",
        "backend",
        "Бэкэнд разработка",
        "Серверная разработка",
        "Django",
        "Flask",
        "REST API",
    ): 0,
    (
        "Цифровой маркетинг",
        "реклама",
        "аналитика",
        "SEO",
        "SEM",
        "Email-маркетинг",
        "Контент-маркетинг",
    ): 0,
    (
        "Финансовый анализ",
        "баланс",
        "доходность",
        "рентабельность",
        "Финансовое планирование",
        "Инвестиции",
        "Аудит",
    ): 0,
    (
        "Blockchain и криптовалюты",
        "технология",
        "достоверность",
        "декентрализация",
        "майнинг",
        "Smart contracts",
        "Ethereum",
    ): 0,
    (
        "UX/UI дизайн",
        "интерфейс",
        "прототипирование",
        "визуальный",
        "Графический дизайн",
        "Motion design",
        "Adobe Photoshop",
    ): 0,
    (
        "IOS разработчик",
        "Разработка приложений для IOS",
        "Swift",
        "Objective-C",
        "Xcode",
        "UIKit",
        "Core Data",
    ): 0,
    (
        "SQL",
        "Реляционные базы данных",
        "Запросы SQL",
        "MySQL",
        "PostgreSQL",
        "Oracle",
        "Microsoft SQL Server",
    ): 0,
    (
        "Кибербезопасность",
        "Cyber security",
        "Защита информации",
        "Киберзащита",
        "Пентестинг",
        "Шифрование",
        "Firewall",
    ): 0,
}

# Словарь для вывода данных на страницу где пользователь может почитать о курсе и перейти к прохождению курса
dct_res_text = {
    "Frontend Development": [
        "Frontend Development",
        "Фронтенд-разработчики занимаются созданием пользовательского интерфейса для веб-приложений и сайтов, используя языки программирования HTML, CSS и JavaScript.",
        "Frontend_разработка/",
    ],
    "Data Science": [
        "Data Science",
        "Этот курс расскажет о базовых принципах анализа данных и машинного обучения. Студенты изучат методы сбора, обработки и интерпретации данных, а также научатся применять статистические модели для прогнозирования и принятия решений.",
        "Data_science/",
    ],
    "Backend Development": [
        "Backend Development",
        "Этот курс предлагает изучение серверной разработки, языков программирования и инструментов для создания мощных веб-приложений. Вы освоите Python, Ruby или Node.js, а также научитесь работать с базами данных, разрабатывать API и обеспечивать безопасность приложения.",
        "Backend_разработка/",
    ],
    "Цифровой маркетинг": [
        "Цифровой маркетинг",
        "Курс по цифровому маркетингу научит вас использовать социальные сети, контент-маркетинг и SEO для привлечения трафика и достижения бизнес-целей. Вы освоите создание и оптимизацию цифровых маркетинговых кампаний.",
        "Цифровой_маркетинг/",
    ],
    "Финансовый анализ": [
        "Финансовый анализ",
        "Этот курс представляет изучение основ финансового анализа и оценки состояния компаний. Студенты освоят различные инструменты и модели, необходимые для принятия обоснованных финансовых решений.",
        "Финансовый_анализ/",
    ],
    "Blockchain и криптовалюты": [
        "Blockchain и криптовалюты",
        "Курс, который позволяет понять концепции и технологии блокчейн, а также различные типы криптовалют. Вы научитесь использовать блокчейн для создания безопасных и надежных систем передачи данных и управления с децентрализованной структурой.",
        "Blockchain/",
    ],
    "UX/UI дизайн": [
        "UX/UI дизайн",
        "Этот курс научит создавать удобные и привлекательные пользовательские интерфейсы. Обучение включает основы UI/UX-дизайна, а также применение современных инструментов и методов для создания и тестирования дизайна.",
        "UX_UI_дизайн/",
    ],
    "IOS разработчик": [
        "IOS разработчик",
        "Курс по разработке мобильных приложений для устройств iOS с использованием языка программирования Swift и инструментов Apple. Студенты научатся создавать, поддерживать и обновлять приложения для iPhone, iPad и других устройств, работающих на iOS.",
        "IOS_разработка/",
    ],
    "SQL": [
        "SQL",
        "Декларативный язык программирования, применяемый для создания, модификации и управления данными в реляционной базе данных, управляемой соответствующей системой управления базами данных.",
        "SQL_разработка/",
    ],
    "Кибербезопасность": [
        "Кибербезопасность",
        "Направление связанное с разработкой и управлением систем информационной безопасности в организации.",
        "Cyber_security/",
    ],
}

# Словарь для хранения
dct = {}


def MainPage(request):
    """Вывод главной страницы курса.
    Когда пользователь еще не зарегистрирован или не вошел в уч запись"""

    use = userSearchEngine()
    # Если юзер зайдет через обычную ссылку и не выйдет из учетной записи, то
    # перейдет сразу на страницу после регистрации
    # В общем работае как авто сохранение в учетке
    try:
        if request.session["userName"]:
            return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")

    except Exception as e:
        logger.exception("")
        return render(request, "main.html", {"forms": use})


def levenshtein_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    # Создаем матрицу для хранения расстояний Левенштейна между префиксами слов
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Инициализируем первую строку и первый столбец матрицы
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Заполняем оставшуюся часть матрицы
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Удаление символа
                    dp[i][j - 1] + 1,  # Вставка символа
                    dp[i - 1][j - 1] + 1,  # Замена символа
                )

    return dp[m][n]


def res_search(request):
    """Вывод результатов поиска"""
    """ Тут было бы неплохо из запросов сделать транзакции """

    global dct_courses, dct_res_text

    # Получение имени пользователя из сессии
    userNameSession = request.session.get("userName")

    u_theme = db.get_one(userNameSession, "user_theme")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    lst = []
    if request.method == "POST":
        # Обработка данных, полученных из формы
        userReqqq = userSearchEngine(request.POST)
        if userReqqq.is_valid():
            user_word = userReqqq.cleaned_data["search_engine"]

            # Алгоритм Левенштейна работает с введенным словом
            for k, v in dct_courses.items():
                total_koef = 0
                for i in k:
                    koef_semiliar_word = levenshtein_distance(user_word, i)
                    total_koef += koef_semiliar_word

                dct_courses[k] = total_koef

                if total_koef <= 80:
                    lst.append(k[0])

            lst_result = []

            for i in lst:
                lst_result.append(dct_res_text[i])

            # Возвращение шаблона "search_results.html" с передачей списка lst и темы пользователя u_theme
            return render(
                request,
                "search_results.html",
                {"collection": lst_result, "u_theme": u_theme},
            )

    # Возврат шаблона "search_results.html" без данных
    return render(request, "search_results.html")


def end_user_course(request, course):
    """Функция для окончания курса."""

    # Получение ника из сессий
    userNameSession = request.session.get("userName")

    # Получение exp пользователя
    exp_num = db.get_one(userNameSession, "xp")

    # Получаем set курсов из бд. Тип данных: str
    courses_el = db.get_one(userNameSession, "user_courses")
    # Перевод курсов из str в set
    courses = eval(courses_el[0])
    logger.debug(f"Курсы пользователя '{userNameSession}': \n{pformat(courses)}")

    # Получаем set законченных курсов из бд. Тип данных: str
    # Вносим законченные курсы в переменную
    set_end_courses = db.get_one(userNameSession, "user_certific")

    if set_end_courses:
        # Перевод курсов из str в set
        set_end_courses = eval(set_end_courses[0])
    else:
        set_end_courses = set()

    logger.debug(
        f"Курсы пользователя '{userNameSession}': \n{pformat(set_end_courses)}"
    )

    if course == "Backend" and "Backend разработка" not in set_end_courses:
        # Мы удаляем его из действующих курсов
        courses.remove("Backend разработка")
        # множество курсов переводим в str формат для бд
        courses = str(courses)
        # Вносим изменения в бд
        db.update_one_parametr(
            user_name=userNameSession, key="user_courses", value=courses
        )

        set_end_courses.add("Backend разработка")
        set_end_courses = str(set_end_courses)
        # Добавляем в законченные курсы, чтобы пользователь мог получить сертификат
        db.update_one_parametr(
            key="user_sertific", value=set_end_courses, user_name=userNameSession
        ),

        # За прохождение курса полльзователю +1000 к xp
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession),

        # Возвращаем на страницу пользователя
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if (
        course == "Blockchain_и_криптовалюты"
        and "Blockchain и криптовалюты" not in set_end_courses
    ):
        courses.remove("Blockchain и криптовалюты")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),

        set_end_courses.add("Blockchain и криптовалюты")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),

        # Начисляем xp за то что закончил курс
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)

        # Переадресация юзера на страницу профиля | В будущем возможно изменим, чтобы он уходил в каталог
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Цифровой_маркетинг" and "Цифровой маркетинг" not in set_end_courses:
        courses.remove("Цифровой маркетинг")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("Цифровой маркетинг")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Кибербезопасность" and "Кибербезопасность" not in set_end_courses:
        courses.remove("Кибербезопасность")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("Кибербезопасность")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Data_science" and "Data science" not in set_end_courses:
        logger.warning("Я В DS")
        courses.remove("Data science")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("Data science")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "Финансовый_анализ" and "Финансовый анализ" not in set_end_courses:
        courses.remove("Финансовый анализ")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("Финансовый анализ")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")
    if course == "Frontend" and "Frontend разработка" not in set_end_courses:
        courses.remove("Frontend разработка")
        courses = str(courses)

        db.update_one_parametr(userNameSession, "user_courses", courses)
        set_end_courses.add("Frontend разработка")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "IOS_разработчик" and "IOS разработчик" not in set_end_courses:
        courses.remove("IOS разработчик")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("IOS разработчик")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "SQL" and "SQL" not in set_end_courses:
        courses.remove("SQL")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("SQL")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")

    if course == "UX/UI_дизайн" and "UX/UI дизайн" not in set_end_courses:
        courses.remove("UX/UI дизайн")
        courses = str(courses)

        db.update_one_parametr(
            key="user_courses", value=courses, user_name=userNameSession
        ),
        set_end_courses.add("UX/UI дизайн")
        set_end_courses = str(set_end_courses)

        db.update_one_parametr(
            key="user_certific", value=set_end_courses, user_name=userNameSession
        ),
        exp_num += 1000
        db.update_one_parametr(key="xp", value=exp_num, user_name=userNameSession)
        return HttpResponseRedirect("http://127.0.0.1:8000/Авторизация/Профиль/")
    else:
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def send_user_courses(request, course):
    """Добавление курсов в бд"""
    """ Тут было бы неплохо из запросов сделать транзакции """

    userNameSession = request.session.get("userName")

    # Получаем тему пользователя
    u_theme = db.get_one(userNameSession, "user_theme")

    logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    # Получаем действующие курс
    courses = db.get_one(userNameSession, "user_courses")
    logger.debug(f"Курсы пользователя '{userNameSession}': \n{pformat(courses)}")
    if courses:
        courses = eval(courses[0])
    else:
        courses = {}
    course_set = set()

    course_set.update(courses)

    logger.debug(f"User {userNameSession} courses from db:", course_set)

    # Если пользователь нажмет на кнопку 'начать курс' то он переходит в эти условия
    # В зависимости от кнопки пользователю добавляется определенный курс в бд
    if course == "UX_UI_дизайн":
        # В сет с курсами добавляется это
        course_set.add("UX/UI дизайн")
        # Переводим в str для бд
        # Потому что в postgres тип данных этого столбца text
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )
        # Переносим юзера на страницу с курсом
        return render(
            request, "study_courses_page/study_courses_ux_ui.html", {"u_theme": u_theme}
        )

    if course == "Backend":
        course_set.add("Backend разработка")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )
        return render(
            request,
            "study_courses_page\study_courses_Backend.html",
            {"u_theme": u_theme},
        )

    if course == "Blockchain_и_криптовалюты":
        course_set.add("Blockchain и криптовалюты")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request,
            "study_courses_page\study_courses_Blockchain.html",
            {"u_theme": u_theme},
        )

    if course == "Цифровой_маркетинг":
        course_set.add("Цифровой маркетинг")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request,
            "study_courses_page\study_courses_Cifrov_mark.html",
            {"u_theme": u_theme},
        )

    if course == "Кибербезопасность":
        course_set.add("Кибербезопасность")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request,
            "study_courses_page\study_courses_CyberS.html",
            {"u_theme": u_theme},
        )

    if course == "Data_science":
        course_set.add("Data science")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request,
            "study_courses_page\study_courses_DataScience.html",
            {"u_theme": u_theme},
        )

    if course == "Финансовый_анализ":
        course_set.add("Финансовый анализ")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request,
            "study_courses_page\study_courses_Finn_analiz.html",
            {"u_theme": u_theme},
        )

    if course == "Frontend":
        course_set.add("Frontend разработка")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request, "study_courses_page/study_Frontend.html", {"u_theme": u_theme}
        )

    if course == "IOS_разработчик":
        course_set.add("IOS разработчик")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request,
            "study_courses_page/study_IosDev.html",
            context={"u_theme": u_theme},
        )

    if course == "SQL":
        course_set.add("SQL")
        course_set = str(course_set)
        db.update_one_parametr(
            user_name=userNameSession, value=course_set, key="user_courses"
        )

        return render(
            request, "study_courses_page/study_courses_Sql.html", {"u_theme": u_theme}
        )


def User_page(request):
    """Вывод всей информации о пользователе на домашней странице"""

    global img_src
    userNameSession = request.session.get("userName")

    # ...Подтверждение pro у пользователя

    # maxz2024: Получай значение pro и проверяй когда выдаешь данные

    pro = db.get_one(userNameSession, "pro")

    # ...Вывод url фото пользователя
    res_img = db.get_one(user_name=userNameSession, parametr="photo_url")

    img_src = "https://brend-mebel.ru/image/no_image.jpg"
    logger.debug(f"Изображение пользователя '{userNameSession}': \n{res_img}")

    if res_img:
        img_src = res_img[0]

    # ...Вывод описания профиля
    func_desc = take_desc(userNameSession)

    logger.debug(f"Описание пользователя '{userNameSession}': \n{func_desc}")
    if func_desc is None:
        func_desc = "Hello world!"

    # ...Вывод курсов пользователя
    user_courses = db.get_one(userNameSession, "user_courses")

    logger.debug(f"Курсы пользователя '{userNameSession}': \n{pformat(user_courses)}")
    if user_courses:
        user_courses = eval(user_courses[0])
    logger.debug(f"Курсы пользователя '{userNameSession}': \n{pformat(user_courses)}")

    # ...Вывод сертефикатов пользователя

    user_certific = db.get_one(userNameSession, "user_sertific")

    if user_certific:
        user_certific = eval(user_certific[0])
    logger.debug(f"Сертификаты пользователя '{userNameSession}': \n{user_certific}")

    # ...Вывод и изменение темы сайта

    u_theme = db.get_one(userNameSession, "user_theme")
    logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")

    # maxz2024: добавил, не было проверки
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    # ...Вывод xp пользователя

    exp = db.get_one(userNameSession, "xp")

    xp = 0
    if exp:
        xp = exp[0]

    # ...Вывод данных об достижениеях/ачивках

    user_achievments = db.get_one(userNameSession, "user_achiv")

    if user_achievments:
        user_achievments = eval(user_achievments[0])
    else:
        user_achievments = set()

    # ...Добавление в бд ачивки
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

    db.update_one_parametr(
        key="user_achiv", value=user_achievments, user_name=userNameSession
    )

    user_achievments = eval(user_achievments)

    # 3 круга ада
    # Дай бог разобраться
    # Я думаю это стоит упростить, хотя кода может прибавиться
    if pro:
        if func_desc:
            data = {
                "userName": userNameSession,
                "add": True,
                "desc": func_desc,
                "img_src": img_src,
                "courses": user_courses,
                "user_certific": user_certific,
                "xp": xp,
                "user_achievments": user_achievments,
                "u_theme": u_theme,
            }
            return render(request, "user_room.html", context=data)

        data = {
            "userName": userNameSession,
            "add": True,
            "img_src": img_src,
            "courses": user_courses,
            "user_certific": user_certific,
            "xp": xp,
            "user_achievments": user_achievments,
            "u_theme": u_theme,
        }
        return render(request, "user_room.html", context=data)
    else:
        if func_desc:
            # Описание профиля есть
            # print("Есть функция, без pro")
            data = {
                "userName": userNameSession,
                "add": False,
                "desc": func_desc,
                "img_src": img_src,
                "courses": user_courses,
                "user_certific": user_certific,
                "xp": xp,
                "user_achievments": user_achievments,
                "u_theme": u_theme,
            }
            return render(request, "user_room.html", context=data)

        data = {
            "userName": userNameSession,
            "add": False,
            "img_src": "https://uhd.name/uploads/posts/2023-03/1678237559_uhd-name-p-kris-massolia-vkontakte-95.jpg",
            "courses": user_courses,
            "user_certific": user_certific,
            "xp": xp,
            "user_achievments": user_achievments,
            "u_theme": u_theme,
        }
        return render(request, "user_room.html", context=data)

    # maxz2024: Теоретически можно попробовать так:
    # data = {
    #         "userName": userNameSession,
    #         "add": False,
    #         "img_src": "https://uhd.name/uploads/posts/2023-03/1678237559_uhd-name-p-kris-massolia-vkontakte-95.jpg",
    #         "courses": user_courses,
    #         "user_certific": user_certific,
    #         "xp": xp,
    #         "user_achievments": user_achievments,
    #         "u_theme": u_theme,
    #     }
    # if pro:
    #     data["add"] = True

    # if func_desc:
    #     data["desc"] = func_desc

    # return render(request, "user_room.html", context=data)


def Auth(request):
    """Страница аутентификации"""

    ufa = userFormAUTH()
    if request.method == "POST":
        userName = request.POST.get("_user_name")
        userPassword = request.POST.get("_password")
        # Добавление в сессию ник юзера
        request.session["userName"] = userName
        # Вывод none если юзер есть в бд
        result = db.get_one(userName, "id")

        # Если пользователь в бд, то переходим на главную страницу для авторизованных
        if result:
            return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")
        else:
            # Иначе выводим ошибку
            u_excp = "Проверьте правильность ввода."
            return render(request, "exception.html", context={"u_excp": u_excp})

    return render(request, "auth.html", {"forms": ufa})


def reg(request):
    """Страница регистрации"""
    userform = userFormREG()
    return render(request, "reg.html", {"form": userform})


def send_email(to_email, subj, text):
    """Отпрака email пользователю
    Первый параметр это email нужного нам пользователя
    Второй - Тема письма
    Третий - Текст письма"""
    msg = MIMEMultipart()
    msg["From"] = "mighty.hiper@yandex.ru"
    msg["To"] = to_email
    msg["Subject"] = subj
    msg.attach(MIMEText(text, "plain"))
    server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
    server.ehlo("mighty.hiper@yandex.ru")
    server.login("mighty.hiper@yandex.ru", "rtuctelaovikxwfs")
    server.auth_plain()
    server.send_message(msg)
    server.quit()


def conf_to_reg(request):
    """Отправка кода подтверждения пользователю!"""
    try:
        if request.method == "POST":
            userform = userFormREG(request.POST)

            if userform.is_valid():
                userName = userform.cleaned_data["user_name_"]
                userEmail = userform.cleaned_data["user_email_"]
                userPassw = userform.cleaned_data["password_"]
                logger.debug("Получена информация: ", userName, userEmail, userPassw)
                logger.warning("Входим в проверку на дубликат")
                res = db.check_repeat_email(userEmail)
                # print("All commit good!!!!!!!!")
                logger.warning("выходим")

                if res[0] >= 1:
                    return render(request, "email_InDB_exception.html")
                # Генерируем рандомный пароль
                random_code = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=6)
                )

                send_email(userEmail, "LFtB-код подтверждение", random_code)

                request.session["generated_password"] = random_code
                request.session["userNameREG"] = userName
                request.session["userEmailREG"] = userEmail
                request.session["userPasswREG"] = userPassw
                data = {"userName": userName}
                return render(request, "confirmTOreg.html", context=data)

    except Exception as exc:
        logger.exception("")
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def confirm(request):
    """Проверка кода из email"""
    try:
        if request.method == "POST":
            # Получаем введенный пользователем код из формы
            userEnteredCode = request.POST.get("code6")

            # Получаем сгенерированный код из сессии
            generatedCode = request.session.get("generated_password")

            userNameSession = request.session.get("userNameREG")
            userEmailSession = request.session.get("userEmailREG")
            userPasswSession = request.session.get("userPasswREG")

            logger.debug(
                "Получена информация: ",
                userNameSession,
                userEmailSession,
                userPasswSession,
            )
            logger.warning("Начинается проверка пароля!!!!!!")
            if userEnteredCode == generatedCode:
                request.session["userName"] = userNameSession
                logger.warning("Пароль подошел!")

                datatodb = (
                    userNameSession,
                    userEmailSession,
                    userPasswSession,
                    0,
                    False,
                )
                # Вставляем в бд данные юзера
                db.add(data=datatodb)
                # print("All commit good!!!!!!!!")

                return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./")
            else:
                logger.warning("Пароль не подошел!(")
                # Коды не совпадают, выводим ошибку
                u_excp = "Неверный код."
                return render(request, "exception.html", context={"u_excp": u_excp})
    except Exception as e:
        logger.exception("")
        u_excp = "Произошла какая-то ошибка. Попробуйте позже."
        return render(request, "exception.html", context={"u_excp": u_excp})


def main_b_a(request):
    """Главная страница после регестрации"""
    try:
        use = userSearchEngine()

        userNameSession = request.session.get("userName")

        u_theme = db.get_one(userNameSession, "user_theme")
        logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
        if u_theme is None:
            u_theme = "theme1"
        else:
            u_theme = u_theme[0]

        data = {"forms": use, "userName": userNameSession, "u_theme": u_theme}
        if request.method == "POST":
            if use.is_valid():
                # userRequest = use.cleaned_data["search_engine"]

                return render(request, "search_results.html")

        return render(request, "main_before_reg.html", context=data)
    except HttpResponseServerError("Server Error") as e:
        logger.exception("")
        HttpResponseServerError("Server Error")


def catalog(request):
    """Каталог курсов"""
    userNameSession = request.session.get("userName")
    if userNameSession:
        try:
            u_theme = db.get_one(userNameSession, "user_theme")
            logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
            if u_theme is None:
                u_theme = "theme1"
            else:
                u_theme = u_theme[0]

            return render(
                request,
                "catalog.html",
                {"userName": userNameSession, "u_theme": u_theme},
            )
        except Exception as e:
            logger.exception("")
            # http://127.0.0.1:8000/Регистрация/
            u_excp = "Произошла какая-то ошибка."

            return render(request, "exception.html", context={"u_excp": u_excp})
    else:
        return render(request, "catalog_exc.html")


""" На основе этой функции нужно сделать остальные. Но нужно учитывать доступность курсов! """


def catalog_Frontend(request):
    """Страница Frontend разработки"""
    user_vision = True
    try:
        userNameSession = request.session.get("userName")

        u_theme = db.get_one(userNameSession, "user_theme")
        logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
        if u_theme is None:
            u_theme = "theme1"
        else:
            u_theme = u_theme[0]

        return render(
            request,
            r"all_courses/CFrontend.html",
            context={"u_theme": u_theme, "user_vision": user_vision},
        )

    except Exception as e:
        logger.exception("")
        user_vision = False
        return render(
            request,
            r"all_courses/CFrontend.html",
            context={"u_theme": "theme1", "user_vision": user_vision},
        )


def catalog_Cyber_security(request):
    """Страница Кибербезопасности"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")

    logger.debug(f"Статус про пользователя '{username}': \n{result}")
    if result is not None:
        return render(
            request, r"all_courses/Ccyber_security.html", context={"u_theme": u_theme}
        )
    else:
        return render(
            request, "exception.html", context={"u_excp": "Приобретите Pro версию."}
        )


def catalog_Backend(request):
    """Страница Backend"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")
    logger.debug(f"Статус про пользователя '{username}': \n{result}")
    if result:
        return render(
            request, r"all_courses/Cbackend.html", context={"u_theme": u_theme}
        )

    return render(
        request, "exception.html", context={"u_excp": "Приобретите Pro версию."}
    )


def catalog_Cifra_marketing(request):
    """Страница Цифрового маркетинга"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")

    logger.debug(f"Статус про пользователя '{username}': \n{result}")
    return render(request, r"all_courses/Ccm.html", context={"u_theme": u_theme})


def catalog_Data_scince(request):
    """Страница Data science"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")
    logger.debug(f"Статус про пользователя '{username}': \n{result}")
    
    if result:
        return render(
            request, r"all_courses/Cdata_science.html", context={"u_theme": u_theme}
        )

    return render(
        request, "exception.html", context={"u_excp": "Приобретите Pro версию."}
    )


def catalog_Fin_analitic(request):
    """Страница Финансовой аналитики"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    return render(request, r"all_courses/Cfa.html", context={"u_theme": u_theme})


def catalog_IOS(request):
    """Страница IOS"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")
    logger.debug(f"Статус про пользователя '{username}': \n{result}")
    
    if result:
        return render(request, r"all_courses/Cios.html", context={"u_theme": u_theme})
    return render(
        request, "exception.html", context={"u_excp": "Приобретите Pro версию."}
    )


def catalog_SQL(request):
    """Страница SQL"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")
    logger.debug(f"Статус про пользователя '{username}': \n{result}")

    return render(request, r"all_courses/Csql.html", context={"u_theme": u_theme})


def catalog_UX(request):
    """Страница UX/UI"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    return render(request, r"all_courses/CuxUi.html", context={"u_theme": u_theme})


def catalog_Blockchain(request):
    """Страница Блокчейна"""
    username = request.session.get("userName")
    u_theme = db.get_one(username, "user_theme")
    logger.debug(f"Тема пользователя '{username}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    result = db.get(username, "pro")
    logger.debug(f"Статус про пользователя '{username}': \n{result}")
    
    if result:
        return render(request, r"all_courses/Cbc.html", context={"u_theme": u_theme})

    return render(request, "exception.html")


def pro(request):
    """Страница с плюсами про версии"""
    try:
        userNameSession = request.session.get("userName")

        u_theme = db.get_one(userNameSession, "user_theme")
        logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
        if u_theme is None:
            u_theme = "theme1"
        else:
            u_theme = u_theme[0]

        result = db.get(userNameSession, "pro")
        logger.debug(f"Статус про пользователя '{userNameSession}': \n{result}")
        
        return render(request, "ADDpro.html", context={"u_theme": u_theme})

    except Exception as e:
        logger.exception("")
        u_excp = "Пожалуйста, войдите в учетную запись."

        return render(request, "exception.html", context={"u_excp": u_excp})


def quest(request):
    """Квесты"""

    userNameSession = request.session.get("userName")
    if userNameSession:
        try:
            logger.debug(f"Пользователь '{userNameSession}'")

            u_theme = db.get_one(userNameSession, "user_theme")
            logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
            if u_theme is None:
                u_theme = "theme1"
            else:
                u_theme = u_theme[0]

            return render(request, "quest.html", context={"u_theme": u_theme})
        except Exception as e:
            logger.exception("")
            u_excp = "Произошла какая-то ошибка."

            return render(request, "exception.html", context={"u_excp": u_excp})
    else:
        return render(request, "quest.html", context={"u_theme": "theme1"})


def theme(request):
    """Вывод и работа с настройками"""

    userNameSession = request.session.get("userName")

    u_theme = db.get_one(userNameSession, "user_theme")
    logger.debug(f"Тема пользователя '{userNameSession}': \n{u_theme}")
    if u_theme is None:
        u_theme = "theme1"
    else:
        u_theme = u_theme[0]

    st = select_theme()
    if request.method == "POST":
        user_name = request.POST.get("usernameSET")
        user_desc = request.POST.get("description")
        user_photo = request.POST.get("user_photo_url")
        user_theme = request.POST.get("user_theme")

        request.session["userName"] = user_name

        db.update_all_parametr(
            userNameSession,
            {
                "user_name": user_name,
                "user_desc": user_desc,
                "photo_url": user_photo,
                "user_theme": user_theme,
            },
        )

        return HttpResponseRedirect("http://127.0.0.1:8000/Главная_страница./Профиль/")

    return render(request, "themes.html", {"form": st, "u_theme": u_theme})


def test(request):
    """Тестовая функция | ДЛя проверки фич"""
    subject = "Test Email"
    message = "Hello, this is a test email."
    from_email = "vladnety134@gmail.com"
    recipient_list = ["vladnety134@gmail.com"]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return HttpResponse("Hello")


def take_desc(username):
    """Получить описание пользователя из бд"""
    result = db.get_one(user_name=username, parametr="users_desc")
    logger.debug(f"Описание пользователя '{username}': \n{result}")

    return result


# Выход из учетной записи на главной странице
def quit(request):
    del request.session["userName"]

    return HttpResponseRedirect("http://127.0.0.1:8000/")


def payments(request):
    """Страница с вводом данных карты"""
    # username = request.session.get("userName")
    try:
        userNameSession = request.session.get("userName")
        logger.debug(f"Пользователь '{userNameSession}'")

        if userNameSession is not None:
            return render(request, "payments.html")
        else:
            u_excp = "Перед покупкой нужно зарегистрироваться!"

            return render(request, "exception.html", context={"u_excp": u_excp})
    except Exception as e:
        logger.exception("")

        return render(
            request, "exception.html", context={"u_excp": "Произошла какая-то ошибка!"}
        )
