from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter
import random
import pymysql
import csv
from datetime import datetime
btnColor='#3d47e6'
#afficher l'inerface principale 

def afficher_interface_gestion():
    print("Changement d'interface")  
    interface_verification.place_forget()
    frame_principale.place(relwidth=1, relheight=1)  
    config_menu()

# afficher l'interface de virification de code 
def verifier_code():
    code = code_entry.get()
    name = name_entry.get()
    if code == "1234" and name == 'admin':
        afficher_interface_gestion()
    else:
        messagebox.showerror("Erreur", "Code incorrect")
# la fenêtre 

window = Tk()
window.title("Gestion des Stocks")
window.geometry("720x640")
window.iconbitmap("C:\\Users\\HP\\Desktop\\projet_stage\\logo.ico")


photo = Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\plan.jpg")  
photo1 = photo.resize((720, 640))
photo2 = ImageTk.PhotoImage(photo1)
lable_window = Label(window, image=photo2)
lable_window.place(relwidth=1, relheight=1)
lable_window.image = photo2

# une fonction reteurner les informations de connexion avec la base de données 

def connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='stockage'
    )

# une fonction pour ajouter un elemment 

def ajouter():
    def read():
      with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks "
            cursor.execute(sql)
            results = cursor.fetchall()
      return results

    def refreshTable():
       for data in my_tree.get_children():
           my_tree.delete(data)
       for array in read():
           my_tree.insert(parent='', index='end', iid=array, text="", values=array, tag="orow")
       my_tree.tag_configure('orow', background="#EEEEEE")
       my_tree.grid(row=2, column=0, columnspan=7, sticky='nsew')
    def save():
        itemId = itemIdEntry.get().strip()
        name = nameEntry.get().strip()
        price = priceEntry.get().strip()
        qnt = qntEntry.get().strip()
        cat = categoryCombo.get().strip()
        if not all([itemId, name, price, qnt, cat]):
            messagebox.showwarning("", "Veuillez remplir tous les champs")
            return
        def test(itemId):
            conn=pymysql.connect(host='localhost',user='root',password='',db='abdo')
            corsur=conn.cursor()
            sql="select * from stocks where item_id=%s"
            corsur.execute(sql,(itemId,))
            result=corsur.fetchone()
            conn.close()
            if result:
                return True
            else:
                return False
        if test==TRUE:
            messagebox.showwarning("", "ID d'article invalide")
            return
        with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM stocks WHERE `item_id` = %s"
            cursor.execute(sql, (itemId,))
            if cursor.fetchall():
                messagebox.showwarning("", "ID d'article déjà utilisé")
                return
            sql = "INSERT INTO stocks (`item_id`, `name`, `price`, `quantity`, `category`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (itemId, name, price, qnt, cat))
            conn.commit()
        itemIdEntry.delete(0, END)
        nameEntry.delete(0, END)
        priceEntry.delete(0, END)
        qntEntry.delete(0, END)
        categoryCombo.set('')
        refreshTable()
    frame=Frame(window,bg='#7a7978')
    frame.place(relheight=1,relwidth=1)
    im=Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\stockage.jpg")
    im1=im.resize((720,640))
    im2=ImageTk.PhotoImage(im1)
    l=Label(frame,image=im2)
    l.place(relwidth=1,relheight=1)
    l.image=im2
    my_tree = ttk.Treeview(frame, show='headings', height=20)
    style = ttk.Style()
    
    entriesFrame = tkinter.LabelFrame(frame, text="Formulaire", borderwidth=5)
    entriesFrame.grid(row=1, column=0, sticky="w", padx=[10, 200], pady=[0, 20], ipadx=[6])

    itemIdLabel = Label(entriesFrame, text="ID ARTICLE", anchor="e", width=10)
    nameLabel = Label(entriesFrame, text="NOM", anchor="e", width=10)
    priceLabel = Label(entriesFrame, text="PRIX", anchor="e", width=10)
    qntLabel = Label(entriesFrame, text="QNT", anchor="e", width=10)
    categoryLabel = Label(entriesFrame, text="CATÉGORIE", anchor="e", width=10)

    itemIdLabel.grid(row=0, column=0, padx=10)
    nameLabel.grid(row=1, column=0, padx=10)
    priceLabel.grid(row=2, column=0, padx=10)
    qntLabel.grid(row=3, column=0, padx=10)
    categoryLabel.grid(row=4, column=0, padx=10)

    categoryArray = ['Montagne','Ville','Route','Hybride','BMX','Électrique','Pliable','Gravel','Enfant','Tourisme']

    itemIdEntry = Entry(entriesFrame, width=50)
    nameEntry = Entry(entriesFrame, width=50)
    priceEntry = Entry(entriesFrame, width=50)
    qntEntry = Entry(entriesFrame, width=50)
    categoryCombo = ttk.Combobox(entriesFrame, width=47, values=categoryArray)

    itemIdEntry.grid(row=0, column=2, padx=5, pady=5)
    nameEntry.grid(row=1, column=2, padx=5, pady=5)
    priceEntry.grid(row=2, column=2, padx=5, pady=5)
    qntEntry.grid(row=3, column=2, padx=5, pady=5)
    categoryCombo.grid(row=4, column=2, padx=5, pady=5)

    style.configure(frame)
    my_tree['columns'] = ("ID Article", "Nom", "Prix", "Quantité", "Catégorie", "Date")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID Article", anchor=W, width=70)
    my_tree.column("Nom", anchor=W, width=125)
    my_tree.column("Prix", anchor=W, width=125)
    my_tree.column("Quantité", anchor=W, width=100)
    my_tree.column("Catégorie", anchor=W, width=150)
    my_tree.column("Date", anchor=W, width=150)
    my_tree.heading("ID Article", text="ID Article", anchor=W)
    my_tree.heading("Nom", text="Nom", anchor=W)
    my_tree.heading("Prix", text="Prix", anchor=W)
    my_tree.heading("Quantité", text="Quantité", anchor=W)
    my_tree.heading("Catégorie", text="Catégorie", anchor=W)
    my_tree.heading("Date", text="Date", anchor=W)
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.place()
    refreshTable()
    saveBtn = Button(frame, text="ENREGISTRER", width=10, borderwidth=3, bg='#29cf2c', fg='white', command=save)
    saveBtn.place(x=470,y=140)

