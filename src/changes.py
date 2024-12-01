import os
import sqlite3


def create_connection(name):
    if os.path.exists('data_bases/' + str(name) + '.db'):
        os.remove('data_bases/' + str(name) + '.db')
        print(f"База данных '{'data_bases/' + str(name) + '.db'}' была удалена.")

    con = sqlite3.connect('data_bases/' + str(name) + '.db')
    con.execute(f'''CREATE TABLE IF NOT EXISTS 'Changes' (
    id          INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL
                        UNIQUE,
    action      INTEGER NOT NULL,
    pen_color   TEXT    NOT NULL,
    brush_color TEXT    NOT NULL,
    width       INTEGER NOT NULL,
    meta        TEXT
    )''')
    con.commit()
    return con, con.cursor()


def add_change_to_db(con, cur, ctool, config, meta):
    """""
     1: 'pen',
     2: 'erazer',
     3: 'spray',
     4: 'rectangle',
     5: 'ellipse'
     """
    cur.execute(f"""INSERT INTO 'Changes' (action, pen_color, brush_color, width, meta) VALUES (?, ?, ?, ?, ?)""",
                (ctool, str(config['pen_color'].getRgb()), str(config['brush_color'].getRgb()), config['width'], meta))

    con.commit()


def del_last_change(name):
    con = sqlite3.connect(name + '.db')
    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) FROM {name}')
    total = cur.fetchone()[0]

    cur.execute(f'DELETE FROM {name} WHERE id = ?', (total,))

    con.commit()
    # con.close()


def get_last_change():
    pass
