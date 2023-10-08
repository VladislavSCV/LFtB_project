def catalog_courses(request, course):
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
    match course:
        case "Frontend":
            return render(request, r"all_courses/CFontend.html", context={"u_theme": u_theme})
        case "Цифровой_маркетинг":
            return render(request, r"all_courses/Cbc.html", context={"u_theme": u_theme})
        case "Финансовый_анализ":
            return render(request, r"all_courses/Cfa.html", context={"u_theme": u_theme})
        case "UX_UI_дизайн":
            return render(request, r"all_courses/CuxUi.html", context={"u_theme": u_theme}) 
        case "SQL_разработка":
            return render(request, r"all_courses/Csql.html", context={"u_theme": u_theme}) 


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



""" """ """ """ """ """ """ """ """ """ """ """ """ """  """ """ """ """ """ """ """ """ """ """ """ """ """ """



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