#une fonction pour supprimer un élement 

def supprimer():
    def read():
      with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks "
            cursor.execute(sql)
            results = cursor.fetchall()
      return results

    def refreshTable():
       for data in my_tree.get_children():
           my_tree.delete(data)
       for array in read():
           my_tree.insert(parent='', index='end', iid=array, text="", values=array, tag="orow")
       my_tree.tag_configure('orow', background="#EEEEEE")
       my_tree.grid(row=2, column=0, columnspan=7, sticky='nsew')
    def suppr():
     try:
        if my_tree.selection()[0]:
            decision = messagebox.askquestion("", "Supprimer les données sélectionnées ?")
            if decision == 'yes':
                selectedItem = my_tree.selection()[0]
                itemId = my_tree.item(selectedItem)['values'][0]
                with connection() as conn:
                    cursor = conn.cursor()
                    sql = "DELETE FROM stocks WHERE `item_id` = %s"
                    cursor.execute(sql, (itemId,))
                    conn.commit()
                messagebox.showinfo("", "Données supprimées avec succès")
                refreshTable()
     except:
        messagebox.showwarning("", "Veuillez sélectionner une ligne de données")

    frame=Frame(window)
    frame.place(relheight=1,relwidth=1)
    im=Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\stockage.jpg")
    im1=im.resize((720,640))
    im2=ImageTk.PhotoImage(im1)
    l=Label(frame,image=im2)
    l.place(relwidth=1,relheight=1)
    l.image=im2
    my_tree = ttk.Treeview(frame, show='headings', height=20)
    style = ttk.Style()

    
    style.configure(frame)
    my_tree['columns'] = ("ID Article", "Nom", "Prix", "Quantité", "Catégorie", "Date")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID Article", anchor=W, width=70)
    my_tree.column("Nom", anchor=W, width=125)
    my_tree.column("Prix", anchor=W, width=125)
    my_tree.column("Quantité", anchor=W, width=100)
    my_tree.column("Catégorie", anchor=W, width=150)
    my_tree.column("Date", anchor=W, width=150)
    my_tree.heading("ID Article", text="ID Article", anchor=W)
    my_tree.heading("Nom", text="Nom", anchor=W)
    my_tree.heading("Prix", text="Prix", anchor=W)
    my_tree.heading("Quantité", text="Quantité", anchor=W)
    my_tree.heading("Catégorie", text="Catégorie", anchor=W)
    my_tree.heading("Date", text="Date", anchor=W)
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.place()
    refreshTable()
   
    supprimerbtn = Button(frame, text="SUPPRIMER", width=30,height=2, borderwidth=3, bg='#29cf2c', fg='white', command=suppr)
    supprimerbtn.place(anchor=CENTER,relx=0.5,y=480)
