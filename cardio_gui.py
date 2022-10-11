import imp
from unicodedata import name
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineListItem
from screens.loginScreen import LoginScreen
from screens.doctorScreen import DoctorsScreen
from screens.patientsScreen import PatientsScreen
from screens.patientReadingsScreen import PatientReadingsScreen
from screens.ecgResultsScreen import EcgResultsScreen
from screens.newPatientScreen import NewPatientScreen
from screens.newReadingScreen import NewReadingScreen

from threading import Thread
import audioop
import pyaudio
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot

import serial
import time
import requests
import json
import pandas as pd

import time

def get_ecg_readings_from_file():
    global levels
    global reading_values
    reading_values = []

    i = 0
    sam = pd.read_csv("ecg_3.csv")
    sam_vals = sam["0"]

    sub = 0

    while True:
        if len(levels) >= 100:
            levels = []

        if len(reading_values) >= 5000:
            reading_values.pop(0)

        if sub == 4:
            levels.append((sam_vals[i] + 1) * 100)  
        reading_values.append(sam_vals[i])

        i+=1
        if i > 15000:
            i = 0
        
        sub += 1
        if sub > 4:
            sub = 0

        time.sleep(.001)

        


def get_ecg_readings():
    arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)
    global levels
    global reading_values
    reading_values = []
    while True:
        line = arduino.readline()   # read a byte
        if line:
            string = line.decode()  # convert the byte string to a unicode string
            num = int(string) # convert the unicode string to an int
            if len(levels) >= 100:
                levels = []
            if len(reading_values) >= 5000:
                reading_values.pop(0)
            levels.append(num)
            reading_values.append(num)


def post_ecg_readings():
    baseUrl = "https://kjox2q.deta.dev/"

    f = open("cache/keyfile.txt", 'r')
    key = f.readlines()[0]
    f.close()

    f = open("cache/selected_patient.txt", 'r')
    selected_patient = f.readlines()[0]
    f.close()
    
    f = open("cache/reading_details.txt", 'r')
    reading_details_txt = f.readlines()[0]
    f.close()

    reading_details_txt = reading_details_txt.replace("\'", "\"")

    reading_details = json.loads(reading_details_txt)
    reading_details["patient_id"] = selected_patient

    reading_details["values"] = []
    f = open("cache/new_reading.txt", 'r')
    reading_vals = f.readlines()[0]
    f.close()
    reading_vals = reading_vals.replace("[", "").replace("]", "")
    reading_vals = reading_vals.split(", ")
    for sample in range(len(reading_vals)):
        reading_details["values"].append({
        "sample": sample,
        "MLII": int(reading_vals[sample]),
        "V5": 0
    })

    reading_details["predictions"] = "normal"
    # Add logic for retrieving predictions

    headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

    res = requests.post(baseUrl + "reading/", headers=headers, json=reading_details)
    res = res.json()
    print(res)



# def get_microphone_level():
#     """
#     `source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
#     audioop.max alternative to audioop.rms
#     """
#     chunk = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100
#     p = pyaudio.PyAudio()

#     s = p.open(format=FORMAT,
#             channels=CHANNELS,
#             rate=RATE,
#             input=True,
#             frames_per_buffer=chunk)
#     global levels
#     global reading_values
#     reading_values = []
#     while True:
#         data = s.read(chunk)
#         mx = audioop.rms(data, 2)
#         if len(levels) >= 100:
#             levels = []
#         levels.append(mx)
#         reading_values.append(mx)

class WindowManager(ScreenManager):
    pass
 
class DashboardScreen(Screen):
    pass


class EcgReadingScreen(Screen):
    def __init__(self, **kwargs):
        super(EcgReadingScreen, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

        self.app = None

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)


    def get_value(self, dt):
        self.plot.points = [(i, j/5) for i, j in enumerate(levels)]
    
    def end(self):
        self.stop()

        # Format ecg data and add logic for predictions

        f = open("cache/new_reading.txt", "w")
        f.write(str(reading_values))
        f.close()
        self.app.root.current = "patient_readings"


class myApp(MDApp):
    def build(self): 

        Builder.load_file("windowManager.kv")

        global screen_manager
        screen_manager = ScreenManager()
        
        loginScreen = LoginScreen(name="login")
        loginScreen.app = self
        screen_manager.add_widget(loginScreen)

        dashboard = DashboardScreen(name="dashboard")
        screen_manager.add_widget(dashboard)

        doctorsScreen = DoctorsScreen(name="doctors")
        doctorsScreen.app = self
        screen_manager.add_widget(doctorsScreen)

        patientsScreen = PatientsScreen(name="patients")
        patientsScreen.app = self
        screen_manager.add_widget(patientsScreen)

        patientReadingsScreen = PatientReadingsScreen(name="patient_readings")
        patientReadingsScreen.app = self
        screen_manager.add_widget(patientReadingsScreen)

        new_reading = NewReadingScreen(name="new_reading")
        new_reading.app = self
        screen_manager.add_widget(new_reading)

        new_patients = NewPatientScreen(name="new_patient")
        new_patients.app = self
        screen_manager.add_widget(new_patients)

        ecgReading = EcgReadingScreen(name="ecg_reading")
        ecgReading.app = self
        screen_manager.add_widget(ecgReading)

        ecgResults = EcgResultsScreen(name="ecg_results")
        ecgResults.app = self
        screen_manager.add_widget(ecgResults)

        return screen_manager

    def back(self, page):
        print("back pressed")
        screen_manager.current = page


        

if __name__ == "__main__":
    levels = []  # store levels of microphone
    # get_level_thread = Thread(target = get_microphone_level)
    get_level_thread = Thread(target = get_ecg_readings_from_file)
    get_level_thread.daemon = True
    get_level_thread.start()
    myApp().run()