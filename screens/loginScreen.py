from kivy.uix.screenmanager import Screen
import requests

class LoginScreen(Screen):    
    # def __init__(self):
        # self.baseUrl = "https://kjox2q.deta.dev/"

    def login(self, email, password):
        baseUrl = "https://kjox2q.deta.dev/"
        # data = {"username":email, "password":password}
        data = {"username":"tech@example.com", "password":"password"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.post(baseUrl + "login", data=data, headers=headers)
        res = res.json()
        print(res.get("access_token"))
        if(res.get("access_token")):
            f = open("cache/keyfile.txt", "w")
            f.write(res.get("access_token"))
            return True
        else:
            return False

# login = LoginScreen()
# login.login("jjackson@example.com", "password")