def modifier():
    
    placeholderArray = ['', '', '', '', '']
    def read():
      with connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks "
            cursor.execute(sql)
            results = cursor.fetchall()
      return results
    def refreshTable():
       for data in my_tree.get_children():
           my_tree.delete(data)
       for array in read():
           my_tree.insert(parent='', index='end', iid=array, text="", values=array, tag="orow")
       my_tree.tag_configure('orow', background="#EEEEEE")
    # Utilisez grid au lieu de pack
       my_tree.grid(row=2, column=0, columnspan=7, sticky='nsew')
    def setph(word, num):
       placeholderArray[num] = word
    def select():
      try:
        selectedItem = my_tree.selection()[0]
        values = my_tree.item(selectedItem)['values']
        for i, value in enumerate(values):
            setph(value, i)
      except:
        messagebox.showwarning("", "Veuillez sélectionner une ligne de données")
    def modif():
        itemId = itemIdEntry.get().strip()
        name = nameEntry.get().strip()
        price = priceEntry.get().strip()
        qnt = qntEntry.get().strip()
        cat = categoryCombo.get().strip()
        if not all([itemId, name, price, qnt, cat]):
            messagebox.showwarning("", "Veuillez remplir tous les champs")
            return
        
        with connection() as conn:
            cursor = conn.cursor()
            sql = "UPDATE stocks SET `name` = %s, `price` = %s, `quantity` = %s, `category` = %s WHERE `item_id` = %s"
            cursor.execute(sql, (name, price, qnt, cat, itemId))
            conn.commit()
        refreshTable()



    frame=Frame(window)
    frame.place(relheight=1,relwidth=1)
    im=Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\stockage.jpg")
    im1=im.resize((720,640))
    im2=ImageTk.PhotoImage(im1)
    l=Label(frame,image=im2)
    l.place(relwidth=1,relheight=1)
    l.image=im2
    my_tree = ttk.Treeview(frame, show='headings', height=20)
    style = ttk.Style()
 
    entriesFrame = tkinter.LabelFrame(frame, text="Formulaire", borderwidth=5)
    entriesFrame.grid(row=1, column=0, sticky="w", padx=[10, 200], pady=[0, 20], ipadx=[6])

    itemIdLabel = Label(entriesFrame, text="ID ARTICLE", anchor="e", width=10)
    nameLabel = Label(entriesFrame, text="NOM", anchor="e", width=10)
    priceLabel = Label(entriesFrame, text="PRIX", anchor="e", width=10)
    qntLabel = Label(entriesFrame, text="QNT", anchor="e", width=10)
    categoryLabel = Label(entriesFrame, text="CATÉGORIE", anchor="e", width=10)

    itemIdLabel.grid(row=0, column=0, padx=10)
    nameLabel.grid(row=1, column=0, padx=10)
    priceLabel.grid(row=2, column=0, padx=10)
    qntLabel.grid(row=3, column=0, padx=10)
    categoryLabel.grid(row=4, column=0, padx=10)

    categoryArray = ['Outils de Réseau', 'Composants Informatiques', 'Outils de Réparation', 'Gadgets']

    itemIdEntry = Entry(entriesFrame, width=50)
    nameEntry = Entry(entriesFrame, width=50)
    priceEntry = Entry(entriesFrame, width=50)
    qntEntry = Entry(entriesFrame, width=50)
    categoryCombo = ttk.Combobox(entriesFrame, width=47, values=categoryArray)

    itemIdEntry.grid(row=0, column=2, padx=5, pady=5)
    nameEntry.grid(row=1, column=2, padx=5, pady=5)
    priceEntry.grid(row=2, column=2, padx=5, pady=5)
    qntEntry.grid(row=3, column=2, padx=5, pady=5)
    categoryCombo.grid(row=4, column=2, padx=5, pady=5)

    # generateIdBtn = Button(entriesFrame, text="GÉNÉRER ID", borderwidth=3, bg=btnColor, fg='white', command=generateRand)
    # generateIdBtn.grid(row=0, column=3, padx=5, pady=5)
    def selec():
        
        try:
            selectedItem = my_tree.selection()[0]
            values = my_tree.item(selectedItem)['values']
          
            itemIdEntry.delete(0, END)
            itemIdEntry.insert(0, values[0])
            nameEntry.delete(0, END)
            nameEntry.insert(0, values[1])
            priceEntry.delete(0, END)
            priceEntry.insert(0, values[2])
            qntEntry.delete(0, END)
            qntEntry.insert(0, values[3])
            categoryCombo.set(values[4])
        except:
            messagebox.showwarning("", "Veuillez sélectionner une ligne de données")
    style.configure(frame)
    my_tree['columns'] = ("ID Article", "Nom", "Prix", "Quantité", "Catégorie", "Date")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID Article", anchor=W, width=70)
    my_tree.column("Nom", anchor=W, width=125)
    my_tree.column("Prix", anchor=W, width=125)
    my_tree.column("Quantité", anchor=W, width=100)
    my_tree.column("Catégorie", anchor=W, width=150)
    my_tree.column("Date", anchor=W, width=150)
    my_tree.heading("ID Article", text="ID Article", anchor=W)
    my_tree.heading("Nom", text="Nom", anchor=W)
    my_tree.heading("Prix", text="Prix", anchor=W)
    my_tree.heading("Quantité", text="Quantité", anchor=W)
    my_tree.heading("Catégorie", text="Catégorie", anchor=W)
    my_tree.heading("Date", text="Date", anchor=W)
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.place()
    refreshTable()
    # label_logo=Label(frame,font=("Amasis MT Pro ",80,"bold"),fg='black',text="S9",bg='#7a7978')
    # label_logo.place(width=180,height=150,x=500)
    saveBtn = Button(frame, text="MODIFIER", width=10, borderwidth=3, bg='#29cf2c', fg='white', command=modif)
    saveBtn.place(x=470,y=80)
    selectBtn = Button(frame, text="SÉLECTIONNER", width=10, borderwidth=3, bg='#29cf2c', fg='white', command=selec)
    selectBtn.place(x=470,y=120)

