# -*- coding: utf8 -*-
import os
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextFieldRound
from kivy.lang import Builder
from kivy.config import ConfigParser
from kivy.properties import *
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition, RiseInTransition
from kivy.core.window import Window
from kivy.logger import PY2
from kivymd.theming import ThemeManager
from kivymd.toast.kivytoast.kivytoast import toast
import re
#from kivy.network.urlrequest import UrlRequest
import requests
from kivy.network.urlrequest import UrlRequest
from baseclas.startscreen import StartScreen
import json
import sys
from kivymd.uix.list import OneLineIconListItem, TwoLineIconListItem
from kivymd.uix.label import MDLabel
from baseclas.cardnews import CardNews
from kivymd.uix.picker import MDDatePicker
from datetime import datetime

class BarberTwoLineIconListItem(TwoLineIconListItem):
    lid = NumericProperty()
    licon = StringProperty('')
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            toast(self.text+" id "+str(self.lid)+ '  '+str(self.uid))
            for l in self.parent.children:
                l.licon = 'checkbox-blank'

            self.licon = 'checkbox-marked'
            return True
        return super().on_touch_down(touch)

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
    lCard = BooleanProperty(False)
    lService = BooleanProperty(False)
    lMaster  = BooleanProperty(False)
    lServiceTime = BooleanProperty(False)
    lTimeTable = StringProperty('')


    url_register = StringProperty('')
    url_listnews = StringProperty('')
    url_userinfo = StringProperty('')
    url_lmasters = StringProperty('')
    url_lservices = StringProperty('')
    url_lservicestime = StringProperty('')

    #dict_masters = DictProperty()
    #dict_services = DictProperty()
    #dict_servicestime = DictProperty()


    def __init__(self, **kvargs):
        super(BarberApp, self).__init__(**kvargs)
        #Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'
        Window.size = (480, 853)

        self.window = Window
        self.config = ConfigParser() 
        
        self.url_register = 'http://127.0.0.1:8000/api/v1/register/'
        self.url_listnews = 'http://127.0.0.1:8000/api/v1/getlistnewsuser/'
        self.url_userinfo = 'http://127.0.0.1:8000/api/v1/getuserinfo/'
        self.url_lmasters = 'http://127.0.0.1:8000/api/v1/getlistmasters/'
        self.url_lservices = 'http://127.0.0.1:8000/api/v1/getlistservices/'
        self.url_lservicestime = 'http://127.0.0.1:8000/api/v1/getlisttime/'
        self.lCard = False
        

        self.manager = None
        

    #def get_application_config(self):
    #   return super(BarberApp, self).get_application_config('~/.%(appname)s.ini')
    #self.theme_cls.primary_hue = "500"
    #self.theme_cls.theme_style = "Dark"


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
        self.theme_cls.primary_palette = 'Gray'
        
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.manager.transition = RiseInTransition()
        
        
        if self.Token:
            self.manager.current_screen.ids.btn_reg.text = 'Войти'
            self.manager.current_screen.ids.tel_text.text = self.PhoneNumber

        self.get_list_masters()
        self.get_list_service()
        self.get_list_servicetime()
        self.set_date(datetime.date(datetime.today()))
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
            #добавить функцию обновления данных пользователя 'Имени' 
            self.toggle_base_screen()           
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
                    self.get_list_news()
                    
                else: 
                    self.say_user('Ошибка')    

    def say_user(self, errText):
        toast(errText)
        
    def change_title_actionbar(self, text_title):
        if self.manager.current == 'base':
            self.screen.ids.action_bar.title = text_title
        elif self.manager.current == 'login': 
            self.screen.ids.action_bar.title = self.title
        elif self.manager.current == 'order': 
            self.screen.ids.action_bar.title = text_title      

    def get_list_news(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_listnews, method='POST', req_headers=header, on_success=self.success_getdata)

    # Общая обработка сети    
    def success_getdata(self, request, result):
        
        if request.url == self.url_listnews:
            if not self.lCard:
                self.lCard = True
                instance_grid = self.manager.current_screen.ids.grid_card
                
                for news in result:
                    instance_grid.add_widget(CardNews(
                        text_title = news['bTitleNews'],
                        text_body  = news['bTextNews']
                    ))
        elif request.url == self.url_lmasters:
            self.write_list_master(result)

        elif request.url == self.url_lservices:
            self.write_list_service(result)
        
        elif request.url == self.url_lservicestime:
            self.write_list_timetable(result)
            

    def error_listnews(self, *args):
        a=0    

    def get_user_info(self):
        pass
    def get_user_orders(self):
        pass
    def create_user_order(self):
        pass
    def get_list_service(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_lservices, method='POST', req_headers=header, on_success=self.success_getdata) 

    def get_list_servicetime(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_lservicestime, method='POST', req_headers=header, on_success=self.success_getdata) 

    def get_list_masters(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_lmasters, method='POST', req_headers=header, on_success=self.success_getdata)   

    def sys_exit(self):
        sys.exit(0)    

    def sm_on_enter(self):
        if self.manager.current == 'base':
            self.screen.ids.action_bar.right_action_items = [['account-edit-outline', lambda x: self.toggle_order_screen()], ['exit-to-app', lambda x: self.sys_exit()]]
        elif self.manager.current == 'order':
            self.screen.ids.action_bar.right_action_items = [['arrow-left', lambda x: self.toggle_base_screen()], ['exit-to-app', lambda x: self.sys_exit()]]   

    def toggle_base_screen(self):
        self.manager.current = 'base'
        self.change_title_actionbar('Новости')
        if not self.lCard:
            self.get_list_news()   #чтобы не дергать сеть постоянно

    def toggle_order_screen(self):
        self.manager.current = 'order'
        self.change_title_actionbar('Запись к мастеру...')
        
    

    def write_list_service(self, result):
        listservice = self.manager.screens[2].ids.service.ids.common_list    
        if not self.lService:
            self.lService=True
            for lService in result:
                listservice.add_widget(BarberTwoLineIconListItem(
                    text = lService['bService'],
                    secondary_text = 'Стоимость услуги: '+ lService['bPrice']+' руб.',
                    lid = lService['id'],
                    licon = 'checkbox-blank'
                ))
    
    def write_list_master(self, result):
        listmaster = self.manager.screens[2].ids.master.ids.common_list
        if not self.lMaster:
            self.lMaster = True
            for lMaster in result:
                listmaster.add_widget(BarberTwoLineIconListItem(
                    #icon ="language-python",
                    text = lMaster['bMaster'],
                    secondary_text = 'Краткое описание мастера',
                    lid = lMaster['id'],
                    licon = 'checkbox-blank'
                ))  

    def write_list_timetable(self, result):
        listtime = self.manager.screens[2].ids.timetable.ids.common_list
        if not self.lServiceTime: 
            self.lServiceTime = True
            for lservicetime in result:
                listtime.add_widget(BarberTwoLineIconListItem(
                    text = 'Время оказания услуги: ' + lservicetime['bTime'],
                    secondary_text = 'Занято или свободно',
                    lid = lservicetime['id'],
                    licon = 'checkbox-blank'
                ))
    
    def update_date(self):
        date_dialog = MDDatePicker(
        callback=self.set_date)
        date_dialog.open()
        # вызвать функцию обновления расписания

    def set_date(self, *args):
        text_date = self.manager.screens[2].ids.timetable.ids.text_date
        text_date.text = args[0].strftime("%d %B %Y")
        self.lTimeTable = str(args[0])

    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        
        if tab_text == 'Расписание':
            if not instance_tab.ids.text_date:
                instance_tab.ids.text_date = self.lTimeTable
        # получим данные о расписании с сервера        
        
if __name__ == '__main__':
    BarberApp().run()