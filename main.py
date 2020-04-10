# -*- coding: utf8 -*-
'''

= ['Primary', 'Secondary', 'Background', 'Surface', 'Error', 'On_Primary', 'On_Secondary', 'On_Background', 'On_Surface', 'On_Error']

'''




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

import requests
from kivy.network.urlrequest import UrlRequest
from baseclas.startscreen import StartScreen
import json
import sys
from kivymd.uix.list import TwoLineAvatarIconListItem, IRightBodyTouch, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from baseclas.cardnews import CardNews
from kivymd.uix.picker import MDDatePicker
from datetime import datetime

class MyCheckbox(IRightBodyTouch, MDCheckbox):
    pass
class MasterCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class TimeCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class MyAvatar(ILeftBody, Image):
    pass

class MasterTwoLineAvatarListItem(TwoLineAvatarIconListItem):
    lid = NumericProperty()
    ltype = StringProperty('')
    lcheckstatus = BooleanProperty(False)
    lmaster_text = StringProperty('')

class TimeTwoLineAvatarListItem(TwoLineAvatarIconListItem):
    lid = NumericProperty()
    ltype = StringProperty('')
    lcheckstatus = BooleanProperty(False)
    lmaster_text = StringProperty('')
    lservice_text = StringProperty('')

class OrderTwoLineAvatarListItem(TwoLineAvatarIconListItem):
    pass    