#une fonction pour chercher sur un élement
 
def chercher():
    def read():
            id=cherche.get()
            conn=pymysql.connect(host='localhost',user='root',password='',db='stockage')
            corsur=conn.cursor()
            sql="select * from stocks where item_id=%s"
            corsur.execute(sql,(id,))
            result=corsur.fetchone()
            conn.close()
            if result:
                itemIdEntry.config(text=result[0])
                nameEntry.config(text= result[1])
                priceEntry.config(text=result[2])
                qntEntry.config(text=result[3])
                categoryCombo.config(text=result[4])
            else:
                messagebox.showwarning("Avertissement", "ID non trouvé")

    frame=Frame(window)
    frame.place(relheight=1,relwidth=1)
    im=Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\stockage.jpg")
    im1=im.resize((720,640))
    im2=ImageTk.PhotoImage(im1)
    l=Label(frame,image=im2)
    l.place(relwidth=1,relheight=1)
    l.image=im2
    entriesFrame = Frame(frame, borderwidth=5)
    entriesFrame.place(x=10,y=100,width=600,height=400)
    itemIdLabel = Label(entriesFrame, text="ID ARTICLE", anchor="e", width=10)
    nameLabel = Label(entriesFrame, text="NOM", anchor="e", width=10)
    priceLabel = Label(entriesFrame, text="PRIX", anchor="e", width=10)
    qntLabel = Label(entriesFrame, text="QNT", anchor="e", width=10)
    categoryLabel = Label(entriesFrame, text="CATÉGORIE", anchor="e", width=10)    

    itemIdLabel.grid(row=0, column=0, padx=10)
    nameLabel.grid(row=1, column=0, padx=10)
    priceLabel.grid(row=2, column=0, padx=10)
    qntLabel.grid(row=3, column=0, padx=10)
    categoryLabel.grid(row=4, column=0, padx=10)

    itemIdEntry = Label(entriesFrame, width=50,bg="#807c84",fg="#070708")
    nameEntry = Label(entriesFrame, width=50,bg="#807c84",fg="#070708")
    priceEntry = Label(entriesFrame, width=50,bg="#807c84",fg="#070708")
    qntEntry = Label(entriesFrame, width=50,bg="#807c84",fg="#070708")
    categoryCombo = Label(entriesFrame, width=47,bg="#807c84",fg="#070708")

    itemIdEntry.grid(row=0, column=2, padx=5, pady=5)#807c84
    nameEntry.grid(row=1, column=2, padx=5, pady=5)
    priceEntry.grid(row=2, column=2, padx=5, pady=5)
    qntEntry.grid(row=3, column=2, padx=5, pady=5)
    categoryCombo.grid(row=4, column=2, padx=5, pady=5)

    cherche=Entry(window)
    cherche.place(x=20,y=30,width=100,height=30)

    btn=Button(window,text="chercher",command=read,bg='#29cf2c')
    btn.place(x=140,y=30,width=100,height=30)

