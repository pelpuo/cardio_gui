from kivy.uix.screenmanager import Screen
import requests
import json
from kivymd.uix.list import ThreeLineListItem, TwoLineListItem

class DoctorsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None

    def on_enter(self):
        self.ids.verifiedList.clear_widgets()
        self.ids.unverifiedList.clear_widgets()
        self.load_doctors()
    
    def load_doctors(self):
        baseUrl = "https://kjox2q.deta.dev/"
        f = open("cache/keyfile.txt", 'r')
        key = f.readlines()[0]

        headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

        res = requests.get(baseUrl + "user", headers=headers)

        doctors = res.json()

        doctors_file = open("cache/doctors.txt", 'w')
        doctors_file.write(str(doctors))

        for doctor in doctors:
            li = TwoLineListItem(text=f"{doctor.get('first_name')} {doctor.get('last_name')}", secondary_text=f"email: {doctor.get('email_address')}")

            if doctor.get("is_verified") == True:
                self.ids.verifiedList.add_widget(li)
            else:
                self.ids.unverifiedList.add_widget(li)

