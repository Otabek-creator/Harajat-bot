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


def create_user(ism, familya ,ph_number, chat_id):
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO users (ism, familya, ph_number, chat_id) VALUES ('{ism}', '{familya.replace("'", "`")}', '{ph_number}', '{chat_id}');"""
        )


def update_user(result, chat_id):
    conn = connect_to_db()
    print(result, chat_id)
    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE users SET result = '{result}' WHERE chat_id = '{chat_id}';"
        )

    close_db(conn)


def delete_user(chat_id):
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM users WHERE chat_id = '{chat_id}';"
        )

    close_db(conn)

def get_user_by_id(chat_id):
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM users WHERE chat_id = '{chat_id}';"
        )
        result = cur.fetchone()

    close_db(conn)
    return result




def get_result():
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM users "
        )
        result = cur.fetchall()

    close_db(conn)
    return result

def close_db(conn):
    if conn:
        conn.close()
