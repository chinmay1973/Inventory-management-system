from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from update import UpdateClass
from AddRemove import AddRemoveClass
import time
import os
import tempfile
import mysql.connector as c
#===========================================CONNECTING TO DATABASE======================================================
mydb = c.connect(host="localhost", user="chinmay", password="root", database="inventory")
mycursor = mydb.cursor()
#=============================================WINDOW FROMATION==========================================================
class IMS:
    def __init__(self, main):
        self.main = main
        self.main.title("inventory")
        self.main.configure(background="light grey")
        self.main.attributes("-fullscreen", True)
#====================================================ALL VARIABLES===========================================================
        self.GaneshProductEntry = StringVar()
        self.GaneshProductEntryQty = IntVar()
        self.GaneshProductEntryPrice = StringVar()
        self.BirthdayproductEntry = StringVar()
        self.BirthdayproductEntryQty = IntVar()
        self.BirthdayproductEntryPrice = StringVar()
        self.ProductRemove = StringVar()
        self.RemoveProduct = StringVar()
        self.Name = StringVar()
        self.Name2 = StringVar()
        self.Qty = int()
        self.Qty2 = int()
        self.Price = int()
        self.Price2 = int()
        self.BillingQty = int()
        self.BillingProduct = StringVar()
        self.BillingQty2 = int()
        self.BillingProduct2 = StringVar()
        self.cart_list = []
        self.ProductTableList = []
        self.ProductTable2List = []
        self.ProductTable3List = []

        self.GlobalFrame = Frame(self.main, background='yellow')
        self.GlobalFrame.place(x=0, y=0, height=50, relwidth=1)

        self.globallabel = Label(self.GlobalFrame, text="***INVENTORY MANAGEMENT SYSTEM***", background="yellow",
                                 foreground="black", font=("goudy old style", 25, "bold"))
        self.globallabel.pack(side='top', ipadx=10, ipady=13)

        self.frame_1 = Frame(self.main, background="white", borderwidth=10, relief="groove")
        self.frame_1.place(x=20, y=60, height=600, width=400)

        self.frame_2 = Frame(self.main, background="white", borderwidth=10, relief="groove")
        self.frame_2.place(x=425, y=60, height=600, width=400)

        self.frame_3 = Frame(main, background="white", relief="groove", borderwidth=10)
        self.frame_3.place(x=900, y=100, height=300, width=300)

        self.TotalAmountLabel = Label(self.main, text=f'Total Amount:\n0.0 ', bg="light grey", fg="red")
        self.TotalAmountLabel.place(x=900, y=400)

        self.Symbol_Frame = Frame(self.GlobalFrame, background='yellow', relief='groove', borderwidth=3)
        self.Symbol_Frame.place(x=1245, y=4, height=40, width=115)

        self.MinimizeLogo = Image.open("./all_.jpg")
        self.MinimizeLogo = self.MinimizeLogo.resize((30, 30))
        self.MinimizeLogo = ImageTk.PhotoImage(self.MinimizeLogo)

        self.CloseLogo = Image.open("./close_.jpg")
        self.CloseLogo = self.CloseLogo.resize((30, 30))
        self.CloseLogo = ImageTk.PhotoImage(self.CloseLogo)

        self.RefreshLogo = Image.open("./RELOAD_.png")
        self.RefreshLogo = self.RefreshLogo.resize((30, 30))
        self.RefreshLogo = ImageTk.PhotoImage(self.RefreshLogo)

        self.Button_MinimizeLogo = Button(self.Symbol_Frame, command=self.main.iconify, cursor="hand2", image=self.MinimizeLogo)
        self.Button_MinimizeLogo.pack(side=LEFT)

        self.Button_RefreshLogo = Button(self.Symbol_Frame, command=self.refresh, cursor="hand2", image=self.RefreshLogo)
        self.Button_RefreshLogo.pack(side=LEFT)

        self.Button_CloseLogo = Button(self.Symbol_Frame, command=self.main.destroy, cursor="hand2", image=self.CloseLogo)
        self.Button_CloseLogo.pack(side=LEFT)


        self.HeadingLabel1 = Label(self.frame_1, text="GANESH KITCHEN APPLIANCES", foreground="black", background="light grey", font=("goudy old style", 13))
        self.HeadingLabel1.pack(side=TOP, fill='x')

        yscrollbar = Scrollbar(self.frame_1, orient=VERTICAL, cursor='hand2')

        self.ProductTable = ttk.Treeview(self.frame_1, columns=("Product", "Price", "Quantity"), yscrollcommand=yscrollbar.set, cursor='hand2')
        yscrollbar.pack(side=RIGHT, fill='y')
        yscrollbar.config(command=self.ProductTable.yview)

        self.ProductTable.heading("Product", text="Product")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Quantity", text="Qty")
        self.ProductTable['show'] = 'headings'

        self.ProductTable.column("Product", width=230)
        self.ProductTable.column("Price",  width=45)
        self.ProductTable.column("Quantity",  width=30)
        self.ProductTable.pack(fill='both', expand=1)
        self.ProductTable.bind('<ButtonRelease-1>', self.get_data)

        self.HeadingLabel2 = Label(self.frame_2, text="BIRTHDAY APPLIANCES", foreground="black", background="light grey", font=("goudy old style", 13))
        self.HeadingLabel2.pack(side=TOP, fill='x')

        yscrollbar2 = Scrollbar(self.frame_2, orient=VERTICAL, cursor='hand2')

        self.ProductTable2 = ttk.Treeview(self.frame_2, columns=("Product", "Price", "Quantity"), yscrollcommand=yscrollbar.set)
        yscrollbar2.pack(side=RIGHT, fill='y')
        yscrollbar2.config(command=self.ProductTable2.yview)

        self.ProductTable2.heading("Product", text="Product")
        self.ProductTable2.heading("Price", text="Price")
        self.ProductTable2.heading("Quantity", text="Qty")
        self.ProductTable2['show'] = 'headings'

        self.ProductTable2.column("Product", width=230)
        self.ProductTable2.column("Price",  width=45)
        self.ProductTable2.column("Quantity",  width=30)
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
        print(self.ProductTable2List)

        self.HeadingLabel3 = Label(self.frame_3, text="PRODUCTS", background="light grey", font=("goudy old style", 11))
        self.HeadingLabel3.pack(side=TOP, fill='x')

        yscrollbar3 = Scrollbar(self.frame_3, orient=VERTICAL, cursor='hand2')
        xscrollbar3 = Scrollbar(self.frame_3, orient=HORIZONTAL, cursor='hand2')

        self.ProductTable3 = ttk.Treeview(self.frame_3, columns=("Product", "Total Price", "Quantity"), yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar3.set)
        yscrollbar3.pack(side=RIGHT, fill='y')
        xscrollbar3.pack(side=BOTTOM, fill='x')
        yscrollbar3.config(command=self.ProductTable3.yview)
        xscrollbar3.config(command=self.ProductTable3.xview)

        self.ProductTable3.heading("Product", text="Product")
        self.ProductTable3.heading("Total Price", text="Price")
        self.ProductTable3.heading("Quantity", text="Qty")
        self.ProductTable3['show'] = 'headings'

        self.ProductTable3.column("Product", width=150)
        self.ProductTable3.column("Total Price",  width=95)
        self.ProductTable3.column("Quantity",  width=30)
        self.ProductTable3.pack(fill='both', expand=1)
        qry1 = "select Product, Price, Qty from ProductDataTable"
        mycursor.execute(qry1)
        myresult = mycursor.fetchall()
        self.ProductTable.delete(*self.ProductTable.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable.insert(parent='', index='end', iid=i, values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

        for name in myresult:
            self.ProductTableList.append(name[0])
        print(self.ProductTableList)

        self.but_1 = Button(self.main, text="Confirm", command=self.moveon, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised")
        self.but_1.place(x=300, y=720)

        self.but_2 = Button(self.main, text="Confirm", command=self.moveon1, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised")
        self.but_2.place(x=710, y=720)
        self.but_3 = Button(self.main, text="Confirm", command=self.moveon2, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised")
        self.but_3.place(x=1010, y=420)

        self.but_4 = Button(self.main, text="Remove", command=self.Remove, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=7)
        self.but_4.place(x=1010, y=480)

        self.but_5 = Button(self.main, text="Update Inventory", command=self.updateinventory, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=15)
        self.but_5.place(x=1215, y=723)

        self.but_9 = Button(self.main, text="Add to Inventory", command=self.add_remove, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=15)
        self.but_9.place(x=1050, y=723)


        self.but_6 = Button(self.main, text="Search", command=self.search, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=5, height=1)
        self.but_6.place(x=290, y=675)

        self.but_7 = Button(self.main, text="Search", command=self.search2, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=5, height=1)
        self.but_7.place(x=700, y=675)

        self.but_8 = Button(self.main, text="Show All", command=self.show_all, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=7, height=1)
        self.but_8.place(x=355, y=675)

        self.but_8 = Button(self.main, text="Show All", command=self.show_all2, font=('goudy old style', 10), cursor='hand2',
                            borderwidth=3, relief="raised", width=7, height=1)
        self.but_8.place(x=765, y=675)
#========================================================ENTERIES_1=============================================================
        self.GaneshProduct = Entry(self.main, textvariable=self.GaneshProductEntry, width=40, bg='pink')
        self.GaneshProduct.place(x=30, y=675)

        self.GaneshQty = Entry(self.main, textvariable=self.GaneshProductEntryQty, width=10)
        self.GaneshQty.place(x=70, y=710)

        self.QtyLabel = Label(self.main, text="Qty:", background='light grey')
        self.QtyLabel.place(x=35, y=710)
        # =================================================ENTERIES_2=============================================================
        self.BirthdayProduct = Entry(self.main, textvariable=self.BirthdayproductEntry, width=40, bg='pink')
        self.BirthdayProduct.place(x=440, y=675)

        self.BirthdayQty = Entry(self.main, textvariable=self.BirthdayproductEntryQty, width=10)
        self.BirthdayQty.place(x=480, y=710)

        self.QtyLabel2 = Label(self.main, text="Qty:", background='light grey')
        self.QtyLabel2.place(x=445, y=710)

    def moveon(self):
        try:
                if self.GaneshProductEntry.get() == "":
                    messagebox.showerror("Selection ERROR!", "Select A Product!!")
                elif self.GaneshProductEntryQty.get() <= 0:
                    messagebox.showerror("Quantity ERROR!", " Enter a Valid Quantity!!")
                elif self.GaneshProductEntryQty.get() > self.Qty:
                    messagebox.showerror("Quantity ERROR!", " We Dont Have That Much In Stock Right Now!!")
                else:
                    price_cal = float(int(self.GaneshProductEntryQty.get())*float(self.Price))
                    qry_1 = f"select * from productdatatable where product = '{self.GaneshProductEntry.get()}'"
                    mycursor.execute(qry_1)
                    myresult = mycursor.fetchall()
                    mydb.commit()

                    cart_data = [self.GaneshProductEntry.get(), price_cal, self.GaneshProductEntryQty.get()]

                    present = 'no'
                    index = 0
                    for row in self.cart_list:
                        if self.GaneshProductEntry.get() == row[0]:
                            present = 'yes'
                            break
                        index += 1
                    if present == 'yes':
                        response = messagebox.askyesno('Confirm', 'Do You Want to Update Ur Cart?')
                        if response == True:
                            self.cart_list[index][1] = price_cal
                            self.cart_list[index][2] = self.GaneshProductEntryQty.get()
                        else:
                            pass
                    else:
                        self.cart_list.append(cart_data)

                    self.show_cart()
                    self.TotalAmount()

                    self.BillingQty = self.GaneshProductEntryQty.get()
                    self.BillingProduct = self.GaneshProductEntry.get()

                    self.GaneshProductEntryQty.set(0)
                    self.GaneshProductEntry.set("")
        except:
                    messagebox.showerror('ERROR', 'Enter a valid Quantity1')

    def moveon1(self):
            try:
                if self.BirthdayproductEntry.get() == "":
                    messagebox.showerror("Selection ERROR!", "Select A Product!!")
                elif self.BirthdayproductEntryQty.get() <= 0:
                    messagebox.showerror("Quantity ERROR!", " Enter a Valid Quantity!!")
                elif self.BirthdayproductEntryQty.get() > self.Qty2:
                    messagebox.showerror("Quantity ERROR!", " We Dont Have That Much In Stock Right Now!!")
                else:
                    price_cal = float(int(self.BirthdayproductEntryQty.get()) * float(self.Price2))
                    qry_1 = f"select * from birthdaytable where product = '{self.BirthdayproductEntry.get()}'"
                    mycursor.execute(qry_1)
                    myresult = mycursor.fetchall()
                    mydb.commit()

                    cart_data = [self.BirthdayproductEntry.get(), price_cal, self.BirthdayproductEntryQty.get()]

                    present = 'no'
                    index = 0
                    for row in self.cart_list:
                        if self.BirthdayproductEntry.get() == row[0]:
                            present = 'yes'
                            break
                        index += 1
                    if present == 'yes':
                        response = messagebox.askyesno('Confirm', 'Do You Want to Update Ur Cart?')
                        if response == True:
                            self.cart_list[index][1] = price_cal
                            self.cart_list[index][2] = self.BirthdayproductEntryQty.get()
                    else:
                        self.cart_list.append(cart_data)

                    self.show_cart()
                    self.TotalAmount()

                    self.BillingQty2 = self.BirthdayproductEntryQty.get()
                    self.BillingProduct2 = self.BirthdayproductEntry.get()

                    self.BirthdayproductEntry.set("")
                    self.BirthdayproductEntryQty.set(0)
            except:
                messagebox.showerror("Quantity ERROR!", " Enter a Valid Quantity!!")

    def show_cart(self):
        try:
            self.ProductTable3.delete(*self.ProductTable3.get_children())
            for row in self.cart_list:
                self.ProductTable3.insert('',END, values=row)
        except Exception as ex:
            messagebox.showerror('ERROR', f'Error deu to : {str(ex)}')


    def moveon2(self):
        if len(self.cart_list) != 0:
            messagebox.showinfo('SUCCESS', 'Order Confirmed')
            self.Bill()
            self.update_stock()
            self.cart_list = []
            self.TotalAmount()
            for record in self.ProductTable3.get_children():
                self.ProductTable3.delete(record)
        else:
            messagebox.showwarning('', 'Your Cart is Empty')

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
                
    def Remove(self):
                x = self.ProductTable3.selection()[0]
                g = self.ProductTable3.focus()
                content1 = (self.ProductTable3.item(x))
                row1 = content1['values']
                row1[1] = float(row1[1])
                self.cart_list.remove(row1)
                if x != []:
                    response = messagebox.askyesno('Remove', 'Do you want to remove the selected product')
                    if response == True:
                        self.ProductTable3.delete(x)
                        self.TotalAmount()
                        messagebox.showinfo('', 'Product has been removed successfully!')
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
        qry1 = "select Product, Price, Qty from birthdaytable"
        mycursor.execute(qry1)
        myresult = mycursor.fetchall()
        self.ProductTable2.delete(*self.ProductTable2.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable2.insert(parent='', index='end', iid=i, values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

    def update_stock(self):
        for row in self.cart_list:
            mycursor.execute(f'select * from productdatatable where product = "{row[0]}"')
            stock_info = mycursor.fetchmany()
            mydb.commit()
            if stock_info != []:
                mycursor.execute(f"select qty from productdatatable where product = '{row[0]}'")
                stock_qty = mycursor.fetchone()
                mycursor.execute(
                    f"update productdatatable set Qty = {stock_qty[0] - row[2]} where product = '{row[0]}' ")
                qry1 = "select Product, Price, Qty from ProductDataTable"
                mycursor.execute(qry1)
                myresult = mycursor.fetchall()
                self.ProductTable.delete(*self.ProductTable.get_children())
                for i in range(0, len(myresult), 1):
                    self.ProductTable.insert(parent='', index='end', iid=i,
                                             values=(myresult[i][0], myresult[i][1], myresult[i][2]))
                mydb.commit()
            else:
                mycursor.execute(f"select qty from birthdaytable where product = '{row[0]}'")
                stock_qty = mycursor.fetchone()
                mycursor.execute(
                    f"update birthdaytable set Qty = {stock_qty[0] - row[2]} where product = '{row[0]}' ")
                qry1 = "select Product, Price, Qty from birthdaytable"
                mycursor.execute(qry1)
                myresult = mycursor.fetchall()
                self.ProductTable2.delete(*self.ProductTable2.get_children())
                for i in range(0, len(myresult), 1):
                    self.ProductTable2.insert(parent='', index='end', iid=i,
                                             values=(myresult[i][0], myresult[i][1], myresult[i][2]))
                mydb.commit()

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.GaneshProductEntry.set(row[0])
        self.GaneshProductEntryQty.set(row[2])
        self.GaneshQty.focus()
        self.Name = row[0]
        self.Qty = row[2]
        self.Price = row[1]

    def get_data2(self, ev):
        g = self.ProductTable2.focus()
        content1 = (self.ProductTable2.item(g))
        row1 = content1['values']
        self.BirthdayproductEntry.set(row1[0])
        self.BirthdayproductEntryQty.set(row1[2])
        self.BirthdayQty.focus()
        self.Name2 = row1[0]
        self.Qty2 = row1[2]
        self.Price2 = row1[1]

    def TotalAmount(self):
        self.bill_amount = 0
        for row in self.cart_list:
            self.bill_amount = self.bill_amount + row[1]
        self.TotalAmountLabel.config(text=f'Total Amount:\n{float(self.bill_amount)}')

    def refresh(self):
        qry1 = "select Product, Price, Qty from ProductDataTable"
        mycursor.execute(qry1)
        myresult = mycursor.fetchall()
        self.ProductTable.delete(*self.ProductTable.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable.insert(parent='', index='end', iid=i, values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

        qry2 = "select Product, Price, Qty from BIRTHDAYTABLE"
        mycursor.execute(qry2)
        myresult = mycursor.fetchall()
        self.ProductTable2.delete(*self.ProductTable2.get_children())
        for i in range(0, len(myresult), 1):
            self.ProductTable2.insert(parent='', index='end', iid=i,
                                     values=(myresult[i][0], myresult[i][1], myresult[i][2]))

        mydb.commit()

    def PrintBill(self):
        messagebox.showinfo('Print', 'Your Bill is Printing!')
        new_file = tempfile.mktemp('.txt')
        open(new_file, 'w').write(self.Bill_Window.get('1.0', END))
        os.startfile(new_file, 'print')

    def Bill(self):
        self.invoice = str(time.strftime("%H%M%S")+str(time.strftime("%d%m%Y")))
        bill_top_temp = f'''
        \t\tShalimar Township
        \t404, Begonia, A.B. Road, Indore
        Phone No.= 8827400458, 9826628441
{str('*' * 49)}
        \t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}\n
 Product Name\t\tP/P\tQty\tTotal Price
{str('*' * 49)}
                '''
        bill_bottom_temp = f'''
{str('*' * 49)}
 Total Bill Amount:\t\t\t\tRs.{self.bill_amount}
{str('*' * 49)}
        '''
        self.new_win_2 = Toplevel(self.main)
        self.new_win_2.focus_force()
        self.new_win_2.geometry("400x430")
        self.new_win_2.title('Bill')
        self.new_win_2.configure(background='white')
        self.Frame_1 = Frame(self.new_win_2)
        self.Frame_1.place(x=0, y=0, height=400, width=400)
        self.Bill_Window = Text(self.Frame_1)
        self.Bill_Window.pack(fill=BOTH, expand=1)
        self.Bill_Window.delete('1.0', END)
        self.Bill_Window.insert('1.0', bill_top_temp)
        for row in self.cart_list:
            name = row[0]
            qty = row[2]
            price = row[1]
            per_price = price / qty
            qty = str(qty)
            price = str(price)
            self.Bill_Window.insert(END, '\n '+name+'\t\t\t'+qty+'\tRs.'+price+f'\n\t     Rs.{per_price}')
        self.Bill_Window.insert(END, bill_bottom_temp)
        self.Bill_Window['state'] = 'disable'
        file_open = open(f'D:/BILLS/{str(self.invoice)}.text', 'w')
        file_open.write(self.Bill_Window.get('1.0', END))
        file_open.close()
        self.button = Button(self.new_win_2, text='Print', command=self.PrintBill, font=("goudy old style", 12), cursor='hand2')
        self.button.place(x=155, y=400, height=30, width=100)

    def updateinventory(self):
        self.new_win = Toplevel(self.main)
        self.new_obj = UpdateClass(self.new_win)

    def add_remove(self):
        self.new_win3 = Toplevel(self.main)
        self.new_obj3 = AddRemoveClass(self.new_win3)


#=====================================================END===============================================================
if __name__ == "__main__":
    main = Tk()
    obj = IMS(main)
    main.mainloop()
#=======================================================================================================================