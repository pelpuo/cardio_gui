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

def get_microphone_level():
    """
    `source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
    audioop.max alternative to audioop.rms
    """
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    s = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=chunk)
    global levels
    global reading_values
    reading_values = []
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)
        if len(levels) >= 100:
            levels = []
        levels.append(mx)
        reading_values.append(mx)

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
        f = open("cache/new_reading.txt", "w")
        f.write(str(reading_values))
        f.close()
        self.app.root.current = "patient_readings"


class myApp(MDApp):
    def build(self): 

        Builder.load_file("windowManager.kv")

        global screen_manager
        screen_manager = ScreenManager()
        
        screen_manager.add_widget(LoginScreen(name="login"))

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

        screen_manager.add_widget(NewReadingScreen(name="new_reading"))

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
    get_level_thread = Thread(target = get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()
    myApp().run()