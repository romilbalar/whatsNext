import sqlite3
from tabula import read_pdf
from playsound import playsound #pip install playsound
from kivy.app import App
import speech_recognition as sr
import pyttsx3
import pandas
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '350')
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

r=sr.Recognizer()
class WidgetApp(BoxLayout):
   
    def whats_next(self):
        # playsound("whatsNext.mp3")
        from datetime import date
        import time

        today= date.today()
        
        # weekDayArray=('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
        self.day=today.weekday()              	

        t = time.localtime()
        time = time.strftime("%H:%M", t)
        # lst=currentTime.split(":")
        # lst[0]=int(lst[0])%12
        # lst[0]= str(lst[0])
        # time="".join(lst)

        self.getSchedule(time)
        self.schedule=str(int(self.schedule) + 1)
        self.getLecture()       


    
    def voice(self):        
        playsound("voice.mp3")
        with sr.Microphone() as source:
            audio = r.listen(source)            

        try:
            query = r.recognize_google(audio)        
            print(query)
            dayTemp,timeTemp="",""
            flag=0
            query=query.upper()
            lst=query.split()
            for word in lst:
                if word.endswith('DAY'):
                    
                    dayTemp=word
                    if flag==1:
                        break
                    flag=1
                if ':' in word or word.isnumeric():
                    timeTemp=word
                    if flag==1:
                        break
                    flag=1

            # if dayTemp=="":

            days = {"MONDAY":0,"TUESDAY":1,"WEDNESDAY":2,"THURSDAY":3,"FRIDAY":4,"SATURDAY":5}
            self.day = days[dayTemp]
            # print(day)
            self.getSchedule(timeTemp)
            self.getLecture()
        except:
            print("No class found")
                
            
        
    def returnQuery(self,lecture):
        # dictionary = {"LUNCH:":"LUNCH","BREAK":"BREAK","NaN":"BREAK","PYTHON":"PYTHON","SE":"SOFTWARE ENGINEERING","CN":"COMPUTER NETWORKS","IOT":"INTERNET OF THINGS","ADA":"ADA","ADA LAB":"ADA LAB","IOT / CN LAB":"IOT / CN LAB"}
        engine = pyttsx3.init()
        if lecture is None or self.day is None or self.schedule is None:
            lecture="Please repeat" #change
        engine.say(lecture)
        engine.setProperty('rate',120)  #120 words per minute
        engine.setProperty('volume',0.9) 
        engine.runAndWait()

    def getSchedule(self,query):
            
            
            if ':' in query:
                    
                    lst=query.split(":")
                    
                    lst[0]=int(lst[0])%12
                    
                    lst[0]= str(lst[0])
                    
                    text="".join(lst)   
            else:
                text= query   
        
            
            if int(text) in (range(810,855) or range(81,90)) or "8" == text:
                self.schedule = 1
            elif int(text) in (range(855,950) or range(91,100)) or "9" == text:
                self.schedule = 2
            elif int(text) in (range(950,1045) or range(101,110)) or "10" == text:
                self.schedule = 3
            elif int(text) in (range(1045,1115) or range(111,120)) or "11" == text:
                self.schedule = 4
            elif int(text) in (range(1115,1210) or range(121,130)) or "12" == text:
                self.schedule = 5
            elif int(text) in (range(1210,1260) or range(10,16)) or "1" == text:
                self.schedule = 6
            elif int(text) in (range(15,20) or range(110,160)):
                self.schedule = 7
            elif int(text) in (range(210,255) or range(21,30)) or "2" == text:
               self.schedule = 8
            elif int(text) in (range(255,350) or range(31,40)) or "3" == text:
                self.schedule = 9
            else:
                self.schedule=None

            self.schedule=str(self.schedule)
    def getLecture(self):
        lecture = None
        self.day=str(self.day)
        print(self.schedule ,self.day)
        if self.day is None or self.schedule is None:
            print("Day or schedule not mentioned")
            return
        query = "SELECT Schedule"+self.schedule+" from TimeTable WHERE Day = "+self.day+";"
        lecture = cur.execute(query)
        lecture= lecture.fetchall()
        lecture=lecture[0]
        print(lecture)
        self.returnQuery(lecture)


class WhatsNextApp(App):
    def build(self):
        return WidgetApp()
#initialisation code to read the PDF and get the DATABASE READY
df = read_pdf("TimeTable1.pdf")

df.columns = [0,1,2,3,4,5,6,7,8,9]
conn = sqlite3.connect("timeTable.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS TimeTable(Day int,
Schedule1 varchar(20), Schedule2 varchar(20), Schedule3 varchar(20), Schedule4 varchar(20), Schedule5 varchar(20),
Schedule6 varchar(20),Schedule7 varchar(20),Schedule8 varchar(20),Schedule9 varchar(20))""")
ls = []
for i in range(1,10):
    ls.append(list(df[i]))
for i in range(6):
    cur.execute("INSERT INTO TimeTable VALUES(?,?,?,?,?,?,?,?,?,?)",[i,ls[0][i],ls[1][i],ls[2][i],ls[3][i],ls[4][i],ls[5][i],ls[6][i],ls[7][i],ls[8][i]])

# i=cur.execute("select * from timeTable")
# print(i.fetchall())




if __name__ == "__main__":
    WhatsNextApp().run()

