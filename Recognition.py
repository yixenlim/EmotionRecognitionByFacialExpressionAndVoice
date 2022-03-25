from tkinter import *
import tkinter.messagebox
import librosa,numpy as np,pandas as pd
import os,math,shutil,cv2,keras
from datetime import datetime
from moviepy.editor import *
from pydub import AudioSegment
from pickle import load
import Employee

def loadModels():
    # Load the cascade
    faceDetector = cv2.dnn.readNetFromCaffe(os.path.join('Program','Models','deploy.prototxt.txt'),os.path.join('Program','Models','res10_300x300_ssd_iter_140000.caffemodel'))
    
    # Face model
    loaded_model_face = keras.models.load_model(os.path.join('Program','Models','faceModel629-self.h5'))
    
    # Voice model
    loaded_model_voice = keras.models.load_model(os.path.join('Program','Models','voiceModel-aug-mel823.h5'))
    
    # load the scaler
    scaler = load(open(os.path.join('Program','Models','scaler.pkl'), 'rb'))
    
    return faceDetector,loaded_model_face,loaded_model_voice,scaler

def getVideoPaths(employeeList,root):
    videos_base_dir = os.path.join('Program', 'Devices')
    videoPaths = []
    
    for emp in employeeList:
        path = os.path.join(videos_base_dir, emp.id)
        
        if len(os.listdir(path)) == 0:
            errorMessage = 'No videos found in',path,'. Please insert video(s)'
            tkinter.messagebox.showerror("Error",errorMessage)
            # print('No videos found in',path,'. Please insert video(s)')
            root.destroy()
        else:
            videoPath = os.path.join(path, os.listdir(path)[0])
            videoPaths.append(videoPath)
    return videoPaths

def extractFrames(path):
    video = cv2.VideoCapture(path)
    
    frameRate = video.get(5) #frame rate
    extractedFrames = []

    while(video.isOpened()):
        frameId = video.get(1) #current frame number
        ret, frame = video.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0): #every second save the first frame
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            extractedFrames.append(rgbImage)
    video.release()

    return extractedFrames

def getCroppedFaceRegions(frames,faceDetector):
    cropped = []
    
    for frame in frames:
        # Detect faces
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
        faceDetector.setInput(blob)
        faces = faceDetector.forward()

        try:
            for i in range(faces.shape[2]):
                confidence = faces[0, 0, i, 2]
                if confidence > 0.7:
                    box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (x1, y1, x2, y2) = box.astype("int")
                    face_rgb = frame[y1:y2,x1:x2]
                    cropped.append(cv2.resize(face_rgb,(48,48)))

        except cv2.error as e:
            print('[Unknown error] Invalid face!')
        
    return cropped

def faceRecog(faces,model):
    result = []
    
    for face in faces:
        img = face.astype('float32') / 255.0
        img = img.reshape(-1, 48, 48, 1)
        result.append(model.predict(img)[0])
    
    faceTotal = len(result)
    finalFaceResult = []
    
    #calculate for each emotion (since the fps of each video might be different)
    for i in range(4): 
        sumEmotion = 0
        for res in result:
            sumEmotion += res[i]
        finalFaceResult.append(sumEmotion/faceTotal)
    
    # Round up to 4 decimal places
    finalFaceResult = [np.round(num, 4) for num in finalFaceResult]
    
    return finalFaceResult

def extractAudio(path):
    destinationFolder = 'Extracted audio'
    destAudio = os.path.join(destinationFolder,'audio.wav')
    
    # Create directory if no such directory
    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)
    
    # Extract audio from the video
    video = VideoFileClip(path)
    video.audio.write_audiofile(destAudio, logger=None)
    video.close()
    
    # Delete the video
    os.remove(path)
    
    # Convert to mono channel
    sound = AudioSegment.from_wav(destAudio)
    sound = sound.set_channels(1)
    
    # Extract audio for every 3 seconds
    length = int(sound.duration_seconds)    
    num = int(length/3)
    audioList = []
    
    for i in range(num):
        dest = os.path.join(destinationFolder,str(i+1)+'.wav')
        crop_file = sound[(i*3)*1000:]
        crop_file.export(dest, format='wav')
        
        # Read in again with desired format and library
        X, sample_rate = librosa.load(dest, duration=3, res_type='kaiser_fast',sr=44100,offset=0.5)
        audioList.append(X)

    # Delete the directory and the audio inside it
    if os.path.exists(destinationFolder):
        shutil.rmtree(destinationFolder)
    
    return audioList, sample_rate

