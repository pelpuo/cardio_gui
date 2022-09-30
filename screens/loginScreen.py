from kivy.uix.screenmanager import Screen
import requests

class LoginScreen(Screen):    
    # def __init__(self):
        # self.baseUrl = "https://kjox2q.deta.dev/"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = None

    def login(self, email, password):
        baseUrl = "https://kjox2q.deta.dev/"
        data = {"username":email, "password":password}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.post(baseUrl + "login", data=data, headers=headers)
        res = res.json()
        print(res.get("access_token"))
        if(res.get("access_token")):
            f = open("cache/keyfile.txt", "w")
            f.write(res.get("access_token"))
            f.close()
            self.app.root.current = "dashboard"
        else:
            return False

        

# login = LoginScreen()
# login.login("jjackson@example.com", "password")