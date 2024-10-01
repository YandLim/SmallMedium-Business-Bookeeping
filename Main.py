#This is the program with a touch of SQLite
import sqlite3
import time
from Bookeeping_Interface import main_interface

Goods = dict()

def load_database_to_goods():
    try:
        global Goods
        conn = sqlite3.connect("Bookeeping.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Goods, Price, Quantity, Capital FROM Goods_Data")
        rows = cursor.fetchall()

        Goods = {}
        for row in rows:
            goods_name = row[0] 
            price = row[1]
            quantity = row[2]  
            capital = row[3]     

            Goods[goods_name.lower()] = [price, capital, quantity]

        conn.close()
        return Goods

    except:
        pass


def Updating_Database(Goods, Price, Quantity, Capital):
    conn = sqlite3.connect("Bookeeping.db")
    Goods_Tabble_Query = '''CREATE TABLE IF NOT EXISTS Goods_Data
            (Goods TEXT, Price INT, Quantity INT, Capital INT)
    '''
    conn.execute(Goods_Tabble_Query)
    cursor = conn.cursor()

    cursor.execute("SELECT Price, Quantity, Capital FROM Goods_Data WHERE Goods = ?", (Goods,))
    existing_record = cursor.fetchone()

    if existing_record:
        update_query = '''UPDATE Goods_Data 
                          SET Price = ?, Quantity = ?, Capital = ?
                          WHERE Goods = ?'''
        cursor.execute(update_query, (Price, Quantity, Capital, Goods))

    else:
        Goods_query = '''INSERT INTO Goods_Data (Goods, Price, Quantity, Capital) VALUES
        (?, ?, ?, ?)'''
        Goods_insert_query = (Goods, Price, Quantity, Capital)
        cursor.execute(Goods_query, Goods_insert_query)

    conn.commit()
    conn.close()


def updating_goods(goods, capital, price, quantity):
    global Goods
    if goods not in Goods:
        try:
            Goods[goods] = [price, capital, quantity]

            Goods = {k.lower(): v for k, v in Goods.items()}
            Updating_Database(goods, price, quantity, capital)

        except ValueError:
            print("Invalid input. Please enter numeric values for capital price and quantity.")

    else:
        if price == "":
            price = Goods[goods][0]

        if capital == "":
            capital = Goods[goods][1]

        if quantity == "":
            quantity = Goods[goods][2]

        Goods[goods][0] = int(price)
        Goods[goods][1] = int(capital)
        Goods[goods][2] = int(quantity)

        Goods = {k.lower(): v for k, v in Goods.items()}                
        Updating_Database(goods, Goods[goods][0], Goods[goods][2], Goods[goods][1])


def removing_goods_database(good):
    conn = sqlite3.connect("Bookeeping.db")
    cursor = conn.cursor()

    delete_quary = "DELETE FROM Goods_Data WHERE Goods = ?"
    cursor.execute(delete_quary, (good,))

    conn.commit()
    conn.close()


def removing_goods(good):
        del Goods[good]
        removing_goods_database(good)


def database_sale_history(Goods_Name, Price, Quantity, Total_Price, Time):
    global Goods
    conn = sqlite3.connect("Bookeeping.db")
    Sale_Tabble_Quary = '''CREATE TABLE IF NOT EXISTS Sale_History
            (Goods TEXT, Price REAL, Quantity INT, Total_Price REAL, Time REAL)
    '''

    conn.execute(Sale_Tabble_Quary)
    cursor = conn.cursor()
    Goods_query = '''INSERT INTO Sale_History (Goods, Price, Quantity, Total_Price, Time) VALUES
    (?, ?, ?, ?, ?)'''

    Goods_insert_query = (Goods_Name, Price, Quantity, Total_Price, Time)
    cursor.execute(Goods_query, Goods_insert_query)

    cursor.execute("SELECT Price, Quantity, Capital FROM Goods_Data WHERE Goods = ?", (Goods_Name,))
    existing_record = cursor.fetchone()

    Goods[Goods_Name][2] -= int(Quantity)

    update_goods_query = '''UPDATE Goods_Data 
                        SET Quantity = ?
                        WHERE Goods = ?'''
    cursor.execute(update_goods_query, (Goods[Goods_Name][2], Goods_Name))

    conn.commit()
    conn.close()


def sale(goods, price, quantity):
    global Goods
    total_price = int(price) * int(quantity)
    
    reduced_quantity = Goods[goods][2] - int(quantity)
    database_sale_history(goods, price, quantity, total_price, time.strftime('%Y-%m-%d %H:%M:%S'))
                

main_interface()