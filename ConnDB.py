import sqlite3

class Connect():
    connection = sqlite3.connect("shop_produt.db")
    cursor = connection.cursor()

ConnectionDB = Connect