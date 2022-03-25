from tkinter import *
from tkinter import ttk
import Font,Homepage,Employee,Recognitionpage

def show(currentFrame,root):
    currentFrame.forget()

    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    topFrame = Frame(mainFrame,bg="peachpuff2")
    topFrame.pack(fill=X,side=TOP)

    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.pack(fill=BOTH,expand=TRUE)
    
    # create the widgets
    title = Label(topFrame,text="Please select an employee or select all.",bg="peachpuff2",font=Font.fontTitle)
    title.pack(pady=(200,100))

    selection = StringVar()
    defaultValue = selection.get()
    list = Employee.getEmployeesIdList(['All employees'])
    options = ttk.Combobox(middleFrame,textvariable=defaultValue,values=list,state='readonly',width=40,height=10,font=Font.fontNormal)
    options.set('All employees') 
    root.option_add('*TCombobox*Listbox.font', Font.fontNormal)
    options.pack(ipady=20,ipadx=75)
    
    recognitionButton = Button(middleFrame,text="Start recognition",height=2,width=40,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Recognitionpage.show(mainFrame,root,options.get()))
    recognitionButton.place(relx=.5,rely=.35,anchor=CENTER)

    homeButton = Button(middleFrame,text="Home",height=2,width=10,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Homepage.show(mainFrame,root))
    homeButton.place(relx=0,rely=1,anchor=SW)
