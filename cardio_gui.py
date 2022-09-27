from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineListItem

class WindowManager(ScreenManager):
    pass

class LoginScreen(Screen):    
    def some_function(self):
        print("hello")
 
class DashboardScreen(Screen):
    pass

class DoctorsScreen(Screen):
    def addListItems(self):
        items = ["First", 
        "Second", 
        "Third", 
        "Fourth", 
        "Fifth", 
        "Sixth", 
        "Seventh", 
        "Eighth", 
        "Ninth", 
        "Tenth"
        ]
        for item in items:
            li = TwoLineListItem(text=f"{item} verified", secondary_text=f"This is the {item} verified doctor")
            li2 = TwoLineListItem(text=f"{item} unverified", secondary_text=f"This is the {item} unverified doctor")
            self.ids.verifiedList.add_widget(li)
            self.ids.unverifiedList.add_widget(li2)

class PatientsScreen(Screen):
    pass

class PatientReadingsScreen(Screen):
    pass

class NewReadingScreen(Screen):
    pass


class NewPatientScreen(Screen):
    pass

class EcgScreen(Screen):
    pass


class myApp(MDApp):
    def build(self): 
        items = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]

        Builder.load_file("windowManager.kv")

        global screen_manager
        screen_manager = ScreenManager()
        
        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(DashboardScreen(name="dashboard"))

        doctorsScreen = DoctorsScreen(name="doctors")
        self.addListItems(doctorsScreen, items, "verifiedList")
        self.addListItems(doctorsScreen, items, "unverifiedList")
        screen_manager.add_widget(doctorsScreen)

        patientsScreen = PatientsScreen(name="patients")
        self.addListItems(patientsScreen, items, "patients", on_release=self.to_patient_readings)
        screen_manager.add_widget(patientsScreen)

        patientReadingsScreen = PatientReadingsScreen(name="patient_readings")
        self.addListItems(patientReadingsScreen, items, "patient_readings")
        screen_manager.add_widget(patientReadingsScreen)

        screen_manager.add_widget(NewReadingScreen(name="new_reading"))
        screen_manager.add_widget(NewPatientScreen(name="new_patient"))

        screen_manager.add_widget(EcgScreen(name="ECG"))

        return screen_manager

    def back(self, page):
        print("back pressed")
        screen_manager.current = page

    
    def addListItems(self, screen, items, listId, **kwargs):
        for item in items:
            li = TwoLineListItem(text=f"{item} patient reading", secondary_text=f"This is the {item} patient reading")
            if kwargs.get('on_release'):
                li.on_release = kwargs['on_release']
            screen.ids[listId].add_widget(li)


    # def addPatientReadings(self, screen):
    #     items = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
    #     for item in items:
    #         li = TwoLineListItem(text=f"{item} patient", secondary_text=f"This is the {item} patient")
    #         li.on_release = self.to_patient_readings
    #         screen.ids.patients.add_widget(li)

    def to_patient_readings(self):
        screen_manager.current = "patient_readings"

        

if __name__ == "__main__":
    myApp().run()