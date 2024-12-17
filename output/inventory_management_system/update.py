from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as c

#===========================================CONNECTING TO DATABASE======================================================
mydb = c.connect(host="localhost", user="chinmay", password="root", database="inventory")
mycursor = mydb.cursor()
#=============================================WINDOW FROMATION==========================================================
class UpdateClass:
    def __init__(self, main):
        self.main = main
        self.main.title("Update Inventory")
        self.main.geometry("840x730+510+0")
        self.main.configure(background="light grey")

        self.GaneshProductEntry = StringVar()
        self.GaneshProductEntryQty = IntVar()
        self.GaneshProductEntryPrice = IntVar()
        self.BirthdayproductEntry = StringVar()
        self.BirthdayproductEntryQty = IntVar()
        self.BirthdayProductEntryPrice = IntVar()
        self.ProductRemove = StringVar()
        self.RemoveProduct = StringVar()
        self.Qty = IntVar()
        self.Qty2 = IntVar()
        self.Price = int()
        self.Price2 = int()
        self.count = 0
        self.ProductTableList = []
        self.ProductTable2List = []
        self.ProductTable3List = []

        self.frame_1 = Frame(self.main, background="white", borderwidth=10, relief="groove")
        self.frame_1.place(x=20, y=20, height=600, width=400)

        self.frame_2 = Frame(self.main, background="white", borderwidth=10, relief="groove")
        self.frame_2.place(x=425, y=20, height=600, width=400)

        self.HeadingLabel1 = Label(self.frame_1, text="GANESH KITCHEN APPLIANCES", foreground="black",
                                   background="light grey", font=("goudy old style", 13))
        self.HeadingLabel1.pack(side=TOP, fill='x')

        yscrollbar = Scrollbar(self.frame_1, orient=VERTICAL)

        self.ProductTable = ttk.Treeview(self.frame_1, columns=("Product", "Price", "Quantity"),
                                         yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side=RIGHT, fill='y')
        yscrollbar.config(command=self.ProductTable.yview)

        self.ProductTable.heading("Product", text="Product")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Quantity", text="Qty")
        self.ProductTable['show'] = 'headings'

        self.ProductTable.column("Product", width=230)
        self.ProductTable.column("Price", width=45)
        self.ProductTable.column("Quantity", width=30)
        self.ProductTable.pack(fill='both', expand=1)
        self.ProductTable.bind('<ButtonRelease-1>', self.get_data)

        qry1 = "select Product, Price, Qty from ProductDataTable"
        mycursor.execute(qry1)
        myresult = mycursor.fetchall()
        self.ProductTable.delete(*self.ProductTable.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable.insert(parent='', index='end', iid=i,
                                     values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

        for name in myresult:
            self.ProductTableList.append(name[0])

        self.HeadingLabel2 = Label(self.frame_2, text="BIRTHDAY APPLIANCES", foreground="black",
                                   background="light grey", font=("goudy old style", 13))
        self.HeadingLabel2.pack(side=TOP, fill='x')

        yscrollbar2 = Scrollbar(self.frame_2, orient=VERTICAL)

        self.ProductTable2 = ttk.Treeview(self.frame_2, columns=("Product", "Price", "Quantity"),
                                          yscrollcommand=yscrollbar.set)
        yscrollbar2.pack(side=RIGHT, fill='y')
        yscrollbar2.config(command=self.ProductTable2.yview)

        self.ProductTable2.heading("Product", text="Product")
        self.ProductTable2.heading("Price", text="Price")
        self.ProductTable2.heading("Quantity", text="Qty")
        self.ProductTable2['show'] = 'headings'

        self.ProductTable2.column("Product", width=230)
        self.ProductTable2.column("Price", width=45)
        self.ProductTable2.column("Quantity", width=30)
        self.ProductTable2.pack(fill='both', expand=1)
        self.ProductTable2.bind('<ButtonRelease-1>', self.get_data2)

        qry1 = "select Product, Price, Qty from BIRTHDAYTABLE"
        mycursor.execute(qry1)
        myresult = mycursor.fetchall()
        self.ProductTable2.delete(*self.ProductTable2.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable2.insert(parent='', index='end', iid=i,
                                      values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

        for name in myresult:
            self.ProductTable2List.append(name[0])
#=================================================ENTERIES=============================================================
        self.GaneshProduct = Entry(self.main, textvariable=self.GaneshProductEntry, width=40, bg='pink')
        self.GaneshProduct.place(x=40, y=630)

        self.QtyLabel = Label(self.main, text="Qty:", background='light grey')
        self.QtyLabel.place(x=35, y=665)

        self.GaneshQty = Entry(self.main, textvariable=self.GaneshProductEntryQty, width=10)
        self.GaneshQty.place(x=70, y=665)

        self.PriceLabel = Label(self.main, text="Price:", background='light grey')
        self.PriceLabel.place(x=150, y=665)

        self.GaneshPrice = Entry(self.main, textvariable=self.GaneshProductEntryPrice, width=10)
        self.GaneshPrice.place(x=190, y=665)

        self.BirthdayProduct = Entry(self.main, textvariable=self.BirthdayproductEntry, width=40, bg='pink')
        self.BirthdayProduct.place(x=450, y=630)

        self.BirthdayQty = Entry(self.main, textvariable=self.BirthdayproductEntryQty, width=10)
        self.BirthdayQty.place(x=480, y=665)

        self.QtyLabel2 = Label(self.main, text="Qty:", background='light grey')
        self.QtyLabel2.place(x=445, y=665)

        self.PriceLabel2 = Label(self.main, text="Price:", background='light grey')
        self.PriceLabel2.place(x=560, y=665)

        self.BirthdayPrice = Entry(self.main, textvariable=self.BirthdayProductEntryPrice, width=10)
        self.BirthdayPrice.place(x=600, y=665)
#========================================================================================================================
        self.but_1 = Button(self.main, text="Update", command=self.update, font=('goudy old style', 12),
                            cursor='hand2', borderwidth=3, relief="raised")
        self.but_1.place(x=345, y=670)

        self.but_2 = Button(self.main, text="Update", command=self.update2, font=('goudy old style', 12),
                            cursor='hand2', borderwidth=3, relief="raised")
        self.but_2.place(x=745, y=670)

        self.but_6 = Button(self.main, text="Search", command=self.search, font=('goudy old style', 12), cursor='hand2',
                            borderwidth=3, relief="raised", width=5, height=1)
        self.but_6.place(x=290, y=620)

        self.but_7 = Button(self.main, text="Search", command=self.search2, font=('goudy old style', 12), cursor='hand2',
                            borderwidth=3, relief="raised", width=5, height=1)
        self.but_7.place(x=700, y=620)

        self.but_8 = Button(self.main, text="Show All", command=self.show_all, font=('goudy old style', 12), cursor='hand2',
                            borderwidth=3, relief="raised", width=7, height=1)
        self.but_8.place(x=355, y=620)

        self.but_8 = Button(self.main, text="Show All", command=self.show_all2, font=('goudy old style', 12), cursor='hand2',
                            borderwidth=3, relief="raised", width=7, height=1)
        self.but_8.place(x=765, y=620)

#=========================================================================================================================
    def update(self):
        try:
                    if self.GaneshProductEntryQty.get() <= 0:
                        messagebox.showerror("Quantity ERROR!", " Enter a Valid Quantity!!")
                    else:
                        mycursor.execute(
                            f"update productdatatable set price = {self.GaneshProductEntryPrice.get()}, Qty = {self.GaneshProductEntryQty.get()} where product = '{self.GaneshProductEntry.get()}' ")

                        self.GaneshProductEntryPrice.set(0)
                        self.GaneshProductEntryQty.set(0)
                        self.GaneshProductEntry.set("")

                    qry1 = "select Product, Price, Qty from ProductDataTable"
                    mycursor.execute(qry1)
                    myresult = mycursor.fetchall()
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for i in range(0, len(myresult), 1):
                        self.ProductTable.insert(parent='', index='end', iid=i,
                                                 values=(myresult[i][0], myresult[i][1], myresult[i][2]))
                    mydb.commit()
                    '''messagebox.showinfo('', 'Update Successful)'''
        except:
            messagebox.showerror("Quantity ERROR!", " Enter a Valid Quantity!!")

    def update2(self):
        try:
                if self.BirthdayproductEntryQty.get() <= 0:
                    messagebox.showerror("Quantity ERROR!", " Enter a Valid Quantity!!")

                else:
                    mycursor.execute(
                            f"update birthdaytable set price = {self.BirthdayProductEntryPrice.get()},Qty = {self.BirthdayproductEntryQty.get()} where product = '{self.BirthdayproductEntry.get()}' ")

                    self.BirthdayProductEntryPrice.set(0)
                    self.BirthdayproductEntry.set("")
                    self.BirthdayproductEntryQty.set(0)

                qry1 = "select Product, Price, Qty from birthdaytable"
                mycursor.execute(qry1)
                myresult = mycursor.fetchall()
                self.ProductTable2.delete(*self.ProductTable2.get_children())
                for i in range(0, len(myresult), 1):
                    self.ProductTable2.insert(parent='', index='end', iid=i,
                                            values=(myresult[i][0], myresult[i][1], myresult[i][2]))
                mydb.commit()
                '''messagebox.showinfo('', 'Update Successful')'''
        except:
            messagebox.showerror("Quantity ERROR!", " Enter a Quantity!!")

    def search(self):
        for row in self.ProductTableList:
            if self.GaneshProductEntry.get() == row:
                self.ProductTable.delete(*self.ProductTable.get_children())
                mycursor.execute(f'select * from productdatatable where product = "{self.GaneshProductEntry.get()}"')
                myresult = mycursor.fetchone()
                self.ProductTable.insert(parent='', index='end',
                                             values=(myresult))
                mydb.commit()
                self.GaneshProductEntry.set('')
            else:
                pass
    def search2(self):
        for row in self.ProductTable2List:
            if self.BirthdayproductEntry.get() == row:
                self.ProductTable2.delete(*self.ProductTable2.get_children())
                mycursor.execute(f'select * from birthdaytable where product = "{self.BirthdayproductEntry.get()}"')
                myresult = mycursor.fetchone()
                self.ProductTable2.insert(parent='', index='end',
                                             values=(myresult))
                mydb.commit()
                self.BirthdayproductEntry.set('')
            else:
                pass

    def show_all(self):
        qry1 = "select Product, Price, Qty from ProductDataTable"
        mycursor.execute(qry1)
        myresult = mycursor.fetchall()
        self.ProductTable.delete(*self.ProductTable.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable.insert(parent='', index='end', iid=i, values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

    def show_all2(self):
        pass


    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.GaneshProductEntry.set(row[0])
        self.GaneshProductEntryPrice.set(row[1])
        self.GaneshProductEntryQty.set(row[2])
        self.GaneshQty.focus()
        self.Qty = row[2]
        self.Price = row[1]

    def get_data2(self, ev):
        g = self.ProductTable2.focus()
        content1 = (self.ProductTable2.item(g))
        row1 = content1['values']
        self.BirthdayproductEntry.set(row1[0])
        self.BirthdayProductEntryPrice.set(row1[1])
        self.BirthdayproductEntryQty.set(row1[2])
        self.BirthdayQty.focus()
        self.Qty2 = row1[2]
        self.Price2 = row1[1]

#=============================================================================================================================
if __name__ == "__main__":
    main = Tk()
    obj = UpdateClass(main)
    main.mainloop()
