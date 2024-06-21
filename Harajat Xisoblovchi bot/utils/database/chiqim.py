import psycopg2


def connect_to_db():
    conn = psycopg2.connect(
        host='localhost',
        database='for_bot',
        user='postgres',
        password='1',
        port=5432
    )

    conn.autocommit = True

    return conn


def close_db(conn):
    if conn:
        conn.close()


def add_user(chiqim, sabab, chat_id):
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute(
    f"""INSERT INTO chiqim (chiqim, sabab, chat_id) VALUES ('{chiqim}', '{sabab}', '{chat_id}');"""
        )


def get_user(chat_id):
    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM chiqim WHERE chat_id = %s;", (chat_id,))
        user = cur.fetchall()

        return user



def get_subscribers():
    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM chiqim')

        result = cur.fetchall()
        close_db(conn)

    return result
