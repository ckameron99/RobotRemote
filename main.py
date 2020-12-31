from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix import label
from kivy.graphics import *
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

import socket


class API():
    def __init__(self,ui):
        self.robotIP="192.168.1.254"
        self.appIP=socket.gethostbyname(socket.gethostname())
        self.ui=ui

    def attemptConnect(self):
        return False




class UI(Screen):
    def __init__(self,**kwargs):
        self.api=API(self)
        self.batteryStatus=0.0
        self.positionStatus=(0,0)
        self.pitchStatus=0.0
        self.rollStatus=0.0
        super().__init__(**kwargs)

    def updateBattery(self,delta):
        self.battery+=delta
        self.battery=round(self.battery,3)
        self.ids.batteryStatus.text="Battery: {}".format(self.battery)

    def connectUI(self):
        connectionSuccess=self.api.attemptConnect()
        self.ids.connectButton.text="Connection to RPi: {}".format(
            "SUCCESS" if connectionSuccess else "FAILED"
            )

    def connectRemote(self):
        self.ids.remoteButton.text="Remote: ON"

    def connectLidar(self):
        pass

    def connectOrientation(self):
        pass

    def connectMotors(self):
        pass

    def reboot(self):
        pass

    def powerDown(self):
        pass

    def update(self):
        pass


class MainApp(App):
    def __init__(self):
        super().__init__()
    def build(self):
        ui=UI()
        return ui

def main():
    MainApp().run()

if __name__=="__main__":
    main()
print("done")