def getMelSpect(audioList, sample_rate):
    dfAudio = pd.DataFrame()
    
    for X in audioList:
        df = pd.DataFrame(columns=['mel_spectrogram'])
        
        #get the mel-scaled spectrogram (ransform both the y-axis (frequency) to log scale, and the “color” axis (amplitude) to Decibels, which is kinda the log scale of amplitudes.)
        spectrogram = librosa.feature.melspectrogram(y=X, sr=sample_rate, n_mels=128,fmax=8000) 
        db_spec = librosa.power_to_db(spectrogram)

        #temporally average spectrogram
        log_spectrogram = np.mean(db_spec, axis = 0)
        df.loc[0] = [log_spectrogram]

        df = pd.DataFrame(df['mel_spectrogram'].values.tolist())
        dfAudio = pd.concat([dfAudio,df])
        
    return dfAudio

def voiceRecog(dfAudio,model,scaler):
    # NORMALIZE DATA
    df = pd.DataFrame(scaler.transform(dfAudio))
    df = np.array(df)
    df = df.reshape(-1,259,1)
    
    result = model.predict(df).tolist()
    
    voiceTotal = len(result)
    finalVoiceResult = []
    
    #calculate for each emotion (since the fps of each video might be different)
    for i in range(4): 
        sumEmotion = 0
        for res in result:
            sumEmotion += res[i]
        finalVoiceResult.append(sumEmotion/voiceTotal)
    
    # Round up to 4 decimal places
    finalVoiceResult = [np.round(num, 4) for num in finalVoiceResult]

    return finalVoiceResult

def saveResult(now,employeeID,faceResult,voiceResult):
    employees_base_dir = os.path.join('Program', 'Employees')
    dest_path = os.path.join(employees_base_dir, employeeID, 'history.txt')
    
    with open(dest_path,'a+') as textFile:
        textFile.write(now.strftime("%d-%m-%Y(%H:%M:%S)")+'_')
        textFile.write(str(faceResult)[1 : -1].replace(" ", "")+'_')
        textFile.write(str(voiceResult)[1 : -1].replace(" ", "")+'\n')# Newline for future result

def run(selectedValue,root,progress,percentage):
    # faceResultList = []
    # voiceResultList = []
    faceDetector,modelFace,modelVoice,scaler = loadModels()

    if selectedValue == 'All employees':
        employeeList = Employee.getEmployeesInfo()
    else:
        id = selectedValue.split(' - ')[0]
        employeeList = Employee.getEmployeeInfoById(id)

    # get the video path list and close the window if video not found
    videoPathList = getVideoPaths(employeeList,root)
    
    for i,emp in enumerate(employeeList):
        frames = extractFrames(videoPathList[i])
        cropped = getCroppedFaceRegions(frames,faceDetector)
        faceResult = faceRecog(cropped,modelFace)
        # faceResultList.append(faceResult)
        
        audioList, sample_rate = extractAudio(videoPathList[i])
        mel = getMelSpect(audioList, sample_rate)
        voiceResult = voiceRecog(mel,modelVoice,scaler)
        # voiceResultList.append(voiceResult)

        now = datetime.now()
        saveResult(now,emp.id,faceResult,voiceResult)

        formatted_float = "{:.2f}".format((i+1)/len(employeeList)*100)
        root.update_idletasks()
        progress['value'] = formatted_float
        formatted_float = "  " + formatted_float + "%"
        formatted_float.replace("{","").replace("}","")
        percentage['text'] = formatted_float