from kivy.uix.screenmanager import Screen
import requests
import json
from kivymd.uix.list import ThreeLineListItem
from functools import partial


class PatientsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None

    def on_enter(self):
        self.ids.patients.clear_widgets()
        self.load_patients()
    
    def load_patients(self):
        baseUrl = "https://kjox2q.deta.dev/"
        f = open("cache/keyfile.txt", 'r')
        key = f.readlines()[0]
        f.close()

        headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

        res = requests.get(baseUrl + "patient", headers=headers)

        patients = res.json()

        patients_file = open("cache/patients.txt", 'w')
        patients_file.write(str(patients))

        for patient in patients:
            li = ThreeLineListItem(text=f"{patient.get('first_name')} {patient.get('last_name')}", secondary_text=f"email: {patient.get('email_address')} | birth: {patient.get('date_of_birth')}", tertiary_text= f"gender: {patient.get('gender')}")
            li.on_release = partial(self.to_patient_readings,patient.get('_id'))
            self.ids.patients.add_widget(li) 


    def to_patient_readings(self, patient_id):
        selected_patient_file = open("cache/selected_patient.txt", 'w')
        selected_patient_file.write(patient_id)
        self.app.root.current = "patient_readings"