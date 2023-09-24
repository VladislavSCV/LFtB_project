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
                    dp[i - 1][j] + 1,   # Удаление символа
                    dp[i][j - 1] + 1,   # Вставка символа
                    dp[i - 1][j - 1] + 1  # Замена символа
                )

    return dp[m][n]


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

            # Алгоритм Левенштенйна работает с введенным словом
            for k, v in dct_courses.items():
                for i in range(len(k)):
                    koef = levenshtein_distance(userReqqq.cleaned_data['search_engine'], k[i])
                    dct_courses[k] = koef

            


            # # Проверка результатов поиска и добавление соответствующих текстов в список lst
            # for k, v in dct_courses.items():
            #     if k[0] == "Frontend Development" and float(v) > 2.5:
            #         lst.append(dct_res_text[0])
            #     if k[0] == "Data Science" and float(v) > 2.5:
            #         lst.append(dct_res_text[1])
            #     if k[0] == "Backend Development" and float(v) > 2.5:
            #         lst.append(dct_res_text[2])
            #     if k[0] == "Цифровой маркетинг" and float(v) > 2.5:
            #         lst.append(dct_res_text[3])
            #     if k[0] == "Финансовый анализ" and float(v) > 2.5:
            #         lst.append(dct_res_text[4])
            #     if k[0] == "Blockchain и криптовалюты" and float(v) > 2.5:
            #         lst.append(dct_res_text[5])
            #     if k[0] == "UX/UI дизайн" and float(v) > 2.5:
            #         lst.append(dct_res_text[6])
            #     if k[0] == "IOS разработчик" and float(v) > 2.5:
            #         lst.append(dct_res_text[7])
            #     if k[0] == "SQL" and float(v) > 2.5:
            #         lst.append(dct_res_text[8])
            #     if k[0] == "Кибербезопасность" and float(v) > 2.5:
            #         lst.append(dct_res_text[9])               

            # Возвращение шаблона "search_results.html" с передачей списка lst и темы пользователя u_theme
            return render(request, "search_results.html", {"collection": lst, "u_theme": u_theme})

    # Возврат шаблона "search_results.html" без данных
    return render(request, "search_results.html")