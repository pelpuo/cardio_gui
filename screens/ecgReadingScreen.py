from kivy.uix.screenmanager import Screen
import requests
import json
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot
from kivy.clock import Clock
from threading import Thread
import audioop
import pyaudio

class EcgReadingScreen(Screen):
    # pass
    def __init__(self, **kwargs):
        super(EcgReadingScreen, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.levels = []

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j/5) for i, j in enumerate(self.levels)]


# class Logic(BoxLayout):
#     def __init__(self, **kwargs):
#         super(Logic, self).__init__(**kwargs)
#         self.plot = MeshLinePlot(color=[1, 0, 0, 1])
#         self.levels = []

#     def start(self):
#         self.ids.graph.add_plot(self.plot)
#         Clock.schedule_interval(self.get_value, 0.001)

#     def stop(self):
#         Clock.unschedule(self.get_value)

#     def get_value(self, dt):
#         self.plot.points = [(i, j/5) for i, j in enumerate(self.levels)]