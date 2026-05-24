import sqlite3
from config import our_database

# создаем таблицу для продуктов
def new_database():
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
            barrier INTEGER, 
            message INTEGER DEFAULT 0 
        )
    """)

    con.commit()
    con.close()

"""
в таблице:
    1) уникальный id товара
    2) id пользователя
    3) ссылка на товар
    4) название товара
    5) цена на момент добавления товара
    6) последняя цена
    7) порог цены
    8) отправка сообщения
"""


def add_product(user_id, url, name, price, barrier):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("INSERT INTO products (user_id, url, name, first_price, last_price, barrier) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, url, name, price, barrier))

    con.commit()
    con.close()


def update_price(id, new_price, message):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("UPDATE products SET last_price=? message=? WHERE id=?",
                   (new_price, message, id))

    con.commit()
    con.close()


def delete_product(product_id, user_id):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("DELETE FROM products WHERE id=? AND user_id=?",
              (product_id, user_id))

    con.commit()
    con.close()


# товары конкретного пользователя
def users_products(user_id):
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("SELECT id, name, first_price, last_price, barrier FROM products WHERE user_id=?",
                   (user_id))
    users_prod = cursor.fetchall()

    con.close()
    return users_prod
    

# все товары из бд
def all_products():
    con = sqlite3.connect(our_database)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    con.close()
    return products

