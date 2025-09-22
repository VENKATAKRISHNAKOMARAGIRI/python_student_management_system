from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas


def iamexit():
    result=messagebox.askyesno('Confirm','Do You Want To Exit?')
    if  result:
        root.destroy()


def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studenttable.get_children()
    newlist=[]
    for index in indexing:
        content=studenttable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile Number','Email','Address','Gender','Date Of Birth','Added Data','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved Successfully')


def toplevel_data(title,button_text,command):
    global identry,phoneentry,nameentry,emailentry,addressentry,genderentry,dobentry,screen
    screen=Toplevel()
    screen.title(title)
    screen.resizable(False,False)
    screen.configure(bg="#F8F8FF")  # Light background

    idlabel=Label(screen,text='Id',font=('times new roman',20,'bold'),bg="#F8F8FF")
    idlabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    identry=Entry(screen,font=('roman',15,'bold'),width=24)
    identry.grid(row=0,column=1,padx=10,pady=15)

    namelabel=Label(screen,text='Name',font=('times new roman',20,'bold'),bg="#F8F8FF")
    namelabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameentry=Entry(screen,font=('roman',15,'bold'),width=24)
    nameentry.grid(row=1,column=1,padx=10,pady=15)

    phonelabel=Label(screen,text='Phone',font=('times new roman',20,'bold'),bg="#F8F8FF")
    phonelabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneentry=Entry(screen,font=('roman',15,'bold'),width=24)
    phoneentry.grid(row=2,column=1,padx=10,pady=15)

    emaillabel=Label(screen,text='Email',font=('times new roman',20,'bold'),bg="#F8F8FF")
    emaillabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailentry=Entry(screen,font=('roman',15,'bold'),width=24)
    emailentry.grid(row=3,column=1,padx=10,pady=15)

    addresslabel=Label(screen,text='Address',font=('times new roman',20,'bold'),bg="#F8F8FF")
    addresslabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressentry=Entry(screen,font=('roman',15,'bold'),width=24)
    addressentry.grid(row=4,column=1,padx=10,pady=15)

    genderlabel=Label(screen,text='Gender',font=('times new roman',20,'bold'),bg="#F8F8FF")
    genderlabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderentry=Entry(screen,font=('roman',15,'bold'),width=24)
    genderentry.grid(row=5,column=1,padx=10,pady=15)

    doblabel=Label(screen,text='Date Of Birth',font=('times new roman',20,'bold'),bg="#F8F8FF")
    doblabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobentry=Entry(screen,font=('roman',15,'bold'),width=24)
    dobentry.grid(row=6,column=1,padx=10,pady=15)

    student_button=ttk.Button(screen,text=button_text,command=command)
    student_button.grid(row=7,columnspan=2,pady=15)

    if title=='Update Student':
        indexing=studenttable.focus()
        content=studenttable.item(indexing)
        listdata=content['values']
        identry.insert(0,listdata[0])
        nameentry.insert(0,listdata[1])
        phoneentry.insert(0,listdata[2])
        emailentry.insert(0,listdata[3])
        addressentry.insert(0,listdata[4])
        genderentry.insert(0,listdata[5])
        dobentry.insert(0,listdata[6])


def update_data():
    query='update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,DateOfBirth=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameentry.get(),phoneentry.get(),emailentry.get(),addressentry.get(),genderentry.get(),dobentry.get(),date,currenttime,identry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id{identry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_student()

def show_student():
    query='select *from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())
    for index, data in enumerate(fetched_data):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        studenttable.insert('',END,values=data,tags=(tag,))

def delete_student():
    indexing=studenttable.focus()
    content=studenttable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,(content_id))
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is Deleted Successfully')
    show_student()

def search_data():
    query='select * from student where id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or DateOfBirth=%s'
    mycursor.execute(query,(identry.get(),nameentry.get(),phoneentry.get(),emailentry.get(),addressentry.get(),genderentry.get(),dobentry.get()))
    studenttable.delete(*studenttable.get_children())
    fetched_data=mycursor.fetchall()
    for index, data in enumerate(fetched_data):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        studenttable.insert('',END,values=data,tags=(tag,))

