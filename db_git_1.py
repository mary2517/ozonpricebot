import sqlite3
from config import our_database

# создаем таблицу для продуктов
con = sqlite3.connect(our_database)
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER, 
        url TEXT, 
        name TEXT, 
        first_price REAL, 
        last_price REAL, 
        barrier REAL, 
        message INTEGER DEFAULT 0 
    )
""")

con.commit()
con.close()

"""
параметры в таблице:
    1) уникальный id товара
    2) id пользователя
    3) ссылка на товар
    4) название товара
    5) цена на момент добавления товара
    6) последняя цена
    7) порог цены (при достижении которого будет высылаться сообщение в боте)
    8) отправка сообщения (0 - нет, 1 - да)
"""

# добавить товар в таблицу
def add_product(user_id, url, name, first_price, last_price, barrier):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("INSERT INTO products (user_id, url, name, first_price, last_price, barrier) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, url, name, first_price, last_price, barrier))

    con.commit()
    con.close()

# обновить цену
def update_price(product_id, new_price):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("UPDATE products SET last_price=? WHERE id=?",
                   (new_price, product_id))

    con.commit()
    con.close()


# удаление продукта
def delete_product(id, user_id):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("DELETE FROM products WHERE id=? AND user_id=?",
              (id, user_id))

    con.commit()
    con.close()
