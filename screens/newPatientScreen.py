from datetime import date
import imp
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
import requests
from functools import partial
import json

class NewPatientScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None
        self.gender = None
        # self.dropdown = ObjectProperty()
        self.doctor_id = None

    def on_enter(self, *args):
        self.load_doctors()

    
    def gender_clicked(self, instance, value, gender):
        self.gender = gender
        print(self.gender)

    
    def load_doctors(self):
        baseUrl = "https://kjox2q.deta.dev/"
        f = open("cache/keyfile.txt", 'r')
        key = f.readlines()[0]
        f.close()

        headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

        res = requests.get(baseUrl + "user", headers=headers)

        doctors = res.json()

        doctors_file = open("cache/doctors.txt", 'w')
        doctors_file.write(str(doctors))


    def load_dropdown(self):
        print("dropdown_clicked")
        f = open("cache/doctors.txt", 'r')
        doctors = f.read()
        f.close()
        doctors = doctors.replace("\'", "\"")
        doctors = doctors.replace("True", '"True"')
        doctors = doctors.replace("False", '"False"')
        doctors = json.loads(doctors)

        self.dropdown = MDDropdownMenu(width_mult=3, caller=self.ids.doctor_name)
        for doctor in doctors:
            doctor_name = f"{doctor.get('first_name')} {doctor.get('last_name')}"
            self.dropdown.items.append(
                {"viewclass": "OneLineListItem",
                "text": doctor_name,
                "on_release": partial(self.option_callback,doctor_name, doctor.get("_id"))
                }
            )
        self.dropdown.open()

    def option_callback(self, doctor_name, doctor_id):
        self.ids.doctor_name.text = doctor_name
        self.doctor_id = doctor_id
        print(doctor_name + " " + doctor_id)

    def submit(self):
        _first_name = self.ids.first_name.text
        _last_name = self.ids.last_name.text
        _email_address = self.ids.email_address.text
        _date_of_birth = self.ids.date_of_birth.text
        _gender = self.gender

        patient_details = {
            "first_name":_first_name,
            "last_name":_last_name,
            "email_address": _email_address,
            "date_of_birth": _date_of_birth,
            "doctor_id":self.doctor_id,
            "gender":_gender
        }

        print(patient_details)

        valid = True

        for key in patient_details:
            if patient_details.get(key) == "":
                valid = False

        if valid:
            baseUrl = "https://kjox2q.deta.dev/"
            f = open("cache/keyfile.txt", 'r')
            key = f.readlines()[0]
            f.close()

            headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

            res = requests.post(baseUrl + "patient/", headers=headers, json=patient_details)
            res = res.json()
            print(res)

            self.app.root.current = "patients"

        

        
        


