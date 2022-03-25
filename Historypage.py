from tkinter import *
import Font,Homepage,Allhistorypage,Monthlyreportpage

def show(currentFrame,root):
    currentFrame.forget()

    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.pack(fill=BOTH,expand=TRUE)

    # create the widgets
    allHistoryButton = Button(middleFrame,text="History",height=2,width=40,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Allhistorypage.show(mainFrame,root))
    allHistoryButton.place(relx=.5,rely=.42,anchor=CENTER)

    monthlyReportButton = Button(middleFrame,text="Monthly Report",height=2,width=40,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Monthlyreportpage.show(mainFrame,root))
    monthlyReportButton.place(relx=.5,rely=.57,anchor=CENTER)

    homeButton = Button(middleFrame,text="Home",height=2,width=10,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Homepage.show(mainFrame,root))
    homeButton.place(relx=0,rely=1,anchor=SW)