def add_data():
    if identry.get()==''or nameentry.get()=='' or phoneentry.get()=='' or emailentry.get()=='' or addressentry.get()=='' or genderentry.get()=='' or dobentry.get()=='':
        messagebox.showerror('Error','All Fields Are Required',parent=screen)
    else:
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(identry.get(),nameentry.get(),phoneentry.get(),emailentry.get(),addressentry.get(),genderentry.get(),dobentry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('confirm','Data Added Successfully. Do You Want Clean The Form?',parent=screen)
            if result:
                identry.delete(0,END)
                nameentry.delete(0,END)
                phoneentry.delete(0,END)
                emailentry.delete(0,END)
                addressentry.delete(0,END)
                genderentry.delete(0,END)
                dobentry.delete(0,END)
        except:
            messagebox.showerror('Error','Id Cannot be Repeated',parent=screen)
            return
        show_student()

def connect_database():
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host=hostentry.get(),user=usernameentry.get(),password=passwordentry.get())
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Invalid Details',parent=connectwindow)
            return
        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query='use studentmanagementsystem'
            mycursor.execute(query)
            query='create table student(id int not null primary key ,name varchar(50),mobile varchar(50),email varchar(50),address varchar(100),gender varchar(20),DateOfBirth varchar(20),date varchar(50),Time varchar(50))'
            mycursor.execute(query)
        except:
            query='use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success','Database Connection is Successful',parent=connectwindow)
        connectwindow.destroy()
        for btn in [addstudentbutton, searchstudentbutton, updatestudentbutton, showstudentbutton, exportstudentbutton, deletestudentbutton, exitbutton]:
            btn.config(state=NORMAL)

    connectwindow=Toplevel()
    connectwindow.grab_set()
    connectwindow.geometry('470x250+682+230')
    connectwindow.title('Database Connection')
    connectwindow.resizable(0,0)

    hostnamelabel=Label(connectwindow,text='Host Name',font=('arial',20,'bold'))
    hostnamelabel.grid(row=0,column=0,padx=20)
    hostentry=Entry(connectwindow,font=('roman',15,'bold'),bd=2)
    hostentry.grid(row=0,column=1,padx=40,pady=20)

    usernamelabel=Label(connectwindow,text='User Name',font=('arial',20,'bold'))
    usernamelabel.grid(row=1,column=0,padx=20)
    usernameentry=Entry(connectwindow,font=('roman',15,'bold'),bd=2)
    usernameentry.grid(row=1,column=1,padx=40,pady=20)

    passwordlabel=Label(connectwindow,text='Password',font=('arial',20,'bold'))
    passwordlabel.grid(row=2,column=0,padx=20)
    passwordentry=Entry(connectwindow,font=('roman',15,'bold'),bd=2)
    passwordentry.grid(row=2,column=1,padx=40,pady=20)

    connectButton=ttk.Button(connectwindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)


count=0
text=''

def slider():
    global text,count
    if count==len(S):
        count=0
        text=''
    text=text+S[count]
    SliderLabel.config(text=text)
    count+=1
    SliderLabel.after(300,slider)

def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date:{date}\nTime:{currenttime}')
    datetimeLabel.after(1000,clock)


def gradient_background(window, color1, color2):
    canvas = Canvas(window, width=1174, height=680, highlightthickness=0)
    canvas.place(x=0,y=0)
    for i in range(0,680):
        r1,g1,b1 = window.winfo_rgb(color1)
        r2,g2,b2 = window.winfo_rgb(color2)
        r = int(r1 + (r2-r1)*i/680) >> 8
        g = int(g1 + (g2-g1)*i/680) >> 8
        b = int(b1 + (b2-b1)*i/680) >> 8
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0,i,1174,i,fill=hex_color)


root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('System Management System')


gradient_background(root,"#89CFF0","#E6E6FA")


datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

S='Student Management system'
SliderLabel=Label(root,text=S,font=('arial',28,'italic bold'),width=30)
SliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect Database',command=connect_database)
connectButton.place(x=980,y=0)


