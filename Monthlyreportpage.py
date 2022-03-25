from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os,pandas as pd,seaborn as sns,numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

def displayMonthlyReport(dfHistoryGraph):
    # Generating dataframes
    dfFace = dfHistoryGraph[['Datetime','Emotion','ER by Facial Expression']].groupby(['Datetime', 'Emotion']).sum().reset_index()
    dfVoice = dfHistoryGraph[['Datetime','Emotion','ER by Voice']].groupby(['Datetime', 'Emotion']).sum().reset_index()
    
    # Setting
    sns.set(font_scale = 0.8)
    figure = Figure(figsize=(15,5))
    ax = figure.add_subplot(121)

    face = sns.barplot(x="Datetime",
                       y="ER by Facial Expression",
                       hue="Emotion",
                       data=dfFace,
                       ax=ax,
                       palette='Pastel2')

    face.set_title("Emotion Recognition by Facial Expression")
    face.set_xlabel("Datetime")
    face.set_ylabel("Recognition Result")
    face.legend(loc='upper left',bbox_to_anchor=(1, 1),title='Emotion',fontsize='small',borderaxespad=0)
    face.set(ylim=(0, 1))
    
    for p in face.patches:
        face.annotate(format(p.get_height(), '.2f'), 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       xytext = (0, 4), 
                       textcoords = 'offset points',
                      fontsize=8)

    ax = figure.add_subplot(122)
    voice = sns.barplot(x="Datetime",
                        y="ER by Voice",
                        hue="Emotion",
                        data=dfVoice,
                        ax=ax,
                        palette='Pastel2')

    voice.set_title("Emotion Recognition by Voice")
    voice.set_xlabel("Datetime")
    voice.set_ylabel("Recognition Result")
    voice.legend(loc='upper left',bbox_to_anchor=(1, 1),title='Emotion',fontsize='small',borderaxespad=0)
    voice.set(ylim=(0, 1))
    
    for p in voice.patches:
        voice.annotate(format(p.get_height(), '.2f'), 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       xytext = (0, 4), 
                       textcoords = 'offset points',
                       fontsize=8)
        
    figure.tight_layout(pad=2.0)
    return figure

def getRecentHistoryDataFrame(dateTimeList,faceResultList,voiceResultList):
    emotions = ['Angry','Happy','Neutral','Sad']
    df = pd.DataFrame(columns=['Datetime','Emotion','ER by Facial Expression','ER by Voice'])
    c = 0
    
    for i,dateTime in enumerate(dateTimeList):
        for j,emo in enumerate(emotions):
            df.loc[c] = [dateTime,emo,faceResultList[i][j],voiceResultList[i][j]]
            c+=1
    
    return df

def checking():
    year = yearOptions.get()
    month = monthOptions.get()
    employee = employeeOptions.get()

    if year == 'Year' or month == 'Month' or employee == 'Employee':
        tkinter.messagebox.showerror("Error",'Please select the year, month and employee.')
    else:
        for widget in inMiddleFrame.winfo_children():
            widget.destroy()

        dateTimeList,faceResultList,voiceResultList = readResult(employee.split(' - ')[0],int(month),int(year))

        if (len(dateTimeList) == 0):
            noHistoryLabel = Label(inMiddleFrame,text="No history for this employee.",bg="peachpuff2",font=Font.fontTitle)
            noHistoryLabel.place(relx=.5,rely=.6,anchor=CENTER)
        else:
            dfHistoryGraph = getRecentHistoryDataFrame(dateTimeList,faceResultList,voiceResultList)
            figure = displayMonthlyReport(dfHistoryGraph)
            
            canvas = FigureCanvasTkAgg(figure, master=inMiddleFrame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

def show(currentFrame,root):
    currentFrame.forget()

    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    topFrame = Frame(mainFrame,bg="peachpuff2")
    topFrame.pack(fill=X,side=TOP)

    buttonFrame = Frame(topFrame,bg="peachpuff2")
    buttonFrame.pack(padx=70,pady=10,side=BOTTOM)#fill=X

    # global middleFrame
    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.pack(fill=BOTH,expand=TRUE)

    global inMiddleFrame
    inMiddleFrame = Frame(middleFrame,bg="peachpuff2",width=820,height=400)
    inMiddleFrame.pack(pady=10)

    bottomFrame = Frame(mainFrame,bg="peachpuff2")
    bottomFrame.pack(fill=X,side=BOTTOM)
    
    # create the widgets
    title = Label(topFrame,text="Please select the year, month and employee.",bg="peachpuff2",font=Font.fontTitle)
    title.pack(pady=(50,0))

    global yearOptions,monthOptions,employeeOptions

    yearDefaultValue = StringVar().get()
    yearList = np.arange(2022,2030).tolist()
    yearList.insert(0,'Year')
    yearOptions = ttk.Combobox(buttonFrame,textvariable=yearDefaultValue,values=yearList,state='readonly',width=20,height=10,font=Font.fontNormal)
    yearOptions.current(0)
    yearOptions.pack(ipadx=20,ipady=15,side=LEFT)

    monthDefaultValue = StringVar().get()
    monthList = np.arange(1,13).tolist()
    monthList.insert(0,'Month')
    monthOptions = ttk.Combobox(buttonFrame,textvariable=monthDefaultValue,values=monthList,state='readonly',width=20,height=10,font=Font.fontNormal)
    monthOptions.current(0)
    monthOptions.pack(ipadx=20,ipady=15,side=LEFT)

    employeeDefaultValue = StringVar().get()
    employeeList = Employee.getEmployeesIdList(['Employee'])
    employeeOptions = ttk.Combobox(buttonFrame,textvariable=employeeDefaultValue,values=employeeList,state='readonly',width=40,height=10,font=Font.fontNormal)
    root.option_add('*TCombobox*Listbox.font', Font.fontNormal)
    employeeOptions.current(0)
    employeeOptions.pack(ipadx=50,ipady=15,side=LEFT)

    emptyLabel = Label(buttonFrame,text="     ",bg="peachpuff2",font=Font.fontTitle)
    emptyLabel.pack(side=LEFT)

    viewButton = Button(buttonFrame,text="View",height=1,width=10,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=checking)
    viewButton.pack(side=RIGHT)

    homeButton = Button(bottomFrame,text="Home",height=2,width=10,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Homepage.show(mainFrame,root))
    homeButton.pack(side=LEFT)
