""" Тут находятся функции которые не работают """
# Вылетает ошибка 500 во всех функциях


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

    
""" ................................................................................................... """


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

    if course == "Backend":
        course_add("Backend разработка", "study_courses_page_Backend")

    if course == "Blockchain_и_криптовалюты":
        course_add("Blockchain и криптовалюты", "study_courses_page_Blockchain")

    if course == "Цифровой_маркетинг":
        course_add("Цифровой маркетинг", "study_courses_page_Cifrov_mark")

    if course == "Кибербезопасность":
        course_add("Кибербезопасность")

    if course == "Data_science":
        course_add("Data science", "study_courses_page_DataScience")

    if course == "Финансовый_анализ":
        course_add("Финансовый анализ", "study_courses_Finn_analiz")

    if course == "Frontend":
        course_add("Frontend разработка", "study_courses_page_Frontend")

    if course == "IOS_разработчик":
        course_add("IOS разработчик", "study_courses_page_IosDev")

    if course == "SQL":
        course_add("SQL", "study_courses_page_Sql")