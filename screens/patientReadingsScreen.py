from kivy.uix.screenmanager import Screen
import requests
import json
from kivymd.uix.list import ThreeLineListItem, TwoLineListItem

class PatientReadingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None

    def on_enter(self):
        self.ids.patient_readings.clear_widgets()
        self.load_patient_readings()

    def load_patient_readings(self):
        baseUrl = "https://kjox2q.deta.dev/"
        f = open("keyfile.txt", 'r')
        key = f.readlines()[0]

        f =  open('selected_patient.txt', 'r')
        patient_id = f.readlines()[0]

        headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

        res = requests.get(baseUrl + "reading/patient/" + patient_id , headers=headers)

        readings = res.json()

        readings_file = open("readings.txt", 'w')
        readings_file.write(str(readings))

        for reading in readings:
            li = ThreeLineListItem(text=f"date: {reading.get('created_at')}  |  Hospital: {reading.get('hospital_name')}", 
            secondary_text=f"Lead Type: {reading.get('lead_type')}  |  Lead Placement: {reading.get('lead_placement')}",
            tertiary_text = f"speed: {reading.get('speed')}  |  limb: {reading.get('limb')}  |  chest: {reading.get('chest')}")

            self.ids.patient_readings.add_widget(li)