# une fonction pour fermer la fenêtre 

def exit():
    window.destroy()

im_1=Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\images.jpeg")
im1_1=im_1.resize((400,400))
im2_1=ImageTk.PhotoImage(im1_1)

interface_verification = Frame(window, borderwidth=0,bg='#9f55e1')
interface_verification.place(anchor=CENTER, width=400, height=400, relx=0.5, rely=0.5)

label_plan=Label(interface_verification,image=im2_1)
label_plan.place(anchor=CENTER, width=400, height=400, relx=0.5, rely=0.5)
label_plan.image=im2_1

label_name = Label(interface_verification, text="Nom utilisateur :")
label_name.place(width=100, height=30, y=100, x=30)

name_entry = Entry(interface_verification)
name_entry.place(width=200, height=30, y=100, x=150)

label_code = Label(interface_verification, text="Mot de passe :")
label_code.place(width=100, height=30, y=170, x=30)

code_entry = Entry(interface_verification, show='*')
code_entry.place(width=200, height=30, y=170, x=150)

bouton_verifier = Button(interface_verification, text="Se connecter", command=verifier_code)
bouton_verifier.place(width=200, height=30, y=250, relx=0.5, anchor=CENTER)

frame_principale = Frame(window)
frame_principale.place()
im=Image.open("C:\\Users\\HP\\Desktop\\projet_stage\\stokage.png")
im1=im.resize((720,640))
im2=ImageTk.PhotoImage(im1)
l=Label(frame_principale,image=im2)
l.place(relwidth=1,relheight=1)
l.image=im2

# une fonction pour créer un menu 

def config_menu():
    
    menubar=Menu(frame_principale)
    menufichier=Menu(menubar)

    menubar.add_cascade(label="                         Menu                          ",menu=menufichier)
    menufichier.add_command(label='Ajouter',command=ajouter, font=("Times New Roman ", 10,"italic"))
    menufichier.add_separator() 

    menufichier.add_command(label="Modifier",command=modifier, font=("Times New Roman ", 10,"italic"))
    menufichier.add_separator() 

    menufichier.add_command(label='Supprimer',command=supprimer, font=("Times New Roman ", 10,"italic"))
    menufichier.add_separator() 

    menufichier.add_command(label='chercher',command=chercher, font=("Times New Roman ", 10,"italic"))
    menufichier.add_separator() 
    menufichier.add_separator() 

    menufichier.add_command(label='Exit',command=exit, font=("Times New Roman ", 10,"italic"))
    menufichier.add_separator() 
    window.config(menu=menubar)
window.resizable(False, False)
window.mainloop()
