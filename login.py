from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get()=='' or PasswordEntry.get()=='':
        messagebox.showerror('Error','Fields cannot be Empty')

    elif usernameEntry.get()=='Harish' and PasswordEntry.get()=='1234':
        messagebox.showinfo('Success','Welcome')
        window.destroy()
        import student_management_ui
        

    else:
        messagebox.showerror('Error','Please Enter Correct Credentials')

window=Tk()
window.geometry('1280x700+0+0')
window.title('Login System Of Student Management System')
window.resizable(False,False)
backgroundImage = ImageTk.PhotoImage(file='background.jpg')

bgLabel=Label(window,image=backgroundImage)
bgLabel.place(x=0,y=0)



loginFrame=Frame(window,bg='grey')
loginFrame.place(x=400,y=150)


logoimage=PhotoImage(file='students.png')

logoLabel=Label(loginFrame,image=logoimage)

logoLabel.grid(row=0,column=0,columnspan=2,pady=10)

usernameimage=PhotoImage(file='user.png')
usernamelabel=Label(loginFrame,image=usernameimage,text='Username',compound=LEFT,font=('times new roman',20,'bold'),bg='grey')
usernamelabel.grid(row=1,column=0,pady=10,padx=20)
usernameEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
usernameEntry.grid(row=1,column=1,pady=10,padx=20)

Passwordimage=PhotoImage(file='password.png.png')
Passwordlabel=Label(loginFrame,image=Passwordimage,text='Password',compound=LEFT,font=('times new roman',20,'bold'),bg='grey')
Passwordlabel.grid(row=2,column=0,pady=10,padx=20)
PasswordEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
PasswordEntry.grid(row=2,column=1,pady=10,padx=20)


Loginbutton=Button(loginFrame,text='Login',font=('times new roman',14,'bold'),width=15,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',activeforeground='white',cursor='hand2',command=login)

Loginbutton.grid(row=3,column=1,pady=10)

window.mainloop()
