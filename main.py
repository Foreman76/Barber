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
#from kivy.network.urlrequest import UrlRequest
import requests
from baseclas.startscreen import StartScreen


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
    url_register = StringProperty('')


    def __init__(self, **kvargs):
        super(BarberApp, self).__init__(**kvargs)
        #Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'
        Window.size = (480, 853)

        self.window = Window
        self.config = ConfigParser()    
        self.url_register = 'http://127.0.0.1:8000/api/v1/register/'
        self.manager = None
        

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
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        
        
        if self.Token:
            self.manager.current_screen.ids.btn_reg.text = 'Войти'
            self.manager.current_screen.ids.tel_text.text = self.PhoneNumber

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

    def registration(self, btn_text):

        if btn_text == 'Войти':
            self.manager.current = 'base'
            #добавить функцию обновления данных пользователя 'Имени' 
            self.change_title_actionbar('Новости')

        else:
            PhoneNumber = self.manager.current_screen.ids.tel_text.text
            if  PhoneNumber == '+7(' or len(PhoneNumber) < 14:
                self.say_user('Введите правильный номер телефона') 
            else:
                header = {'Content-type':'application/Json'}
                params = {'phone':PhoneNumber}
                resp = requests.post(self.url_register, headers=header, json=params)

                if resp.status_code == 200:
                    user_info = resp.json()
                    keyvalue = {'token':user_info['token'], 'phonenumber':user_info['phone'], 'firstname':user_info['nUser']}
                    self.write_value_in_config(keyvalue)
                    self.manager.current = 'base'
                else: 
                    self.say_user('Ошибка')    

    def say_user(self, errText):
        toast(errText)
        
    def change_title_actionbar(self, text_title):
        if self.manager.current == 'base':
            self.screen.ids.action_bar.title = 'Новости'
        elif self.manager.current == 'login': 
            self.screen.ids.action_bar.title = self.title   

if __name__ == '__main__':
    BarberApp().run()