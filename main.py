#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.ttk
import sqlite3
import os

class TkClass(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.geometry("870x350")
        self.frame1 = Frame(self.parent)
        self.frame2 = Frame(self.parent)
        self.index = 0
        self.create_database()
        self.UI()



    def UI(self):

        self.tree = tkinter.ttk.Treeview(self.parent, height=11)
        vsb = tkinter.ttk.Scrollbar(self.parent, orient="vertical", command=self.tree.yview)
        vsb.place(x=30 + 820 + 2, y=0, height=225 + 20)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree['columns'] = ('num', 'name', 'surname','tel')
        self.tree.heading("#0", text=' ', anchor='center')
        self.tree.column("#0", anchor="center",width=0,minwidth= 0)
        self.tree.heading('num', text='Numarası', anchor='center')
        self.tree.column('num', anchor='center', width=100,minwidth= 130)
        self.tree.heading('name', text='Adı', anchor='center')
        self.tree.column('name', anchor='center', width=250,minwidth= 125)
        self.tree.heading('surname', text='Soyadı', anchor='center')
        self.tree.column('surname', anchor='center', width=250,minwidth=0)
        self.tree.heading('tel', text='Telefonu', anchor='center')
        self.tree.column('tel', anchor='center', width=250, minwidth=0)
        self.tree.grid(sticky = (N,S,W,E),row = 0, column = 0,padx = 0,pady=0,columnspan = 3 ,rowspan = 1)

        self.canvas = Canvas(self.tree, relief=SUNKEN, borderwidth=2)
        self.vscroll = Scrollbar(self.tree, command=self.canvas.yview)
        self.tree.grid_rowconfigure(0, weight = 1)
        self.tree.grid_columnconfigure(0, weight = 1)
        self.data = sqlite3.connect("members.db")
        self.veri = self.data.cursor()
        if self.veri.execute("SELECT name FROM sqlite_master").fetchone() != None:
            for i in self.veri.execute("SELECT * FROM people").fetchall():
                self.tree.insert('', 'end', text= self.index, values=(i[0],i[1],i[2],i[3]))
        self.label1 = Label(self.frame1, text = "Öğrenci No",font=("Helvatica bold", 12))
        self.label1.grid(row=0,column=0)
        self.entry1 = Entry(self.frame1,font=("Helvatica bold", 12))
        self.entry1.grid(row=0,column=1)
        self.label2 = Label(self.frame1, text="Öğrenci Adı",font=("Helvatica bold", 12))
        self.label2.grid(row=1, column=0)
        self.entry2 = Entry(self.frame1,font=("Helvatica bold", 12))
        self.entry2.grid(row=1, column=1)
        self.label3 = Label(self.frame1, text="Öğrenci Soyadı",font=("Helvatica bold", 12))
        self.label3.grid(row=2, column=0)
        self.entry3 = Entry(self.frame1,font=("Helvatica bold", 12))
        self.entry3.grid(row=2, column=1)
        self.label4 = Label(self.frame1, text="Öğrenci Telefonu",font=("Helvatica bold", 12))
        self.label4.grid(row=3, column=0)
        self.entry4 = Entry(self.frame1,font=("Helvatica bold", 12))
        self.entry4.grid(row=3, column=1)
        self.frame1.grid(row=1,column=0,columnspan=2)

        self.button1 = Button(self.frame2, text = "Ekle", command = self.add,font=("Helvatica bold", 12))
        self.button1.grid(row=0,column=0,ipadx=15,pady=2)
        self.button2 = Button(self.frame2, text="Güncelle", command=self.update,font=("Helvatica bold", 12))
        self.button2.grid(row=1, column=0)
        self.button3 = Button(self.frame2, text="Sil", command=self.delete,font=("Helvatica bold", 12))
        self.button3.grid(row=2, column=0,ipadx=21)
        self.frame2.grid(row=1,column=2,columnspan=1)

    def clear_entry(self):
        self.entry1.delete(0,END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
    def add(self):
        i = [self.entry1.get(),self.entry2.get(),self.entry3.get(),self.entry4.get()]
        if i[0] != "" and i[1] != "" and i[2] != "" and i[3] != "":
            self.add_database(i)
            self.update_treview()
        else:
            pass
        self.clear_entry()
    def update(self):
        i = [self.entry1.get(),self.entry2.get(),self.entry3.get(),self.entry4.get()]
        if i[0] != "" and i[1] != "" and i[2] != "" and i[3] != "":
            self.update_database(i)
            self.update_treview()
        else:
            pass
        self.clear_entry()
    def delete(self):
        i = [self.entry1.get(),self.entry2.get(),self.entry3.get(),self.entry4.get()]
        if i[0] != "" and i[1] != "" and i[2] != "" and i[3] != "":
            self.remove_database(i)
            self.update_treview()
        else:
            pass
        self.clear_entry()
    def update_treview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.data = sqlite3.connect("members.db")
        self.veri = self.data.cursor()
        for i in self.veri.execute("SELECT * FROM people").fetchall():
            self.tree.insert('', 'end', text=self.index, values=(i[0], i[1], i[2], i[3]))
        self.data.close()
    def create_database(self):
        self.data = sqlite3.connect("members.db")
        self.veri = self.data.cursor()
        if self.veri.execute("SELECT name FROM sqlite_master").fetchone() == None:
            self.veri.execute("""CREATE TABLE {} (
                    'numara'	TEXT,
                    'adi'   TEXT,
                    'soyadi'  TEXT,
                    'telefonu'  TEXT,
                    PRIMARY KEY(numara));""".format('people'))
            self.data.commit()
            self.data.close()
        else:
            pass
    def add_database(self,data):
        self.data = sqlite3.connect("members.db")
        self.veri = self.data.cursor()
        self.veri.execute("INSERT INTO people (numara,adi,soyadi, telefonu) VALUES (?,?,?,?)",(data[0], data[1], data[2],data[3]))
        self.data.commit()
        self.data.close()
    def update_database(self,data):
        self.data = sqlite3.connect("members.db")
        self.veri = self.data.cursor()
        self.veri.execute("""UPDATE people SET adi = ?, soyadi = ?, telefonu = ? WHERE numara = ? """,(data[1],data[2],data[3],data[0]))
        self.data.commit()
        self.data.close()
    def remove_database(self,data):
        self.data = sqlite3.connect("members.db")
        self.veri = self.data.cursor()
        self.veri.execute('''DELETE FROM people WHERE numara=?''',(data[0],))
        self.data.commit()
        self.data.close()



if __name__ == "__main__":
    root = Tk()
    app = TkClass(root)
    root.mainloop()


