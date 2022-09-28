import imp
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
from screens.ecgReadingScreen import EcgReadingScreen, Logic

from threading import Thread
import audioop
import pyaudio

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
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)
        if len(levels) >= 100:
            levels = []
        levels.append(mx)

class WindowManager(ScreenManager):
    pass
 
class DashboardScreen(Screen):
    pass

class NewReadingScreen(Screen):
    pass


class NewPatientScreen(Screen):
    pass

class EcgResultsScreen(Screen):
    pass


class myApp(MDApp):
    def build(self): 

        Builder.load_file("windowManager.kv")

        global screen_manager
        screen_manager = ScreenManager()

        logic = Logic()
        logic.levels = levels

        # ecgReadingScreen = EcgReadingScreen(name="EcgReading")
        # # ecgReadingScreen.levels = levels
        # ecgReadingScreen.add_widget(Logic())
        # screen_manager.add_widget(ecgReadingScreen)
        
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
        screen_manager.add_widget(NewPatientScreen(name="new_patient"))

        ecgReadingScreen = EcgReadingScreen(name="EcgReading")
        ecgReadingScreen.levels = levels
        screen_manager.add_widget(ecgReadingScreen)

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