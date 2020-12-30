from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix import label
from kivy.graphics import *


class UI(Screen):
    def __init__(self,**kwargs):
        self.battery=0.0
        super().__init__(**kwargs)
    def updateBattery(self,delta):
        self.battery+=delta
        self.battery=round(self.battery,3)
        self.ids.battery.text="Battery: {}".format(self.battery)


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
