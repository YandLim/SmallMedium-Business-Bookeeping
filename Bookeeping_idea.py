#This is the main idea and main function of this program
import time

Goods = dict()
Profit = int()
Sales_History = {}
sale_id = 1

def updating_goods():
    global Goods
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

            except ValueError:
                print("Invalid input. Please enter numeric values for capital price and quantity.")

        else:
            capital = int(input("\nEnter the capital of the Goods "))
            price = int(input("Enter the price of the goods "))
            quantity = int(input("Enter the quantity of the goods "))
            Goods[goods][0] += int(price)
            Goods[goods][1] += int(capital)
            Goods[goods][2] += int(quantity)
        
        Goods = {k.lower(): v for k, v in Goods.items()}
        print(f"\n{goods} has been updated to \n{Goods}")

def removing_goods():
    while True:
        goods = (input("\nWhat Goods do You want to remove? (type: ok for end the removal) ")).lower()
        if goods == "ok":
                return ""

        elif goods in Goods:
            del Goods[goods]
            print(f"{goods} are succesfully removed")

        else:
            print(f"{goods} are not found")

def searching():
    while True:
        goods = (input("\nWhat are you looking for? (type: ok for end the search) ")).lower()
        if goods == "ok":
                return ""
    
        elif goods in Goods:
            print(f"\n{goods}: Price = {Goods[goods][0]}, Capital = {Goods[goods][1]}, Quantity = {Goods[goods][2]}\n")

        else:
            print(f"{goods} are nothing to found")

def sale():
    global sale_id
    global Profit
    while True:
        goods = input("\nWhat the name of product that sold?(type: ok for end the sale) ")
        
        if goods == "ok":
                return ""

        elif goods in Goods:
            price = (input("Enter the price of the goods that sold "))
            quantity = (input("Enter the quantity of the goods that sold "))

            if Goods[goods][2] < int(quantity):
                print(f"Not enough {goods} in stock to complete the sale.")

            if price == "":
                price = Goods[goods][0]

            if quantity == "":
                quantity = 1

            total_price = price * quantity

            sales = [(goods, total_price, quantity)]
            Goods[goods][2] -= int(quantity)
            Sales_History[sale_id] = (goods, time.strftime('%Y-%m-%d %H:%M:%S'), quantity, total_price)
                
            Profit += (int(price) - Goods[goods][1]) * quantity
            sale_id += 1
            print(f"\n{sales}")
            print (f"{goods} quantity is reduced to {Goods[goods][2]}")
            
        else:
            print(f"couldn't find {goods}")

def sales_history():
    print("\n Sales History:")
    for key, value in Sales_History.items():
        goods, time, quantity, total_price = value
        print(f"  Sale ID {key}:")
        print(f"  Product: {goods}")
        print(f"  Date: {time}")
        print(f"  Quantity Sold: {quantity}")
        print(f"  Total Price: Rp{total_price:.2f}")
        print("------------------------------")
    return""

def profit():
    print(f"Your Total profit is Rp{Profit:.2f}")


def main():
    while True:
        choice = input("""\nHi what would you do right now?\nhere is some choice for you to do:
        Updating Goods(type: updating goods)
        Removing Goods(type: removing goods)
        Searching for Goods"(type: search)
        Selled Goods (type: Sale)
        Looking for sales history (type: sales history)
        Looking for the total Profit (type: profit)
        To stop the program (type : okk ) """).lower()

        if choice == "updating goods":
            updating_goods()
        
        elif choice == "removing goods":
            removing_goods()

        elif choice == "search":
            searching()

        elif choice == "sale":
            sale()

        elif choice == "sales history":
            sales_history()

        elif choice == "profit":
            profit()

        elif choice == "okk":
            break

        else:
            print("That isn't an option")

main()