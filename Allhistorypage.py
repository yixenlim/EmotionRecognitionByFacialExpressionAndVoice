from tkinter import *
from tkinter import ttk
import os,pandas as pd,seaborn as sns,pandastable as pdtb
import Font,Homepage,Employee

def readResult(employeeID,specificMonth=0,specificYear=0):
    employees_base_dir = os.path.join('Program', 'Employees')
    dest_path = os.path.join(employees_base_dir, employeeID, 'history.txt')
    
    dateTimeList = []
    faceResultList = []
    voiceResultList = []
    
    if os.path.exists(dest_path):
        with open(dest_path,'r') as textFile:
            lines = textFile.readlines()
            for line in lines:
                items = line.split('_')
                
                dateTime = items[0]
                month = int(items[0].split('-')[1])
                year = int(items[0].split('(')[0].split('-')[2])
                
                # Only display when the employee want to view all history or monthly report
                if specificMonth == 0 or (specificMonth == month and specificYear == year):
                    faceResult = items[1].split(',')
                    faceResult = list(map(float, faceResult))

                    voiceResult = items[2].replace('\n','').split(',')
                    voiceResult = list(map(float, voiceResult))
                    
                    dateTimeList.append(dateTime)
                    faceResultList.append(faceResult)
                    voiceResultList.append(voiceResult)
                    
    return dateTimeList,faceResultList,voiceResultList

def getRecentHistoryDataFrame(dateTimeList,faceResultList,voiceResultList):
    erList = ['ER by Facial Expression','ER by Voice']
    df = pd.DataFrame(columns=['Datetime','ER Result','Angry','Happy','Neutral','Sad'])
    c = 0
    
    for i,dateTime in enumerate(dateTimeList):
        for er in erList:
            if c%2 == 0:
                dt = dateTime
                df.loc[c] = [dt,er,faceResultList[i][0],faceResultList[i][1],faceResultList[i][2],faceResultList[i][3]]
            else:
                df.loc[c] = ["",er,voiceResultList[i][0],voiceResultList[i][1],voiceResultList[i][2],voiceResultList[i][3]]
            c+=1
    
    # Convert result to string so that all the decimal places will be shown
    df['Angry'] = df['Angry'].astype(str)
    df['Happy'] = df['Happy'].astype(str)
    df['Neutral'] = df['Neutral'].astype(str)
    df['Sad'] = df['Sad'].astype(str)
    
    return df

def displayGraph(event):
    selectedValue = event.widget.get()
    id = selectedValue.split(' - ')[0]
    dateTimeList,faceResultList,voiceResultList = readResult(id)

    for widget in inMiddleFrame.winfo_children():
        widget.destroy()

    # no hostory for this employee
    if len(dateTimeList) == 0:
        noHistoryLabel = Label(inMiddleFrame,text="No history for this employee.",bg="peachpuff2",font=Font.fontTitle)
        noHistoryLabel.place(relx=.5,rely=.5,anchor=CENTER)
    else:
        dfHistoryDisplay = getRecentHistoryDataFrame(dateTimeList,faceResultList,voiceResultList)
        pt = pdtb.Table(inMiddleFrame, dataframe=dfHistoryDisplay, editable=False,width=820,height=600)
        pt.show()

def show(currentFrame,root):
    currentFrame.forget()

    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    topFrame = Frame(mainFrame,bg="peachpuff2")
    topFrame.pack(fill=X,side=TOP)

    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.pack(fill=BOTH,expand=TRUE)

    global inMiddleFrame
    inMiddleFrame = Frame(middleFrame,bg="peachpuff2",width=820,height=600)
    inMiddleFrame.pack(pady=20)

    bottomFrame = Frame(mainFrame,bg="peachpuff2")
    bottomFrame.pack(fill=X)

    # create the widgets
    selection = StringVar()
    defaultValue = selection.get()
    list = Employee.getEmployeesIdList([])
    options = ttk.Combobox(topFrame,textvariable=defaultValue,values=list,state='readonly',width=40,height=10,font=Font.fontNormal)
    root.option_add('*TCombobox*Listbox.font', Font.fontNormal)
    options.current(0)
    options.pack(ipadx=75,ipady=20,pady=(30,0))
    options.bind("<<ComboboxSelected>>",displayGraph)

    id = list[0].split(' - ')[0]
    dateTimeList,faceResultList,voiceResultList = readResult(id)

    # no history for this id
    if len(dateTimeList) == 0:
        noHistoryLabel = Label(inMiddleFrame,text="No history for this employee.",bg="peachpuff2",font=Font.fontTitle)
        noHistoryLabel.place(relx=.5,rely=.5,anchor=CENTER)
    else:
        dfHistoryDisplay = getRecentHistoryDataFrame(dateTimeList,faceResultList,voiceResultList)
        pt = pdtb.Table(inMiddleFrame, dataframe=dfHistoryDisplay, editable=False,width=820,height=600)
        pt.show()

    homeButton = Button(bottomFrame,text="Home",height=2,width=10,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Homepage.show(mainFrame,root))
    homeButton.pack(side=LEFT)