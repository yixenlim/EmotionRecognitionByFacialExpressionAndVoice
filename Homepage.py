from tkinter import *
import Font,Startpage,Historypage

root = Tk()
root.title("Emotion Detector")

def show(currentFrame,root):

    # check if it is the initiation of the application
    if currentFrame != None:
        currentFrame.forget() # remove the last frame
    
    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    topFrame = Frame(mainFrame,bg="peachpuff2")
    topFrame.pack(fill=X,side=TOP)

    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.pack(fill=BOTH,expand=TRUE)
    
    # create the widgets
    title = Label(topFrame,text="Emotion Recognition By Facial Expression And Voice",bg="peachpuff2",font=Font.fontTitle)
    title.pack(pady=(200,100))

    startButton = Button(middleFrame,text="Start",height=2,width=40,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Startpage.show(mainFrame,root))
    startButton.place(relx=.5,rely=.1,anchor=CENTER)

    historyButton = Button(middleFrame,text="History",height=2,width=40,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Historypage.show(mainFrame,root))
    historyButton.place(relx=.5,rely=.35,anchor=CENTER)

    exitButton = Button(middleFrame,text="Exit",height=2,width=40,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=root.destroy)
    exitButton.place(relx=.5,rely=.6,anchor=CENTER)

show(None,root)

root.attributes('-fullscreen', True)
root.mainloop()