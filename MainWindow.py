from ConnDB import ConnectionDB
from tkinter import *
from tkinter import Canvas
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning

class Window:
    def __init__(self):
        self.main_win = Tk()
        self.main_win.iconbitmap('shop_icon.ico')
        self.main_win.title("Интернет магазин продуктов")
        self.main_win.resizable(False, False)

        self.main_win.attributes("-fullscreen", True)

        fon_product = PhotoImage(file='product.png')
        icon_logo = PhotoImage(file='icon_logo.png')

        def win_сatalog():
            self.win_Catalog = Toplevel()
            self.win_Catalog.title("Каталог")
            self.win_Catalog.iconbitmap("catalog_icon.ico")
            self.win_Catalog.geometry("600x350+10+30")

            self.win_Catalog.wm_attributes("-topmost", 1)

            colums_catalog = ("name_product", "price", "weight")

            global Entry_info

            self.Entry_info = ttk.Entry(master=self.win_Catalog, width=60)
            self.Entry_info.place(x=0, y=4)

            global tree_Catalog
            self.tree_Catalog = ttk.Treeview(master=self.win_Catalog, columns=colums_catalog, show="headings", height=30)
            self.tree_Catalog.place(x=0, y=33)
            self.tree_Catalog.heading("name_product", text="Продукт")
            self.tree_Catalog.heading("price", text="Цена")
            self.tree_Catalog.heading("weight", text="Вес(гр/мл)")
            def Product_info():
                self.tree_Catalog.delete(*self.tree_Catalog.get_children())
                self.calltabCatalog = self.Entry_info.get()
                self.work_obj = ConnectionDB.cursor.execute(f'''SELECT name_product, price, weight FROM Product WHERE Product.name_product LIKE('%{self.calltabCatalog}%') GROUP BY name_product, price, weight''').fetchall()
                for prod in self.work_obj:
                    self.tree_Catalog.insert("", END, values=prod)
            Product_info()
            FindButton_table = ttk.Button(master=self.win_Catalog, text="Поиск", command=Product_info)
            FindButton_table.place(x=370, y=2)
            def add_new_tabl():
                try:
                    quantity_product = ConnectionDB.cursor.execute(f"SELECT name_product FROM Orders WHERE name_product = '{self.Entry_info.get()}'").fetchall()[0][0]
                    if quantity_product == self.Entry_info.get():
                        select_quantity = ConnectionDB.cursor.execute(f"SELECT quantity FROM Orders WHERE name_product = '{self.Entry_info.get()}'").fetchall()[0][0]+1
                        ConnectionDB.cursor.execute(f"UPDATE Orders SET quantity = '{select_quantity}' WHERE name_product = '{self.Entry_info.get()}'")
                    else:
                        pass
                except:
                    try:
                        self.take_info = ConnectionDB.cursor.execute(
                            f"SELECT * FROM Product WHERE Product.name_product='{self.Entry_info.get()}'").fetchall()
                        ConnectionDB.cursor.execute(
                            f'''INSERT INTO Orders (name_product, price, id_supplier, id_product, weight, quantity) VALUES ('{self.take_info[0][1]}','{self.take_info[0][2]}','{self.take_info[0][3]}','{self.take_info[0][0]}','{self.take_info[0][4]}',1)''')
                    except:
                        showerror(title="Ошибка", message="Данный товар отсуствует на складе")
            AddButton_busket = ttk.Button(master=self.win_Catalog, text="Добавить в корзину", command=add_new_tabl)
            AddButton_busket.place(x=450, y=2)

            self.win_Catalog.mainloop()
        def win_basket():
            self.win_Basket = Toplevel()
            self.win_Basket.title("Корзина")
            self.win_Basket.geometry("800x350")
            self.win_Basket.iconbitmap("icon_basket.ico")

            self.win_Basket.wm_attributes("-topmost", 1)

            global Del_product

            self.Del_product = ttk.Entry(master=self.win_Basket, width=40)
            self.Del_product.place(x=0, y=4)

            colums_busket = ("name_product", "price", "weight", "quantity")

            global tree_busket
            self.tree_busket = ttk.Treeview(master=self.win_Basket, columns=colums_busket, show="headings", height=40)
            self.tree_busket.place(x=0, y=30)

            self.tree_busket.heading("name_product", text="Продукт")
            self.tree_busket.heading("price", text="Цена")
            self.tree_busket.heading("weight", text="Вес(гр/мл)")
            self.tree_busket.heading("quantity", text="Количество")
            def take_product():
                self.tree_busket.delete(*self.tree_busket.get_children())
                self.show_info = ConnectionDB.cursor.execute('''SELECT name_product, price, weight, quantity FROM Orders''').fetchall()
                for prod in self.show_info:
                    self.tree_busket.insert("", END, values=prod)
            take_product()

            def del_info():
                try:
                    self.delete_info = ConnectionDB.cursor.execute(f"DELETE FROM Orders WHERE Orders.name_product = '{self.Del_product.get()}'")
                    take_product()
                except:
                    showerror(title="Ошибка", message="Такого товара нет в корзине")
            btn_delete = ttk.Button(master=self.win_Basket, text="Удалить из корзины", command=del_info)
            btn_delete.place(x=250, y=3)

            def buy_product_all():
                try:
                    show = ConnectionDB.cursor.execute('''SELECT * FROM Orders''').fetchall()[0][0]
                    ConnectionDB.cursor.execute("DELETE FROM Orders")
                    take_product()
                    self.win_Basket.destroy()
                    showinfo(title="Информация", message="Товар приобретён")
                except:
                    showwarning(title="Предупрждение", message="Корзина пуста")

            btn_buy = ttk.Button(master=self.win_Basket, text="Купить", command=buy_product_all)
            btn_buy.place(x=370, y=3)

            self.win_Basket.mainloop()
        def main_menu():
            CanMain = Canvas(bg="White", borderwidth=0, width=1980, height=1080)
            CanMain.place(x=0, y=0)

            CanMain.create_image(928, 538, image=fon_product)
            CanMain.create_image(960, 100, image=icon_logo)

            btn_Catalog = Button(text="Каталог", command=win_сatalog, bg="#953D36", fg="#57960F", font=("", 35))
            CanMain.create_window(150, 500, anchor=NW, window=btn_Catalog, width=500, height=200)

            btn_basket = Button(text="Корзина", command=win_basket, bg="#1452C5", fg="#57960F", font=("", 35))
            CanMain.create_window(1300, 500, anchor=NW, window=btn_basket, width=500, height=200)

            btn_exit = Button(text="Выход", command=Exit, bg="#F7F7F7", fg="#000000", font=("", 35))
            CanMain.create_window(950, 900, window=btn_exit, width=300, height=150)

            def Cursor():
                btn_Catalog["cursor"] = "hand2"
                btn_basket["cursor"] = "hand2"
                btn_exit["cursor"] = "hand2"
            Cursor()
        def Exit():
            for widget in self.main_win.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
            self.main_win.destroy()
        main_menu()

        self.main_win.mainloop()
call_win = Window()