class BarberTwoLineAvatarListItem(TwoLineAvatarIconListItem):
    lid = NumericProperty()
    ltype = StringProperty('')
    lcheckstatus = BooleanProperty(False)
    lservice_text = StringProperty('')
    '''
    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            if self.ltype == 'мастер':

                dialog = MDDialog(
                    title="Информация:",
                    size_hint=(0.8, 0.3),
                    text_button_ok="Yes",
                    text=self.lmaster_text
                    )
                dialog.open()
                return super().on_touch_down(touch)

            elif self.ltype == 'услуга':
                dialog = MDDialog(
                    title="Информация:",
                    size_hint=(0.8, 0.3),
                    text_button_ok="Yes",
                    text=self.lservice_text
                    )
                return True    
            else:
                return True

        return super().on_touch_down(touch)
        '''
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
    dict_order = DictProperty()

    url_register = StringProperty('')
    url_listnews = StringProperty('')
    url_userinfo = StringProperty('')
    url_lmasters = StringProperty('')
    url_lservices = StringProperty('')
    url_lservicestime = StringProperty('')
    url_host = StringProperty('')
    url_getuserorders = StringProperty('')
    # url_stopmaster = StringProperty('') not supported
    url_createorder = StringProperty('')

    def __init__(self, **kvargs):
        super(BarberApp, self).__init__(**kvargs)
        #Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'
        Window.size = (480, 853)

        self.window = Window
        self.config = ConfigParser() 
        '''
        При переносе сервера на другой хост просто поменять значения self.url_host
        '''
        self.url_host = 'http://127.0.0.1:8000'  

        self.url_register = self.url_host+'/api/v1/register/'
        self.url_listnews = self.url_host+'/api/v1/getlistnewsuser/'
        self.url_userinfo = self.url_host+'/api/v1/getuserinfo/'
        self.url_lmasters = self.url_host+'/api/v1/getlistmasters/'
        self.url_lservices = self.url_host+'/api/v1/getlistservices/'
        self.url_lservicestime = self.url_host+'/api/v1/getlisttime/'
        # self.url_stopmaster = self.url_host+'/api/v1/getstoptime/'  в это й версии не используется
        self.url_createorder = self.url_host+'/api/v1/createorder/'
        self.url_getuserorders = self.url_host+'/api/v1/getorders/'

        self.lCard = False
        self.dict_order = {
            'master_id':None,
            'service_id':None,
            'servicetime_id':None,
            'date':None
        }

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

        self.date_init()
        self.get_list_masters()
        self.get_list_service()
        self.get_user_orders()
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
                instance_grid = self.manager.current_screen.ids.grid_card
                instance_grid.clear_widgets()
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

        elif request.url == self.url_createorder:
            if request.resp_status == 201:                               
                self.manager.current = 'base'
                self.get_list_masters() 
                self.get_list_service()
                self.clear_time_list()
                self.say_user('Заявка создана')
            else:
                self.say_user('Ошибка создания')

        elif request.url == self.url_getuserorders:
            self.write_list_userorders(result)

    def error_listnews(self, *args):
        a=0    

    def get_user_info(self):
        pass

    def get_user_orders(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_getuserorders, method='POST', req_headers=header, on_success=self.success_getdata)
    
    def get_list_service(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_lservices, method='POST', req_headers=header, on_success=self.success_getdata) 

    def get_list_servicetime(self):
        order_json = json.dumps(self.dict_order)
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_lservicestime, method='POST', req_headers=header, on_success=self.success_getdata, req_body=order_json) 

    def get_list_masters(self):
        
        order_json = json.dumps(self.dict_order)
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_lmasters, method='POST', req_headers=header, on_success=self.success_getdata, req_body=order_json)   

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
        listservice.clear_widgets()    
    
        for lService in result:
            listservice.add_widget(BarberTwoLineAvatarListItem(
                text = lService['bService'],
                secondary_text = 'Стоимость услуги: '+ lService['bPrice']+' руб.',
                lid = lService['id'],
                ltype = 'услуга',
                lservice_text = lService['bService_text']
            ))
    
    def write_list_master(self, result):
        listmaster = self.manager.screens[2].ids.master.ids.common_list
        listmaster.clear_widgets()

        l_on = False
        for lMaster in result:

            if lMaster['bDateEnd']:
                short_text = 'Отсутствует до '+datetime.strptime(lMaster['bDateEnd'], "%Y-%m-%d").strftime("%d %B %Y")
                mess_text  = 'Приносим свои извинения мастер отсутствует до '+datetime.strptime(lMaster['bDateEnd'], "%Y-%m-%d").strftime("%d %B %Y")
                l_on = True              
            else:
                short_text = 'Присутствует'
                mess_text  = lMaster['bMaster_text']    
                l_on = False

            listmaster.add_widget(MasterTwoLineAvatarListItem(
                text = lMaster['bMaster'],
                secondary_text = short_text,
                lid = lMaster['id'],
                ltype = 'мастер',
                lmaster_text = mess_text,
                lcheckstatus = l_on
                ))  

    def write_list_timetable(self, result):
        listtime = self.manager.screens[2].ids.timetable.ids.common_list
        listtime.clear_widgets()

        #Заполняем
        lcolor = [1,0,1,1] #default color
        l_on = False
        for lservicetime in result:
            if lservicetime['bTimeStatus'] == 'Запрещено':
                lcolor = [0.7,0,0,1]
                l_on = True
            elif lservicetime['bTimeStatus'] == 'Занято':
                lcolor = [0.2,0,0.8,1]
                l_on = True
            elif lservicetime['bTimeStatus'] == 'Свободно':
                lcolor = [0,0.7,0,1]
                l_on =False

            listtime.add_widget(TimeTwoLineAvatarListItem(
                text = 'Время оказания услуги: ' + lservicetime['bTime'],
                secondary_theme_text_color = 'Custom',
                secondary_text_color = lcolor,
                secondary_text = lservicetime['bTimeStatus'],
                lcheckstatus = l_on,
                lid = lservicetime['id'],
                ltype = 'время'
            ))
        self.ltest=listtime.height
    
    def write_list_userorders(self, result):
        listtime = self.manager.screens[2].ids.user_order.ids.common_list
        listtime.clear_widgets()

        for order in result:
            listtime.add_widget(OrderTwoLineAvatarListItem(
                text = '2',
                secondary_text = '1'
            ))

    def update_date(self):
        date_dialog = MDDatePicker(
        callback=self.set_date)
        date_dialog.open()
        
    def date_init(self):
        lcurrent_date = datetime.date(datetime.today())
        text_date = self.manager.screens[2].ids.master.ids.text_date
        text_date.text = lcurrent_date.strftime("%d %B %Y")
        self.dict_order['date'] = str(lcurrent_date)

    def set_date(self, *args):
        
        self.update_text_date(args[0])
        
        
        if self.date_comparison():
            self.dict_order['master_id'] = None
            self.dict_order['service_id'] = None
            self.get_list_masters()
            self.clear_time_list()
            if self.dict_order.get('master_id') and self.dict_order.get('date'):
                self.get_list_servicetime()
        
    def on_checkbox_active_m(self, lid, checkbox, value): 
        if value:
            self.dict_order['master_id'] = lid
            if self.date_comparison():
                if self.dict_order.get('master_id') and self.dict_order.get('date'):
                    self.get_list_servicetime()
                else:
                    self.clear_time_list() 
        else:
            self.dict_order['master_id'] = None
            self.clear_time_list() 

    def on_checkbox_active_s(self, lid, checkbox, value):
        if value:
            self.dict_order['service_id'] = lid
        else:
            self.dict_order['service_id'] = None  

    def on_checkbox_active_t(self, lid, checkbox, value):
        if value:
            self.dict_order['servicetime_id'] = lid
        else:
            self.dict_order['servicetime_id'] = None        

    def date_comparison(self):
        lcurrent_date = datetime.date(datetime.today())
        ldateorder = datetime.date(datetime.strptime(self.dict_order['date'],'%Y-%m-%d'))

        if ldateorder < lcurrent_date:
            self.say_user('Прошлый период выбрать нельзя')
            self.clear_time_list()
            self.update_text_date(datetime.date(datetime.today()))
            return False  
        elif not self.dict_order.get('master_id'):
            self.say_user('Выберите мастера') 
            self.clear_time_list()
            return False
        return True

    def update_text_date(self, ldate):
        text_date = self.manager.screens[2].ids.master.ids.text_date
        text_date.text = ldate.strftime("%d %B %Y")
        self.dict_order['date'] = str(ldate)
    
    def clear_time_list(self):
        self.manager.screens[2].ids.timetable.ids.common_list.clear_widgets()       
        
    def show_advanced_info(self, dialog_text):
        dialog = MDDialog(
            title="Информация:",
            size_hint=(0.8, 0.3),
            text_button_ok="Закрыть",
            text=dialog_text
            )
        dialog.open()

    def create_user_order(self):
        
        if not self.dict_order.get('master_id'):
            self.say_user('Выберите мастера')
            return False            
        elif not self.dict_order.get('service_id'):
            self.say_user('Выберите услугу')   
            return False
        elif not self.dict_order.get('servicetime_id'):
            self.say_user('Выберите время')
            return False

        order_json = json.dumps(self.dict_order)
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        resp = UrlRequest(self.url_createorder, 
                method='POST', 
                req_headers=header, 
                on_success=self.success_getdata, 
                req_body=order_json) 

if __name__ == '__main__':
    BarberApp().run()