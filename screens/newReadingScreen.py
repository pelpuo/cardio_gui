from kivy.uix.screenmanager import Screen

class NewReadingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None
    
    def submit(self):
        hospital_name = self.ids.hospital_name.text
        lead_type = self.ids.lead_type.text
        lead_placement = self.ids.lead_placement.text
        speed = self.ids.speed.text
        limb = self.ids.limb.text
        chest = self.ids.chest.text

        reading_details = {
            "hospital_name":hospital_name,
            "lead_type":lead_type,
            "lead_placement": lead_placement,
            "speed": speed,
            "limb":limb,
            "chest":chest
        }

        print(reading_details)

        valid = True

        for key in reading_details:
            if reading_details.get(key) == "":
                valid = False

        if valid:
            f = open("cache/reading_details.txt", "w")
            f.write(str(reading_details))
            f.close()

            self.app.root.current = "ecg_reading"