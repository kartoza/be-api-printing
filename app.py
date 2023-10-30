# import required modules
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.screen import Screen
from kivymd.icon_definitions import md_icons
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput 
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.button import Button
from printing import APIPrint
import json
from kivy.uix.progressbar import ProgressBar  
from kivy.properties import ObjectProperty 
from kivy.uix.popup import Popup 

class APIApp(MDApp):
    def build(self):
         
        # create screen object
        screen = Screen()
        self.progress_bar = ProgressBar() 
        self.popup = Popup( 
            title ='Progress of Download', 
            content = self.progress_bar 
        ) 
  
        #defining 3rd label
        self.downloadLabel = MDLabel(text="Add the download path",
                    theme_text_color="Custom",
                    text_color=('black'),
                    font_style='H6',
                    pos_hint={'center_x':0.55, 'center_y':0.95})
         
        self.downloadInput = TextInput(font_size = 12, 
                      size_hint_y = None, 
                      size_hint_x = 0.8,
                      height = 30,
                      text='',
                      pos_hint={'center_x':0.5, 'center_y':0.90})
        
        
        #defining 3rd label
        self.urlLabel = MDLabel(text="Add the list of urls",
                    theme_text_color="Custom",
                    text_color=('black'),
                    font_style='H6',
                    pos_hint={'center_x':0.55, 'center_y':0.80})
         
        self.urlDownloadInput = TextInput(font_size = 12, 
                      size_hint_y = None, 
                      size_hint_x = 0.8,
                      height = 150,
                      text='https://gis.collaboratoronline.com/search?mapName=Channels&zoomLevel=8&editing=False&print=True&gpsCoordinates=30.092722446611162,-27.730076537015975&geoserverurl=https://geoserver.collaboratoronline.com/geoserver#',
                      pos_hint={'center_x':0.5, 'center_y':0.65})
        
        
        self.btn = Button(text ="Submit!",
                   font_size ="20sp",
                   background_color =(1, 1, 1, 1),
                   color =(1, 1, 1, 1), 
                   size =(25, 25),
                   size_hint =(.2, .2),
                   pos_hint={'center_x':0.5, 'center_y':0.20})
        
        self.btn.bind(on_press = self.callPrint)

        # add buttons
        screen.add_widget(self.downloadLabel)
        screen.add_widget(self.downloadInput)

        screen.add_widget(self.urlLabel)
        screen.add_widget(self.urlDownloadInput)

        screen.add_widget(self.btn)
         
        return screen
    
    def callPrint(self, event):
        url_list = self.urlDownloadInput.text
        urls = url_list.splitlines()
        url_len = len(urls)

        self.progress_bar.max = url_len
        self.popup.open() 
        download_path = self.downloadInput.text
        
        printAPI = APIPrint(urls, download_path, self.progress_bar)
        printAPI.apiCallBack()