leftframe=Frame(root,bg="#DCDCDC",bd=5,relief="ridge")
leftframe.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='graduates.png')
logo_Label=Label(leftframe,image=logo_image)
logo_Label.grid(row=0,column=0)

addstudentbutton=ttk.Button(leftframe,text='Add Student',width=22,state=DISABLED,command=lambda:toplevel_data('Add Student','Add',add_data))
addstudentbutton.grid(row=1,column=0,pady=20)

searchstudentbutton=ttk.Button(leftframe,text='Search Student',width=22,state=DISABLED,command=lambda:toplevel_data('Search Student','Search',search_data))
searchstudentbutton.grid(row=2,column=0,pady=20)

deletestudentbutton=ttk.Button(leftframe,text='Delete Student',width=22,state=DISABLED,command=delete_student)
deletestudentbutton.grid(row=3,column=0,pady=20)

updatestudentbutton=ttk.Button(leftframe,text='Update Student',width=22,state=DISABLED,command=lambda:toplevel_data('Update Student','Update',update_data))
updatestudentbutton.grid(row=4,column=0,pady=20)

showstudentbutton=ttk.Button(leftframe,text='Show Student',width=22,state=DISABLED,command=show_student)
showstudentbutton.grid(row=5,column=0,pady=20)

exportstudentbutton=ttk.Button(leftframe,text='Export Data',width=22,state=DISABLED,command=export_data)
exportstudentbutton.grid(row=6,column=0,pady=20)

exitbutton=ttk.Button(leftframe,text='Exit',width=22,state=DISABLED,command=iamexit)
exitbutton.grid(row=7,column=0,pady=20)

rightframe=Frame(root,bg="#F5F5F5",bd=5,relief="groove")
rightframe.place(x=350,y=80,width=820,height=600)

Scrollbarx=Scrollbar(rightframe,orient=HORIZONTAL)
Scrollbary=Scrollbar(rightframe,orient=VERTICAL)

studenttable=ttk.Treeview(rightframe,columns=('Id','Name','MobileNumber','Email','Address','Gender','Date Of Birth','Added Data','Added Time'),xscrollcommand=Scrollbarx.set,yscrollcommand=Scrollbary.set)

Scrollbarx.config(command=studenttable.xview)
Scrollbary.config(command=studenttable.yview)

Scrollbarx.pack(side=BOTTOM,fill=X)
Scrollbary.pack(side=RIGHT,fill=Y)

studenttable.pack(fill=BOTH,expand=1)

studenttable.heading('Id',text='Id')
studenttable.heading('Name',text='Name')
studenttable.heading('MobileNumber',text='MobileNumber')
studenttable.heading('Email',text='Email')
studenttable.heading('Address',text='Address')
studenttable.heading('Gender',text='Gender')
studenttable.heading('Date Of Birth',text='Date of Birth')
studenttable.heading('Added Data',text='Added Data')
studenttable.heading('Added Time',text='Added Time')

studenttable.column('Id',width=80,anchor=CENTER)
studenttable.column('Name',width=300,anchor=CENTER)
studenttable.column('MobileNumber',width=200,anchor=CENTER)
studenttable.column('Email',width=300,anchor=CENTER)
studenttable.column('Address',width=300,anchor=CENTER)
studenttable.column('Gender',width=200,anchor=CENTER)
studenttable.column('Date Of Birth',width=200,anchor=CENTER)
studenttable.column('Added Data',width=200,anchor=CENTER)
studenttable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12,'bold'),foreground='black',background='grey',fieldbackground='grey')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='red')

studenttable.config(show='headings')


studenttable.tag_configure('oddrow', background="#E6E6FA")
studenttable.tag_configure('evenrow', background="#F0F8FF")


def on_enter(e):
    e.widget['background'] = "#FFB6C1"

def on_leave(e):
    e.widget['background'] = "SystemButtonFace"

for btn in [addstudentbutton, searchstudentbutton, deletestudentbutton, updatestudentbutton, showstudentbutton, exportstudentbutton, exitbutton]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root.mainloop()
