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


class WindowManager(ScreenManager):
    pass
 
class DashboardScreen(Screen):
    pass

class NewReadingScreen(Screen):
    pass


class NewPatientScreen(Screen):
    pass

class EcgReadingScreen(Screen):
    pass

class EcgResultsScreen(Screen):
    pass


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
        screen_manager.add_widget(NewPatientScreen(name="new_patient"))

        screen_manager.add_widget(EcgReadingScreen(name="ECG"))

        return screen_manager

    def back(self, page):
        print("back pressed")
        screen_manager.current = page


        

if __name__ == "__main__":
    myApp().run()