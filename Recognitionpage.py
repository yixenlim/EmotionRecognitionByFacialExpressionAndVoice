from tkinter import *
from tkinter import ttk
import Font,Recognition,Resultpage
import time
from threading import Thread

def startRecognition(currentFrame,root,selectedValue,progress,percentage):
    Recognition.run(selectedValue,root,progress,percentage)
    time.sleep(2)
    # root.destroy()
    #####change page#####
    Resultpage.show(currentFrame,root,selectedValue)

def show(currentFrame,root,selectedValue):
    currentFrame.forget()

    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    topFrame = Frame(mainFrame,bg="peachpuff2")
    topFrame.pack(fill=X,side=TOP)

    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.place(relx=.5,rely=.55,anchor=CENTER)

    # place the widgets
    title = Label(topFrame,text="Recognition in process...",bg="peachpuff2",font=Font.fontTitle)
    title.pack(pady=(300,100))

    progress = ttk.Progressbar(middleFrame, orient=HORIZONTAL,length=100, mode='determinate')
    progress.grid(row=0,column=0,ipadx=300,ipady=30)

    percentage = Label(middleFrame,text="  0.00%",bg="peachpuff2",font=Font.fontButton)
    percentage.grid(row=0,column=1)
    
    th = Thread(target=startRecognition, args=[mainFrame,root,selectedValue,progress,percentage],daemon = True)
    th.start()
