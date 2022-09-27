from operator import pos
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineListItem
 
class WindowManager(ScreenManager):
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
            li = TwoLineListItem(text=f"{item} verified", secondary_text=f"This is the {item} list item")
            li2 = TwoLineListItem(text=f"{item} unverified", secondary_text=f"This is the {item} list item")
            self.ids.verifiedList.add_widget(li)
            self.ids.unverifiedList.add_widget(li2)

class NewPatientScreen(Screen):
    pass

class CardioGUI(MDApp):

    def build(self):  
        Builder.load_file("screens/mgr.kv")

        global screen_manager
        screen_manager = ScreenManager()
        doctorScreen = DoctorsScreen(name="doctors")
        doctorScreen.addListItems()
        # screen_manager.add_widget(doctorScreen)

        screen_manager.add_widget(NewPatientScreen(name="new_patient"))



        return screen_manager

if __name__ == "__main__":
    CardioGUI().run()