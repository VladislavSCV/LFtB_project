import psycopg2


def take_xp(userNameSession):
    # ...Вывод сертефикатов пользователя
    conn = psycopg2.connect(dbname="LFtB", user="postgres",
                            password="31415926", host="127.0.0.1")
    cursor = conn.cursor()

    cursor.execute("""SELECT user_certific FROM users WHERE user_name = %s""", (userNameSession, ))
    conn.commit()

    user_certific = cursor.fetchone()[0]

    if user_certific:
        user_certific = eval(user_certific)
        
    else:
        user_certific = {}
    print(".............", user_certific)

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

    # num = 1
    # if len(user_certific) == 1 and num == 1:
    #     user_achievments.add("Начало путешествия!")
    #     xp+=400
    #     num += 1
    # if len(user_certific) == 3 and num == 2:
    #     user_achievments.add("Рыцарь знаний")
    #     xp+=300
    #     num += 1
    # if len(user_certific) == 5 and num == 3:
    #     user_achievments.add("Гений инноваций")
    #     xp+=500
    #     num += 1
    # if len(user_certific) == 8 and num == 4:
    #     user_achievments.add("Покоритель предметов")
    #     xp+=800
    #     num += 1

    # Преобразование данных перед вставкой в html
    user_achievments = str(user_achievments)

    cursor.execute(
        """UPDATE users SET user_achiv = %s 
        WHERE user_name = %s""", (user_achievments, userNameSession))

    conn.commit()

    cursor.close()
    conn.close()

print(take_xp("qwerty"))