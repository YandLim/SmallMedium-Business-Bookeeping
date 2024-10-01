#This is the program with a touch of SQLite
import sqlite3
import time

Goods = dict()
Profit = int()
Sales_History = {}
sale_id = 1


def load_database_to_goods():
    global Goods
    try:
        conn = sqlite3.connect("D:\Coding\Python\BookKeeping\Bookeeping.db")
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
        return ""


def Updating_Database(Goods, Price, Quantity, Capital):
    conn = sqlite3.connect("D:\Coding\Python\BookKeeping\Bookeeping.db")
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


def updating_goods():
    global Goods
    try:
        while True:
            goods = (input("""\nWhat Goods do You want to update? Here is what you can do
            type goods's name for updating it
            type ok for end the updating
            type updating name for change good's name """)).lower()

            if goods == "ok":
                return ""

            elif goods == "updating name":
                while True:
                    goods = input("\nWhich Good's you want to change?(ok for end) ").lower()
                    if goods == "ok":
                        return''

                    elif goods in Goods:
                        new_name = input("What the new name for this goods? ")
                        Goods[new_name] = Goods.pop(goods)
                        print(f"{goods} succesfully change name to {new_name}")

                    else:
                        print(f"{goods} are nowhere to be found")

            elif goods not in Goods:
                try:
                    capital = int(input("\nEnter the capital of the Goods "))
                    price = int(input("Enter the price of the goods "))
                    quantity = int(input("Enter the quantity of the goods "))
                    Goods[goods] = [price, capital, quantity]

                    Goods = {k.lower(): v for k, v in Goods.items()}
                    Updating_Database(goods, price, quantity, capital)

                except ValueError:
                    print("Invalid input. Please enter numeric values for capital price and quantity.")

            else:
                capital = (input("\nEnter the capital of the Goods "))
                price = (input("Enter the price of the goods "))
                quantity = (input("Enter the quantity of the goods "))

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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def removing_goods_database(goods):
    conn = sqlite3.connect("D:\Coding\Python\BookKeeping\Bookeeping.db")
    cursor = conn.cursor()

    delete_quary = "DELETE FROM Goods_Data WHERE Goods = ?"
    cursor.execute(delete_quary, (goods,))

    conn.commit()
    conn.close()


def removing_goods():
    while True:
        goods = (input("\nWhat Goods do You want to remove? (type: ok for end the removal) ")).lower()
        if goods == "ok":
                return ""

        elif goods in Goods:
            del Goods[goods]
            removing_goods_database(goods)
            print(f"{goods} are succesfully removed")

        else:
            print(f"{goods} are not found")


def searching():
    while True:
        goods = (input("What are you looking for? (type: ok for end the search) ")).lower()
        if goods == "ok":
                return ""
    
        elif goods in Goods:
            print(f"\n{goods}: Price = {Goods[goods][0]}, Capital = {Goods[goods][1]}, Quantity = {Goods[goods][2]}\n")

        else:
            print(f"{goods} are nothing to found")


def load_sales_history_database():
    global Sales_History
    try:
        conn = sqlite3.connect("D:\Coding\Python\BookKeeping\Bookeeping.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Goods, Price, Quantity, Total_Price FROM Sale_History")
        rows = cursor.fetchall()

        Sales_History = {}
        for row in rows:
            goods_name = row[0] 
            price = row[1]
            quantity = row[2]  
            total_price = row[3]     

            Sales_History[goods_name.lower()] = [price, quantity, total_price]

        conn.close()
        return Sales_History
    except:
        return ""


def database_sale_history(Goods_Name, Price, Quantity, Total_Price, Time):
    global Goods
    conn = sqlite3.connect("D:\Coding\Python\BookKeeping\Bookeeping.db")
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


def sale():
    global sale_id
    global Profit
    while True:
        goods = input("\nWhat the name of product that sold?(type: ok for end the sale) ").lower()
        
        if goods == "ok":
                return ""

        elif goods in Goods:
            price = (input("Enter the price of the goods that sold "))
            quantity = (input("Enter the quantity of the goods that sold "))

            if price == "":
                price = Goods[goods][0]

            if quantity == "":
                quantity = 1

            if Goods[goods][2] < int(quantity):
                print(f"Not enough {goods} in stock to complete the sale.")
                continue

            total_price = int(price) * int(quantity)

            sales = [(goods, quantity, total_price)]
            
            reduced_quantity = Goods[goods][2] - int(quantity)
            Sales_History[sale_id] = (goods, time.strftime('%Y-%m-%d %H:%M:%S'), quantity, total_price)

            database_sale_history(goods, price, quantity, total_price, time.strftime('%Y-%m-%d %H:%M:%S'))
            sale_id += 1
            
            print(f"\n{sales}")
            print (f"{goods} quantity is reduced to {reduced_quantity}")
            
        else:
            print(f"couldn't find {goods}")


def main():
    load_database_to_goods()
    load_sales_history_database()
    while True:
        choice = input("""\nHi what would you do right now?\nhere is some choice for you to do:
        Updating Goods(type: 1)
        Removing Goods(type: 2)
        Searching for Goods"(type: 3)
        Sell Goods (type: 4)
        To stop the program (type : okk ) """).lower()

        if choice == "1":
            updating_goods()
        
        elif choice == "2":
            removing_goods()

        elif choice == "3":
            searching()

        elif choice == "4":
            sale()

        elif choice == "okk":
            break

        else:
            print("That isn't an option")

main()
