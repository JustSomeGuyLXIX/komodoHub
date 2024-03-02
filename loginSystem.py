import customtkinter
import sqlite3
import bcrypt 
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry

app = customtkinter.CTk()
app.title("login")
app.geometry("450x360")
app.config(bg="#001220")
#creates window

font1 = ("Helvetica",30,"bold") #for titles
font2 = ("Arial",17,"bold") #for any other text
font3 = ("Arial",30,"bold") #for buttons

conn = sqlite3.connect("komodoHub.db")
cursor = conn.cursor()
#connects program to database

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        passID   INTEGER PRIMARY KEY AUTOINCREMENT,
        passHash TEXT NOT NULL
    )''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userID   INTEGER PRIMARY KEY AUTOINCREMENT,
        fName    TEXT,
        lName    TEXT,
        email    TEXT,
        passID   INTEGER,
        username TEXT,
        roleID   INTEGER,
        visualID INTEGER,
        dob      TEXT,
        FOREIGN KEY (visualID) REFERENCES visPreset (visID),
        FOREIGN KEY (roleID) REFERENCES role (roleID),
        FOREIGN KEY (passID) REFERENCES passwords (passID)
    )''')
#stops duplicate tables i think, will need to change to match the database.

def register():
    fName = fName_entry.get()
    lName = lName_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirmPass = confPass_entry.get()
    DOB = bdayCal.get()

    if email != '' and password != '' and fName != '' and lName != '' and confirmPass != '' and DOB != '': #ensures that they arent empty
        cursor.execute('SELECT email FROM users WHERE email=?', [email])
        if cursor.fetchone() is not None: #ensures that unique email is used
            messagebox.showerror('Error', 'Email already exists')
        else:
            if password == confirmPass: #ensures that passwords are matching
                encoded_password = password.encode('utf-8')
                passHash = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                
                cursor.execute('INSERT INTO passwords (passHash) VALUES (?)', [passHash])
                passID = cursor.lastrowid  # Retrieve the last inserted ID
                #Inserts the hashed password into the 'passwords' table
                cursor.execute('INSERT INTO users (fName, lName, email, passID, dob) VALUES (?, ?, ?, ?, ?)', [fName, lName, email, passID, DOB])
                #Inserts user info along with the passID from passwords table into the users table
                conn.commit()
                
                messagebox.showinfo('Success', 'Account has been created')
            else:
                messagebox.showerror('Error', 'Your passwords do not match')
    else:
        messagebox.showerror('Error', 'Enter all data')
    email = None
    password = None
    fName = None
    lName = None
    confirmPass = None
    DOB = None
    #deletes data from variables to ensure that data is safe

def login():
    email = email_entry2.get()
    password = password_entry2.get()
    if email != '' and password != '': #ensures that all data is inputted
        cursor.execute('SELECT passID FROM users WHERE email=?', [email])
        result = cursor.fetchone()
        if result:
            passID = result[0] #ensures that only a number is stored
            cursor.execute('SELECT passHash FROM passwords WHERE passID=?', [passID]) #Retrieves the passHash from the passwords table using passID
            passHash = cursor.fetchone()

            if passHash and bcrypt.checkpw(password.encode('utf-8'), passHash[0]): #checks that the password is correct
                messagebox.showinfo('Success', 'Logged in successfully')
            else:
                messagebox.showerror('Error', 'Invalid password')
            result = None
            passHash = None 
            #ensures data is safe by removing the data from variables
        else:
            messagebox.showerror('Error', 'Invalid email')
    else:
        messagebox.showerror('Error', 'Enter all data')
    email = None
    password = None
    #ensures data is safe by removing the data from variables

def loginPage(): #frame3
    frame1.destroy()
    frame3 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=470,height=360)
    frame3.place(x=0,y=0)

    login_label = customtkinter.CTkLabel(frame3,font=font1,text='Log in',text_color='#fff',bg_color='#001220')
    login_label.place(x=180,y=20)

    global email_entry2
    global password_entry2

    email_entry2 = customtkinter.CTkEntry(frame3,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='Email',placeholder_text_color='#a3a3a3',width=400,height=50)
    email_entry2.place(x=25,y=80)

    password_entry2 = customtkinter.CTkEntry(frame3,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='Password',placeholder_text_color='#a3a3a3',width=400,height=50)
    password_entry2.place(x=25,y=150)

    login_btn = customtkinter.CTkButton(frame3,command=login,font=font3,text='Login',text_color='#fff')
    login_btn.place(x=160,y=250)

def regPage(): #frame2
    frame1.destroy()
    app.geometry('450x640')
    frame2 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=470,height=640)
    frame2.place(x=0,y=0)

    signup_label = customtkinter.CTkLabel(frame2,font=font1,text='Register',text_color='#fff',bg_color='#001220')
    signup_label.place(x=160,y=20)


    global fName_entry
    global lName_entry
    global bdayCal
    global email_entry
    global password_entry
    global confPass_entry
    global genderVar

    #update this

    fName_entry = customtkinter.CTkEntry(frame2,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='First name',placeholder_text_color='#a3a3a3',width=300,height=50)
    fName_entry.place(x=70,y=80)

    lName_entry = customtkinter.CTkEntry(frame2,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='Last name',placeholder_text_color='#a3a3a3',width=300,height=50)
    lName_entry.place(x=70,y=150)

    bdayCal = DateEntry(frame2,font=font2, year=2023, month=11, day=30, background='darkblue', foreground='white', borderwidth=3)
    bdayCal.place(x=130,y=220)
    #probably needs changes, tried to make it have placeholer text 'dd/mm/yyyy' but i dont know how

    email_entry = customtkinter.CTkEntry(frame2,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='Email',placeholder_text_color='#a3a3a3',width=300,height=50)
    email_entry.place(x=70,y=275)

    password_entry = customtkinter.CTkEntry(frame2,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='Password',placeholder_text_color='#a3a3a3',width=300,height=50)
    password_entry.place(x=70,y=345)

    confPass_entry = customtkinter.CTkEntry(frame2,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_width=3,placeholder_text='Confirm password',placeholder_text_color='#a3a3a3',width=300,height=50)
    confPass_entry.place(x=70,y=415)

    gender_label = customtkinter.CTkLabel(frame2,font=font2,text='Gender:',text_color='#fff',bg_color='#001220')
    gender_label.place(x=190,y=480)

    genderVar = StringVar(app)
    genderVar.set("male") # default value
    gender_menu = OptionMenu(frame2, genderVar, "male", "female", "prefer not to say")
    gender_menu.place(x=185,y=520)
    #dropdown menu for gender, may need changes

    signup_btn = customtkinter.CTkButton(frame2,command=register,font=font2,text_color='#fff',text='Register',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    signup_btn.place(x=160,y=580)

frame1 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=470,height=360)
frame1.place(x=0,y=0)
#frame 1 = login or signup buttons

reg_label = customtkinter.CTkLabel(frame1,font=font1,text='Register',text_color='#fff',bg_color='#001220')
reg_label.place(x=165,y=20)

reg_label2 = customtkinter.CTkLabel(frame1,font=font2,text='would you like to',text_color='#fff',bg_color='#001220')
reg_label2.place(x=160,y=80)

loginPg_btn = customtkinter.CTkButton(frame1,command=loginPage,font=font3,text='Login',text_color='#fff')
loginPg_btn.place(x=160,y=120)

reg_label3 = customtkinter.CTkLabel(frame1,font=font2,text='or',text_color='#fff',bg_color='#001220')
reg_label3.place(x=220,y=190)

RegPg_btn = customtkinter.CTkButton(frame1,command=regPage,font=font3,text='Register',text_color='#fff')
RegPg_btn.place(x=160,y=250)

app.mainloop()
#runs program/window