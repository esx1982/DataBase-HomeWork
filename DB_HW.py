import psycopg2

# установка соединения с базой данных:
conn = psycopg2.connect(database="home_work_base", user="postgres", password="XInazkRgqj1982")

# для отправки запросов в БД необходим КУРСОР. Его необходимо запросить у соединения:
# первый вариант:
# cur = conn.cursor()
# КУРСОР тоже необходимо закрывать:
# cur.execute("")
#...тело запроса...
# cur.close()
# либо пользоваться контекстным менеджером with:
with conn.cursor() as cur:
    cur.execute("CREATE TABLE ... (id SERIAL PRIMIRY KEY);")
# для отправки запроса в БД необходимо сделать "commit":
    cur.commit()
# если мы не хотим отпрвлять запроосы в БД, необходимо воспользоваться функцией rollback:
    cur.rollback() # все запросы будут проигнорированы...
#соединение необходимо ВСЕГДА закрывать!
conn.close()