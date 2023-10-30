import psycopg2

conn = psycopg2.connect(database="clientsDB", user="postgres", password="XInazkRgqj1982")

def createTables(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE client_email;
                DROP TABLE email;
                DROP TABLE client_phone;
                DROP TABLE phone;
                DROP TABLE client;
                """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            fist_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(60) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS email(
            id SERIAL PRIMARY KEY,
            email VARCHAR(100) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_email(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES client(id),
            email_id INTEGER NOT NULL REFERENCES email(id)
        );
        """)
    # формат E.164, максимум 15 цифр и обычно записываются с префиксом «+»
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            phone_no VARCHAR(15)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_phone(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES client(id),
            phone_id INTEGER NOT NULL REFERENCES phone(id)
        );
        """)
        conn.commit()
    conn.close()

def add_client(conn, fist_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        sql1 = "SELECT id, fist_name, last_name FROM client WHERE fist_name = %s AND last_name = %s"
        cur.execute(sql1, (fist_name, last_name))
        result = cur.fetchall()
        print(result)
        if len(result) == 0:
            sql = "INSERT INTO client(fist_name, last_name) VALUES(%s, %s)"
            cur.execute(sql, (fist_name, last_name))
            sql = "INSERT INTO phone(phone_no) VALUES(%s)"
            cur.execute(sql, (phone,))
            sql = "INSERT INTO email(email) VALUES(%s)"
            cur.execute(sql, (email,))
            sql = "INSERT INTO client_phone(client_id, phone_id) VALUES((SELECT MAX(id) FROM client), (SELECT MAX(id) FROM phone))"
            cur.execute(sql, (fist_name, phone))
            sql = "INSERT INTO client_email(client_id, email_id) VALUES((SELECT MAX(id) FROM client), (SELECT MAX(id) FROM email))"
            cur.execute(sql, (fist_name, email))
            conn.commit()
            print((f'имя {fist_name} и фамилия {last_name} в базе отсутствуют, добавляем!'))
        else:
            print((f'имя {fist_name} и фамилия {last_name} есть в базе!'))

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        sql1 = "SELECT id FROM client WHERE id = %s"
        cur.execute(sql1, (client_id,))
        result = cur.fetchall()
        print(result)
        if len(result) != 0:
            sql = "UPDATE phone SET phone_no = %s WHERE id = %s"
            cur.execute(sql, (phone, client_id))
            conn.commit()
            print(f'Клиенту {client_id} присвоен номер телефона {phone}')
        else:
            print(f'Клиента с таким ID- "{client_id}" нет, попробуйте еще раз!')

def change_client(conn, client_id, fist_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        sql1 = "SELECT id FROM client WHERE id = %s"
        cur.execute(sql1, (client_id,))
        result = cur.fetchall()
        print(result)
        if len(result) != 0:
            sql = "UPDATE client SET fist_name = %s, last_name = %s WHERE id = %s"
            cur.execute(sql, (fist_name, last_name, client_id))
            sql = "UPDATE email SET email = %s WHERE id = %s"
            cur.execute(sql, (email, client_id))
            sql = "UPDATE phone SET phone_no = %s WHERE id = %s"
            cur.execute(sql, (phone, client_id))
            conn.commit()
            print(f'Обновление данных клиенту - "{client_id}" прошло успешно!')
        else:
            print(f'Клиента с таким ID- "{client_id}" нет, попробуйте еще раз!')

def del_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        sql1 = "SELECT id FROM client WHERE id = %s"
        cur.execute(sql1, (client_id,))
        result = cur.fetchall()
        print(result)
        if len(result) != 0:
            sql = "UPDATE phone SET phone_no = %s WHERE id = %s"
            cur.execute(sql, ('Null', client_id))
            conn.commit()
            print(f'Удаление телефона клиенту - "{client_id}" прошло успешно!')
        else:
            print(f'Клиента с таким ID- "{client_id}" нет, попробуйте еще раз!')

def del_client(conn, client_id):
    with conn.cursor() as cur:
        sql1 = "SELECT id FROM client WHERE id = %s"
        cur.execute(sql1, (client_id,))
        result = cur.fetchall()
        print(result)
        if len(result) != 0:
            sql = "DELETE FROM client_phone WHERE id = %s"
            cur.execute(sql, (client_id,))
            sql = "DELETE FROM client_email WHERE id = %s"
            cur.execute(sql, (client_id,))
            sql = "DELETE FROM phone WHERE id = %s"
            cur.execute(sql, (client_id, ))
            sql = "DELETE FROM email WHERE id = %s"
            cur.execute(sql, (client_id,))
            sql = "DELETE FROM client WHERE id = %s"
            cur.execute(sql, (client_id,))
            conn.commit()
            print(f'Удаление клиента - "{client_id}" прошло успешно!')
        else:
            print(f'Клиента с таким ID- "{client_id}" нет, попробуйте еще раз!')

def find_client(conn, fist_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        sql1 = ("SELECT * FROM client AS c "
                "JOIN phone AS p ON c.id = p.id "
                "JOIN email AS e ON c.id = e.id "
                "WHERE c.fist_name=%s OR c.last_name=%s OR e.email=%s OR p.phone_no=%s")
        cur.execute(sql1, (fist_name, last_name, email, phone))
        result = cur.fetchall()
        print(result)

# createTables(conn)
# add_client(conn, "Евгений", "Михайлов", "ev@mail.ru", "+79241221540")
# add_client(conn, "Владимир", "Ухов", "vu@gmail.com", "+79241221570")
# add_client(conn, "Дмитрий", "Руков", "dr@gmail.com", )
# add_phone(conn, "3", "+79147115548")
# change_client(conn, "2", "Vladimir", "Uhov", "uhov_v@mail.ru", "+7-908-998-1622")
# del_phone(conn, "3", "Null")
# del_client(conn, "3")
find_client(conn, "Евгений")
conn.close()