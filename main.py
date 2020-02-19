# -*- coding: utf8 -*-
import os
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextFieldRound
from kivy.lang import Builder
from kivy.config import ConfigParser
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.logger import PY2
from kivymd.theming import ThemeManager
from kivymd.toast.kivytoast.kivytoast import toast
import re

class basescreen(Screen):
    pass
    

class loginscreen(Screen):
    pass

class MyTextField(MDTextFieldRound):
    pattern = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 14:
            return super(MDTextFieldRound, self).insert_text('', from_undo=from_undo)

        s = re.sub(self.pattern, '', substring)

        if s:
            if len(self.text) == 6:
                self.text = self.text+')'
            return super(MDTextFieldRound, self).insert_text(substring, from_undo=from_undo)
        else:
            return super(MDTextFieldRound, self).insert_text(s, from_undo=from_undo)    

    def do_backspace(self, from_undo=False, mode='bkspc'):
        if len(self.text) == 3:
            return False   
        return super(MDTextFieldRound, self).do_backspace(from_undo, mode)


class BarberApp(MDApp):
    title = 'BARBER STYLE'
    PhoneNumber = StringProperty('')
    Token = StringProperty('')
    FirstName = StringProperty('')
    


    def __init__(self, **kvargs):
        super(BarberApp, self).__init__(**kvargs)
        #Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'
        Window.size = (480, 853)

        self.window = Window
        self.config = ConfigParser()    
        
        

    #def get_application_config(self):
    #   return super(BarberApp, self).get_application_config('~/.%(appname)s.ini')

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'ru')  
        config.setdefault('General', 'token', '')  
        config.setdefault('General', 'firstname', '')
        config.setdefault('General', 'lastname', '')
        config.setdefault('General', 'phonenumber', '')
        config.setdefault('General', 'version', '')

    def read_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'barber.ini'))
        self.FirstName = self.config.get('General', 'firstname')
        self.PhoneNumber = self.config.get('General', 'phonenumber')
        self.Token = self.config.get('General', 'token')
        self.config.write()



    def write_value_in_config(self, keyvalue):
        self.config.read(os.path.join(self.directory, 'barber.ini'))
        self.config.setall('General', keyvalue)
        self.config.write()

    def build(self):
        
        self.load_all_kv_files(os.path.join(self.directory, 'kv'))
        self.read_value_from_config()
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'BlueGray'
        sm = ScreenManager()
        sm.add_widget(basescreen(name='base'))
        sm.add_widget(loginscreen(name='login'))
        self.screen = sm
        
        if not self.PhoneNumber:
            mytext = 'phone empty' # Экран логина
            self.screen.current = 'login'
        else:
            mytext = 'phone not empty'
            self.screen.current = 'base'

        return self.screen


    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                if not PY2:
                    with open(kv_file, encoding='utf-8') as kv:
                        Builder.load_string(kv.read())
                else:
                    Builder.load_file(kv_file)

    def registration(self):
        if not self.screen.current_screen.ids['tel_text'].text:
            toast('Телефон не может быть пустым')
        else:
            pass

    

if __name__ == '__main__':
    BarberApp().run()