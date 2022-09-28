from kivy.uix.screenmanager import Screen

class NewPatientScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.gender = None
    
    def gender_clicked(self, instance, value, gender):
        self.gender = gender
        print(self.gender)
