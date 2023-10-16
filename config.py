import sqlite3

connect = sqlite3.connect('bd.db', check_same_thread=False)
cursor = connect.cursor()

def registr(tg_id):
    cursor.execute('''
            INSERT INTO "users" (tg_id) 
            VALUES (?, ?)''', (tg_id))
    connect.commit()

def check(tg_id):
    return cursor.execute('''
        SELECT tg_id 
        FROM "users" 
        WHERE tg_id = ?''', (tg_id,)).fetchone()


resull = cursor.execute('''
CREATE TABLE IF NOT EXISTS
"users"
("id" INTEGER NOT NULL,
"tg_id" INTEGER NOT NULL,
primary key("id" AUTOINCREMENT)
)''')

resull = cursor.execute('''
CREATE TABLE IF NOT EXISTS
"categories"
("id" INTEGER NOT NULL,
"name" TEXT NOT NULL,
primary key("id" AUTOINCREMENT)
)''')

resull = cursor.execute('''
CREATE TABLE IF NOT EXISTS
"subscribes"
("id_user" INTEGER NOT NULL,
"id_category" INTEGER NOT NULL,
FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (id_category) REFERENCES categories(id) ON DELETE CASCADE
)''')

connect.commit()
# cursor.execute('''INSERT INTO categories (name) VALUES("sports")''')
# cursor.execute('''INSERT INTO categories (name) VALUES("business")''')
# cursor.execute('''INSERT INTO categories (name) VALUES("entertainment")''')
# cursor.execute('''INSERT INTO categories (name) VALUES("general")''')
# cursor.execute('''INSERT INTO categories (name) VALUES("health")''')
# cursor.execute('''INSERT INTO categories (name) VALUES("science")''')
# cursor.execute('''INSERT INTO categories (name) VALUES("technology")''')
# connect.commit()

cursor.close()


