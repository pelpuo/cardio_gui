from kivy.uix.screenmanager import Screen
import requests
from matplotlib import pyplot as plt
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg

class EcgResultsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None

    def on_enter(self):
        # self.ids.ecg_results.clear_widgets()
        self.load_result()

    def load_result(self):
        baseUrl = "https://kjox2q.deta.dev/"
        f = open("cache/keyfile.txt", 'r')
        key = f.readlines()[0]

        f =  open('cache/selected_reading.txt', 'r')
        reading_id = f.readlines()[0]

        headers = {'Content-Type': 'application/json', 'Authorization':f'Bearer {key}'}

        res = requests.get(baseUrl + "reading/" + reading_id, headers=headers)

        ecg_results = res.json()

        ecg_results_file = open("cache/ecg_results.txt", 'w')
        ecg_results_file.write(str(ecg_results))

        # Drawing of ECG Graph
        signals = []
        for result in ecg_results.get("values"):
            signals.append(result.get("'MLII'"))
        
        signals = np.array(signals)
        plt.plot(signals)
          
        # setting x label
        plt.xlabel('Time(s)')
          
        # setting y label
        plt.ylabel('signal')
        plt.grid(True, color='lightgray')
          
        # adding plot to kivy boxlayout
        self.ids.results.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return self.ids