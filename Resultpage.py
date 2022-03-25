from tkinter import *
from tkinter import ttk
import os,pandas as pd,seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Font,Homepage,Employee

def readResult(employeeID,specificMonth=0,specificYear=0):
    employees_base_dir = os.path.join('Program', 'Employees')
    dest_path = os.path.join(employees_base_dir, employeeID, 'history.txt')
    
    dateTimeList = []
    faceResultList = []
    voiceResultList = []
    
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

def createPlotForLatestResult(faceResult,voiceResult):
    # Recreating dataframe without datetime and separated by recognition type
    emotions = ['Angry','Happy','Neutral','Sad']
    dfFace = pd.DataFrame(columns=['Emotion','Emotion Recognition by Facial Expression'])
    dfVoice = pd.DataFrame(columns=['Emotion','Emotion Recognition by Voice'])
    c = 0

    for i,emo in enumerate(emotions):
        dfFace.loc[c] = [emo,faceResult[i]]
        dfVoice.loc[c] = [emo,voiceResult[i]]
        c+=1

    # Setting of graphs
    figure = Figure(figsize=(9,5))
    ax = figure.add_subplot(121)
    
    face = sns.barplot(x="Emotion",
                       y="Emotion Recognition by Facial Expression",
                       data=dfFace,
                       ax=ax)
    
    face.set_title("Emotion Recognition by Facial Expression")
    face.set_xlabel("Emotion")
    face.set_ylabel("Recognition Result")
    face.set(ylim=(0, 1.1))
    
    for p in face.patches:
        face.annotate(format(p.get_height(), '.4f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha = 'center', va = 'center',
                      xytext = (0, 4),
                      fontsize=10,
                      textcoords = 'offset points')

    ax = figure.add_subplot(122)
    voice = sns.barplot(x="Emotion",
                        y="Emotion Recognition by Voice",
                        data=dfVoice,
                        ax=ax)
    
    voice.set_title("Emotion Recognition by Voice")
    voice.set_xlabel("Emotion")
    voice.set_ylabel("Recognition Result")
    voice.set(ylim=(0, 1.1))
    
    for p in voice.patches:
        voice.annotate(format(p.get_height(), '.4f'),
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       xytext = (0, 4), 
                       fontsize=10,
                       textcoords = 'offset points')

    figure.tight_layout(pad=2.0)
    return figure

def displayGraph(event):
    selectedValue = event.widget.get()
    id = selectedValue.split(' - ')[0]
    
    dateTimeList,faceResultList,voiceResultList = readResult(id)
    figure = createPlotForLatestResult(faceResultList[-1],voiceResultList[-1])

    for widget in middleFrame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(figure, master=middleFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

def show(currentFrame,root,selectedValue):
    currentFrame.forget()

    # prepare the frames
    mainFrame = Frame(root,bg="peachpuff2")
    mainFrame.pack(fill=BOTH,expand=TRUE)

    topFrame = Frame(mainFrame,bg="peachpuff2")
    topFrame.pack(fill=X,side=TOP)

    global middleFrame
    middleFrame = Frame(mainFrame,bg="peachpuff2")
    middleFrame.pack(fill=BOTH,expand=TRUE)

    bottomFrame = Frame(mainFrame,bg="peachpuff2")
    bottomFrame.pack(fill=X)
    
    # create the widgets
    title = Label(topFrame,text="Recognition DONE. Please view the result.",bg="peachpuff2",font=Font.fontTitle)
    title.pack(pady=(50,10))

    if selectedValue == 'All employees':
        selection = StringVar()
        defaultValue = selection.get()
        list = Employee.getEmployeesIdList([])
        options = ttk.Combobox(topFrame,textvariable=defaultValue,values=list,state='readonly',width=40,height=10,font=Font.fontNormal)
        root.option_add('*TCombobox*Listbox.font', Font.fontNormal)
        options.current(0)
        options.pack(ipadx=75,ipady=20)
        options.bind("<<ComboboxSelected>>",displayGraph)
        id = list[0].split(' - ')[0]
    else:
        id = selectedValue.split(' - ')[0]

        emp = Employee.getEmployeeInfoById(id)
        idLabel = Label(topFrame,text=emp[0].id+" - "+emp[0].name,bg="white",font=Font.fontButton)
        idLabel.pack(ipadx=50,ipady=20)

    dateTimeList,faceResultList,voiceResultList = readResult(id)
    figure = createPlotForLatestResult(faceResultList[-1],voiceResultList[-1])

    canvas = FigureCanvasTkAgg(figure, master=middleFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)
    
    homeButton = Button(bottomFrame,text="Home",height=2,width=10,relief=FLAT,overrelief=SOLID,bg="white",font=Font.fontButton,command=lambda:Homepage.show(mainFrame,root))
    homeButton.pack(side=LEFT)