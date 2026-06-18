import sqlite3

from dotenv import load_dotenv
import os
load_dotenv()
DB_PATH = os.getenv("DB_PATH")

# Устанавливаем соединение с базой данных
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
# Создаем таблицу users и todos
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
tg_user_id BIGINT NOT NULL UNIQUE,
username TEXT,
status TEXT DEFAULT "active"
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL ,
text TEXT NOT NULL,
done_is BOOLEAN NOT NULL DEFAULT FALSE,
deadline TIMESTAMP,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
)
''')
# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

def check_user(tg_user_id) -> int: #if exist int else None
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(''' SELECT id FROM users WHERE tg_user_id = ? LIMIT 1''', (tg_user_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None: return 0
    else: return row[0]


def count_tasks(tg_user_id, status = False) -> int:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    db_id = check_user(tg_user_id)
    cursor.execute(''' SELECT COUNT(*) FROM todos WHERE user_id = ? AND done_is = ?''', (db_id, status))
    row = cursor.fetchone()
    connection.close()
    if row is None: return 0
    else: return row[0]


def addUserDB(name, tg_user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)
    if db_id == 0:
        cursor.execute('''
        INSERT INTO users (username, tg_user_id)
        VALUES (?, ?)
        ''', (name, tg_user_id))

    connection.commit()
    connection.close()


def addTodoDB(texttodo, tg_user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)

    cursor.execute('''
    INSERT INTO todos (user_id, text)
    VALUES (?,?)
    ''', (db_id, texttodo))

    connection.commit()
    connection.close()


def showTodoDB(tg_user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)

    cursor.execute('''
    SELECT text FROM todos
    WHERE user_id = ? AND done_is = FALSE
    ORDER BY created_at
    ''', (db_id,))

    rows = cursor.fetchall()
    ct = len(rows)
    output = ""
    for i in range (0, ct):
        output += "📌 " + rows[i][0] + "\n\n"

    connection.commit()
    connection.close()

    return output


def showNumberTodoDB(tg_user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)

    cursor.execute('''
    SELECT text FROM todos
    WHERE user_id = ? AND done_is = FALSE
    ORDER BY created_at
    ''', (db_id,))

    rows = cursor.fetchall()
    ct = len(rows)
    output = ""
    for i in range (0, ct):
        task = rows[i][0]
        if len(task) > 53: task = task[:51] + "..."
        output += str(i+1) + ". " + task + "\n"

    connection.commit()
    connection.close()

    return output


def editTodoDB(tg_user_id, numtask, newtext):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)

    cursor.execute('''
    SELECT id FROM todos 
    WHERE user_id = ? AND done_is = FALSE
    ORDER BY created_at
    LIMIT 1 OFFSET ?
    ''', (db_id, numtask-1))

    idtask = cursor.fetchone()[0]

    cursor.execute('''
    UPDATE todos
    SET text = ?
    WHERE id = ?
    ''', (newtext, idtask))

    connection.commit()
    connection.close()


def deleteTodoDB(tg_user_id, numtask) -> int:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)

    cursor.execute('''
    SELECT id FROM todos 
    WHERE user_id = ? AND done_is = FALSE
    ORDER BY created_at
    LIMIT 1 OFFSET ?
    ''', (db_id, numtask-1))

    idtask = cursor.fetchone()[0]

    cursor.execute('''
    UPDATE todos
    SET done_is = TRUE
    WHERE id = ?
    ''', (idtask,))

    connection.commit()
    connection.close()

    return idtask


def cancelDeleteTodoDB(tg_user_id, idtask):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    db_id = check_user(tg_user_id)

    cursor.execute('''
    UPDATE todos
    SET done_is = FALSE
    WHERE id = ?
    ''', (idtask,))

    connection.commit()
    connection.close()