import tkinter
from tkinter import messagebox

def main_interface():
    from Main import load_database_to_goods

    def close_frame(current_frame, new_frame):
        current_frame.grid_forget()
        new_frame.grid(row=0, column=0, padx=20, pady=20)

    def stored_update_data(goods_name_entry, capital_entry, price_entry, quantity_entry):
        from Main import updating_goods

        load_database_to_goods()
        goods_name = goods_name_entry.get().lower()
        price = price_entry.get()
        capital = capital_entry.get()
        quantity = quantity_entry.get()

        if goods_name and price and capital and quantity:
            try:
                price = int(price)
                capital = int(capital)
                quantity = int(quantity)
                
                updating_goods(goods_name, capital, price, quantity)

                goods_name_entry.delete(0, "end")
                price_entry.delete(0, "end")
                capital_entry.delete(0, "end")
                quantity_entry.delete(0, "end")
            except ValueError:
                tkinter.messagebox.showwarning("Input Error", "Price, Capital, and Quantity must be valid numbers.")
        else:
            tkinter.messagebox.showwarning("Missing Data", "Please fill all fields before updating.")

    def stored_remove_func(removes_entry):
        from Main import removing_goods
        from Main import Goods

        removed_data = removes_entry.get().lower()
        load_database_to_goods()

        if removed_data:
            if removed_data in Goods:
                removing_goods(removed_data)

                removes_entry.delete(0, "end")
            
            else:
                tkinter.messagebox.showwarning("Not found", f"{removed_data} are not found inside the DataBase")

        else:
            tkinter.messagebox.showwarning("Missing Data", "Please fill all fields before updating.")

    def stored_sale_func(goods, price, quantity):
        from Main import sale
        from Main import database_sale_history
        from Main import Goods

        load_database_to_goods()
        goods_name = goods.get().lower()
        price_sale = price.get()
        sold_quantity = quantity.get()

        if goods_name:
            if goods_name in Goods:
                if price_sale == "":
                    price_sale = int(Goods[goods_name][0])

                if sold_quantity == "":
                    sold_quantity = int(1)

                if price_sale and sold_quantity:
                    if Goods[goods_name][2] < int(sold_quantity):
                        tkinter.messagebox.showwarning("Error", f"Not enough {goods_name} in stock to complete the sale.")
                        return ""

                    try:
                        price_sale = int(price_sale)
                        quantity_sale = int(sold_quantity)

                        sale(goods_name, price_sale, sold_quantity)

                        goods.delete(0, "end")
                        price.delete(0, "end")
                        quantity.delete(0, "end")

                    except ValueError:
                        tkinter.messagebox.showwarning("Input Error", "Price and Quantity must be valid numbers.")
                else:
                    tkinter.messagebox.showwarning("Missing Data", "Please fill all fields before updating.")
            else:
                tkinter.messagebox.showwarning("Not Found", f"{goods_name} are nowhere to be found in the DataBase")
        else:
            tkinter.messagebox.showwarning("Missing Data", "Please fill all fields before updating.")


    window = tkinter.Tk()
    window.title("Bookkeeping")

    frame = tkinter.Frame(window, bg="#282c34")
    frame.pack()


    #Main menu
    def main_menu_frame():
        main_frame = tkinter.LabelFrame(frame, padx=10, pady=10, bg="#282c34")
        main_frame.grid(row=0, column=0, padx=20, pady=20)

        title_frame =tkinter.LabelFrame(main_frame, padx=80, pady=20, bg="gray")
        title_frame.grid(row=0, column=0, columnspan=2, sticky="news")

        title = tkinter.Label(title_frame, padx=80, pady=20, text="Bookkeeping", bg="#282c34", font=("Arial Black", 25), fg="white")
        title.grid(row=0, column=0, columnspan=2)

        Update_Button = tkinter.Button(main_frame, text="Update", padx=50, pady=15, font=("Berlin Sans FB", 20), command=lambda: close_frame(main_frame, updating_function()))
        Update_Button.grid(row=1, column=0, sticky="news")

        Remove_Button = tkinter.Button(main_frame, text="Remove", padx=50, pady=15, font=("Berlin Sans FB", 20), command=lambda: close_frame(main_frame, removing_function()))
        Remove_Button.grid(row=1, column=1, sticky="news")

        Sale_Button = tkinter.Button(main_frame, text="Sale", padx=100, pady=15, font=("Berlin Sans FB", 20), command=lambda: close_frame(main_frame, sale_function()))
        Sale_Button.grid(row=2, column=0, columnspan=2, sticky="ns")

        for widget in main_frame.winfo_children():
            widget.grid_configure(padx=35, pady=25)

        return main_frame


    #execute updating function
    def updating_function():
        update_frame = tkinter.LabelFrame(frame, padx=10, pady=10, bg="#282c34")

        title = tkinter.Label(update_frame, padx=80, pady=20, text="Update", bg="#282c34", font=("Arial Black", 25), fg="white")
        title.grid(row=0, column=0, columnspan=2)

        goods_name_label = tkinter.Label(update_frame, text="Good's name", font=("Algerian", 20))
        goods_name_entry = tkinter.Entry(update_frame, font=("Arial Black", 15))
        goods_name_label.grid(row=1, column=0, sticky="news")
        goods_name_entry.grid(row=1, column=1, sticky="ns")
        goods_name_entry.bind('<Down>', lambda event: capital_entry.focus())

        capital_label = tkinter.Label(update_frame, text="Capital", font=("Algerian", 20))
        capital_entry = tkinter.Entry(update_frame, font=("Arial Black", 15))
        capital_label.grid(row=2, column=0, sticky="news")
        capital_entry.grid(row=2, column=1, sticky="ns")
        capital_entry.bind('<Up>', lambda event: goods_name_entry.focus())
        capital_entry.bind('<Down>', lambda event: price_entry.focus())


        price_label = tkinter.Label(update_frame, text="Price", font=("Algerian", 20))
        price_entry = tkinter.Entry(update_frame, font=("Arial Black", 15))
        price_label.grid(row=3, column=0, sticky="news")
        price_entry.grid(row=3, column=1, sticky="ns")
        price_entry.bind('<Up>', lambda event: capital_entry.focus())
        price_entry.bind('<Down>', lambda event: quantity_entry.focus())


        quantity_label = tkinter.Label(update_frame, text="Quantity", font=("Algerian", 20))
        quantity_entry = tkinter.Entry(update_frame, font=("Arial Black", 15))
        quantity_label.grid(row=4, column=0, sticky="news")
        quantity_entry.grid(row=4, column=1, sticky="ns")
        quantity_entry.bind('<Up>', lambda event: price_entry.focus())
        
        for widget in update_frame.winfo_children():
            widget.grid_configure(padx=25, pady=15)
            widget.bind('<Return>', lambda event: Ok_Button.invoke())


        back_Button = tkinter.Button(update_frame, text="Back", font=("Copper Black", 20), bg="#28282B", command=lambda: close_frame(update_frame, main_menu_frame()))
        back_Button.grid(row=5, column=0, padx=25, pady=25, sticky="ews")

        Ok_Button = tkinter.Button(update_frame, text="OK", font=("Copper Black", 20), bg="#28282B", command=lambda: stored_update_data(goods_name_entry, capital_entry, price_entry, quantity_entry))
        Ok_Button.grid(row=5, column=1, padx=25, pady=25, sticky="ews")

        return update_frame


    #execute remove function
    def removing_function():
        #make new frame for remove function
        remove_frame = tkinter.LabelFrame(frame, padx=10, pady=10, bg="#282c34")
        remove_frame.grid(row=0, column=0, padx=20, pady=20)

        #Making title vertically
        title_R = tkinter.Label(remove_frame, text="R", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_R.grid(row=0, column=0)

        title_Edown = tkinter.Label(remove_frame, text="E", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Edown.grid(row=1, column=0)

        title_Mdown = tkinter.Label(remove_frame, text="M", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Mdown.grid(row=2, column=0)

        title_Odown = tkinter.Label(remove_frame, text="O", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Odown.grid(row=3, column=0)

        title_Vdown = tkinter.Label(remove_frame, text="V", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Vdown.grid(row=4, column=0)

        title_Edown = tkinter.Label(remove_frame, text="E", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Edown.grid(row=5, column=0)

        title_Sdown = tkinter.Label(remove_frame, text="S", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Sdown.grid(row=6, column=0)
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------
        #making title vertically
        title_Efront = tkinter.Label(remove_frame, text="E", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Efront.grid(row=0, column=1)

        title_Mfront = tkinter.Label(remove_frame, text="M", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Mfront.grid(row=0, column=2)

        title_Ofront = tkinter.Label(remove_frame, text="O", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Ofront.grid(row=0, column=3)

        title_Vfront = tkinter.Label(remove_frame, text="V", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Vfront.grid(row=0, column=4)

        title_Efront = tkinter.Label(remove_frame, text="E", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Efront.grid(row=0, column=5)

        title_Sfront = tkinter.Label(remove_frame, text="S", bg="#282c34", font=("Engravers MT", 25), fg="white")
        title_Sfront.grid(row=0, column=6)

        #Configure distancing
        for widget in remove_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        removes_entry = tkinter.Entry(remove_frame, font=("Arial Black", 15))
        removes_entry.grid(row=3, column=2, columnspan=4, rowspan=2, ipady=10)
        removes_entry.bind('<Return>', lambda event: enter_Button.invoke())

        back_Button = tkinter.Button(remove_frame, padx=50, text="Back", font=("Copper Black", 20), bg="#28282B", command=lambda: close_frame(remove_frame, main_menu_frame()))
        back_Button.grid(row=1, rowspan=2, column=2, columnspan=4)

        enter_Button = tkinter.Button(remove_frame, padx=50, text="Enter", font=("Copper Black", 20), bg="#28282B", command=lambda: stored_remove_func(removes_entry))
        enter_Button.grid(row=5, rowspan=2, column=2, columnspan=4)

        return remove_frame


    #execute sale function
    def sale_function():
        sale_frame = tkinter.LabelFrame(frame, padx=10, pady=10, bg="#282c34")

        title = tkinter.Label(sale_frame, text="SALE", bg="#282c34", font=("Arial Black", 25), fg="white")
        title.grid(row=0, column=0, columnspan=2)

        sale_goods_label = tkinter.Label(sale_frame, text="Good's name", font=("Algerian", 15), bg="gray", fg="white")
        sale_goods_entry = tkinter.Entry(sale_frame, font=("Arial Black", 10))
        sale_goods_label.grid(row=1, column=0, sticky="news")
        sale_goods_entry.grid(row=1, column=1, sticky="ns")
        sale_goods_entry.bind('<Down>', lambda event: price_goods_entry.focus())

        price_goods_label = tkinter.Label(sale_frame, text="Price", font=("Algerian", 15), bg="gray", fg="white")
        price_goods_entry = tkinter.Entry(sale_frame, font=("Arial Black", 10))
        price_goods_label.grid(row=2, column=1, sticky="news")
        price_goods_entry.grid(row=2, column=0, sticky="ns")
        price_goods_entry.bind('<Up>', lambda event: sale_goods_entry.focus())
        price_goods_entry.bind('<Down>', lambda event: quantity_goods_entry.focus())

        quantity_goods_label = tkinter.Label(sale_frame, text="Quantity", font=("Algerian", 15), bg="gray", fg="white")
        quantity_goods_entry = tkinter.Entry(sale_frame, font=("Arial Black", 10))
        quantity_goods_label.grid(row=3, column=0, sticky="news")
        quantity_goods_entry.grid(row=3, column=1, sticky="ns")
        quantity_goods_entry.bind('<Up>', lambda event: price_goods_entry.focus())

        for widget in sale_frame.winfo_children():
            widget.grid_configure(padx=25, pady=15)
            widget.bind('<Return>', lambda event: Ok_Button.invoke())

        back_Button = tkinter.Button(sale_frame, text="Back", padx= 25, font=("Copper Black", 20), bg="#28282B", command=lambda: close_frame(sale_frame, main_menu_frame()))
        back_Button.grid(row=0, column=3, rowspan=2, columnspan=2, padx=25, pady=50, sticky="news")

        Ok_Button = tkinter.Button(sale_frame, text="OK", padx= 25, font=("Copper Black", 20), bg="#28282B", command=lambda: stored_sale_func(sale_goods_entry, price_goods_entry, quantity_goods_entry))
        Ok_Button.grid(row=2, column=3, rowspan=2, columnspan=2, padx=25, pady=50, sticky="news")

        return sale_frame

    main_menu_frame()
    window.mainloop()
