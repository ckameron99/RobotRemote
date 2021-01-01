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
import threading


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
            self.connected=True
            try:
                self.sendData(b'initConnection: True')
                self.connected=True
                return True
            except ConnectionRefusedError:
                self.connected=False
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
        b'connectionStatus': self.ui.setConnectionStatus,
        b'batteryStatus': self.ui.setBatteryStatus,
        b'positionStatus': self.ui.setPositionStatus,
        b'pitchStatus': self.ui.setPitchStatus,
        b'rollStatus': self.ui.setRollStatus,
        b'remoteStatus': self.ui.setRemoteStatus,
        b'lidarStatus': self.ui.setLidarStatus,
        b'orientationStatus': self.ui.setOrientationStatus,
        b'motorStatus': self.ui.setMotorStatus
        }
        funcs[key](params)

    def sendData(self, data):
        if self.connected:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.robotIP, self.sendPort))
            s.sendall(data)
            s.close()
            return True
        else:
            self.ui.addText(b'Robot is not connected')
            return False


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

    def connectUI(self):
        connectionSuccess=self.api.attemptConnect()
        self.ids.connectButton.text="Connection to RPi: {}".format(
            "SUCCESS" if connectionSuccess else "FAILED"
            )

    def connectRemote(self):
        self.api.sendData(b'connectRemote: True')

    def connectLidar(self):
        self.api.sendData(b'connentLidar: True')

    def connectOrientation(self):
        self.api.sendData(b'connectOrientation: True')

    def connectMotors(self):
        self.api.sendData(b'connectMotors: True')

    def reboot(self):
        self.confirmBox(
        confirmFunc=self.rebootConfirmed
        )

    def rebootConfirmed(self):
        self.api.sendData(b'powerOptions: reboot')

    def powerDown(self):
        self.confirmBox(
        confirmFunc=self.powerDownConfirmed
        )

    def rebootConfirmed(self):
        self.api.sendData(b'powerOptions: powerDown')

    def update(self):
        self.confirmBox(
        confirmFunc=self.updateConfirmed
        )

    def rebootConfirmed(self):
        self.api.sendData(b'powerOptions: update')

    def setConnectionStatus(self, status):
        self.ids.connectButton.text="Connection to RPI: {}".format(status.decode("uft-8"))

    def setBatteryStatus(self, status):
        self.ids.batteryStautus.text="Battery: {}".format(status.decode("uft-8"))

    def setPositionStatus(self, status):
        self.ids.positionStautus.text="Position: {}".format(status.decode("uft-8"))

    def setPitchStatus(self, status):
        self.ids.pitchStautus.text="Pitch: {}".format(status.decode("uft-8"))

    def setRollStatus(self, status):
        self.ids.rollStautus.text="Roll: {}".format(status.decode("uft-8"))

    def setRemoteStatus(self, status):
        self.ids.remoteButton.text="Remote: {}".format(status.decode("uft-8"))

    def setLidarStatus(self, status):
        self.ids.lidarButton.text="LiDAR: {}".format(status.decode("uft-8"))

    def setOrientationStatus(self, status):
        self.ids.orientationButton.text="Orientation unit: {}".format(status.decode("uft-8"))

    def setMotorStatus(self, status):
        self.ids.motorsButton.text="Motors: {}".format(status.decode("uft-8"))

    def addText(self,text):
        self.ids.genericText.text+=text.decode("utf-8")+"\n"


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
