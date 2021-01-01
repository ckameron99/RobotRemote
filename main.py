from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix import label
from kivy.graphics import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

import socket


class API():
    def __init__(self,ui):
        self.robotIP="192.168.1.254"
        self.appIP=socket.gethostbyname(socket.gethostname())
        self.listenPort=5551
        self.sendPort=5552
        self.ui=ui
        self.connected=False

    def attemptConnect(self):
        if not self.connected:
            self.listeningDaemon=threading.Thread(target=self.listen, daemon=True, args=(1,))
            self.sendData(b'initConnection: True')
            return False
        return True

    def listen(self, name):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.appID, self.listenPort))
        s.listen
        while True:
            data=''
            conn,addr=s.accept()
            with conn:
                while True:
                    newData=conn.recv(1024)
                    if newData:
                        data+=newData
                    else:
                        break
            self.processData(data)

    def processData(self, data):
        splitIndex=data.index(b': ')
        key=data[:splitIndex]
        params=data[splitIndex+2:]
        funcs={
        b'connectionStatus': self.ui.setConnectionStatus
        }
        funcs[key](params)

    def sendData(self, data):
        s=socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
        s.connect((self.robotIP, self.sendPort))
        s.sendall(data)
        s.close()


class UI(Screen):
    def __init__(self,**kwargs):
        self.api=API(self)
        self.batteryStatus=0.0
        self.positionStatus=(0,0)
        self.pitchStatus=0.0
        self.rollStatus=0.0
        super().__init__(**kwargs)

    def confirmBox(self,confirmFunc):
        def cf(button):
            popup.dismiss()
            confirmFunc()

        content=BoxLayout()
        popup=Popup(title='Are you sure?', content=content)
        confirmButton=Button(text="Confirm", on_press=cf)
        cancelButton=Button(text="Cancel", on_press=popup.dismiss)
        content.add_widget(confirmButton)
        content.add_widget(cancelButton)
        popup.open()

    def updateBattery(self,delta):
        self.battery+=delta
        self.battery=round(self.battery,3)
        self.ids.batteryStatus.text="Battery: {}".format(self.battery)

    def connectUI(self):
        connectionSuccess=self.api.attemptConnect()
        self.ids.connectButton.text="Connection to RPi: {}".format(
            "SUCCESS" if connectionSuccess else "FAILED"
            )

    def setConnectionStatus(self, status):
        if status==b'True':
            self.ids.connectButton.text="Connection to RPI: SUCCESS"

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
