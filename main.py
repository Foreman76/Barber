# -*- coding: utf8 -*-
'''

= ['Primary', 'Secondary', 'Background', 'Surface', 'Error', 'On_Primary', 'On_Secondary', 'On_Background', 'On_Surface', 'On_Error']

'''
import re
import json
import sys
import os
import locale
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
from kivy.network.urlrequest import UrlRequest
from baseclas.startscreen import StartScreen
from kivymd.uix.list import TwoLineAvatarIconListItem, IRightBodyTouch, ILeftBody, ThreeLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from baseclas.cardnews import CardNews
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from kivy.config import Config
from kivy.clock import Clock
from baseclas.modalspinner import ModalSpinner
import certifi as cert



__version__ = '1.0.2'


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

class OrderLine(ThreeLineAvatarIconListItem):
    pass    

class BarberTwoLineAvatarListItem(TwoLineAvatarIconListItem):
    lid = NumericProperty()
    ltype = StringProperty('')
    lcheckstatus = BooleanProperty(False)
    lservice_text = StringProperty('')
    resp = ObjectProperty()

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
    resp = ObjectProperty()
    PhoneNumber = StringProperty('')
    Token = StringProperty('')
    FirstName = StringProperty('')
    #lCard = BooleanProperty(False)
    #lService = BooleanProperty(False)
    #lMaster  = BooleanProperty(False)
    #lServiceTime = BooleanProperty(False)
    #lTimeTable = StringProperty('')
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
    url_totaldata = StringProperty()
    screen = ObjectProperty()
    manager = ObjectProperty()
    progress = ObjectProperty()
    def __init__(self, **kvargs):
        super(BarberApp, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'
        #Window.size = (480, 853)

        self.window = Window
        self.config = ConfigParser() 
        '''
        При переносе сервера на другой хост просто поменять значения self.url_host
        '''
        self.url_host = 'https://barberstyle.int24.ru'  

        self.url_register = self.url_host+'/api/v1/register/'
        self.url_listnews = self.url_host+'/api/v1/getlistnewsuser/'
        self.url_userinfo = self.url_host+'/api/v1/getuserinfo/'
        self.url_lmasters = self.url_host+'/api/v1/getlistmasters/'
        self.url_lservices = self.url_host+'/api/v1/getlistservices/'
        self.url_lservicestime = self.url_host+'/api/v1/getlisttime/'
        # self.url_stopmaster = self.url_host+'/api/v1/getstoptime/'  в это й версии не используется
        self.url_createorder = self.url_host+'/api/v1/createorder/'
        self.url_getuserorders = self.url_host+'/api/v1/getorders/'
        self.url_totaldata = self.url_host+'/api/v1/gettotaldata/'

        self.dict_order = {
            'master_id':None,
            'service_id':None,
            'servicetime_id':None,
            'date':None
        }
        
    #def get_application_config(self):
    #   return super(BarberApp, self).get_application_config('~/.%(appname)s.ini')
    
    def events_program(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            pass
        elif keyboard in (282, 319):
            pass

        return True
    def build_config(self, config):
        #locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

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
        self.progress = ModalSpinner()
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        
        
        
        if self.Token:
            self.manager.current_screen.ids.btn_reg.text = 'Войти'
            self.manager.current_screen.ids.tel_text.text = self.PhoneNumber

        return self.screen

    def on_start(self):
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        self.date_init()
        #Config.set('kivy', 'keyboard_mode', 'systemandmulti')
        #print(locale.locale_alias)
        

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
           Clock.schedule_once(lambda dt: self.app_enter(), 1)           
                      
        else:
            PhoneNumber = self.manager.current_screen.ids.tel_text.text
            if  PhoneNumber == '+7(' or len(PhoneNumber) < 14:
                self.say_user('Введите правильный номер телефона') 
            else:
                self.get_register(PhoneNumber)
                
    def get_register(self, PhoneNumber):
        param_json = json.dumps({'phone':PhoneNumber})
        header = {'Content-type':'application/Json'}
        self.resp = UrlRequest(self.url_register, method='POST', 
                req_headers=header, on_success=self.success_getdata, req_body=param_json,
                on_error = self.error_request, ca_file=cert.where(), verify=True)

    def say_user(self, errText):
        toast(errText)
        
    def change_title_actionbar(self, text_title):
        if self.manager.current == 'base':
            self.screen.ids.action_bar.title = text_title
        elif self.manager.current == 'login': 
            self.screen.ids.action_bar.title = self.title
        elif self.manager.current == 'order': 
            self.screen.ids.action_bar.title = text_title      

    def app_enter(self):
        self.manager.current = 'base'
        self.progress.open()
        Clock.schedule_once(lambda dt:self.get_total_data(), .5)

    # Общая обработка сети    
    def success_getdata(self, request, result):
        
        if request.url == self.url_listnews:
            self.write_list_news(result)
             
        elif request.url == self.url_totaldata:
            self.write_list_news(result['news'])
            self.write_list_userorders(result['orders'])
            self.write_list_master(result['masters'])
            self.write_list_service(result['services'])
            self.progress.dismiss()
            
        elif request.url == self.url_lmasters:
            self.write_list_master(result)

        elif request.url == self.url_lservices:
            self.write_list_service(result)
        
        elif request.url == self.url_lservicestime:
            self.write_list_timetable(result)

        elif request.url == self.url_createorder:
            if request.resp_status == 201:                               
                self.manager.current = 'base'
                self.progress.open()
                Clock.schedule_once(lambda dt: self.get_total_data(), 1)
                self.clear_time_list()
                self.say_user('Заявка создана')
                self.clear_dict_order()
            else:
                self.say_user('Ошибка создания')
                self.clear_time_list()
                self.clear_dict_order()

        elif request.url == self.url_getuserorders:
            self.write_list_userorders(result)

        elif request.url == self.url_register:
            if request.resp_status == 200:
                keyvalue = {'token':result['token'], 'phonenumber':result['phone'], 'firstname':result['nUser']}
                self.write_value_in_config(keyvalue)
                self.read_value_from_config()
                self.say_user('Регистрация успешно пройдена')
                self.manager.current_screen.ids.btn_reg.text = 'Войти'
        else: 
            self.say_user('Ошибка')    
            


    def error_request(self, *args):
        self.say_user('Ошибка сети. Проверьте наличие интернет')  

    def get_user_info(self):
        pass

    def get_user_orders(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        self.resp = UrlRequest(self.url_getuserorders, method='POST', req_headers=header, 
        on_success=self.success_getdata, ca_file=cert.where(), verify=True)
    
    def get_list_service(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        self.resp = UrlRequest(self.url_lservices, method='POST', req_headers=header, 
        on_success=self.success_getdata, ca_file=cert.where(), verify=True) 

    def get_list_servicetime(self):
        order_json = json.dumps(self.dict_order)
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        self.resp = UrlRequest(self.url_lservicestime, method='POST', req_headers=header, 
        on_success=self.success_getdata, req_body=order_json, ca_file=cert.where(), verify=True) 

    def get_list_masters(self):
        
        order_json = json.dumps(self.dict_order)
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        self.resp = UrlRequest(self.url_lmasters, method='POST', req_headers=header, 
        on_success=self.success_getdata, req_body=order_json, ca_file=cert.where(), verify=True)   

    def get_list_news(self):
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        self.resp = UrlRequest(self.url_listnews, method='POST', req_headers=header, 
        on_success=self.success_getdata, ca_file=cert.where(), verify=True)

    def get_total_data(self):
        order_json = json.dumps(self.dict_order)
        header = {'Content-type':'application/Json', 'Authorization':'Token '+self.Token}
        self.resp = UrlRequest(self.url_totaldata, method='POST', 
        req_headers=header, on_success=self.success_getdata, 
        req_body=order_json,
        ca_file=cert.where(), verify=True)   

    def sys_exit(self):
        sys.exit(0)    

    def sm_on_enter(self):
        if self.manager.current == 'base':
            self.screen.ids.action_bar.right_action_items = [['arrow-right', lambda x: self.toggle_order_screen()]]
            #['exit-to-app', lambda x: self.sys_exit()]
        elif self.manager.current == 'order':
            self.screen.ids.action_bar.right_action_items = [['arrow-left', lambda x: self.toggle_base_screen()]]   

    def toggle_base_screen(self):
        self.manager.current = 'base'
        self.change_title_actionbar('Новости')

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
                text = 'Время услуги: ' + lservicetime['bTime'],
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
            listtime.add_widget(OrderLine(
                text = datetime.strptime(order['bOrderCreateDate'], "%Y-%m-%d").strftime("%d-%m-%Y")+' '+order['bOrderTimeService']['bTime'],
                secondary_text = 'Услуга: '+order['bOrderService']['bService'],
                tertiary_text = 'Мастер: '+order['bOrderMaster']['bMaster']
            ))

    def write_list_news(self, result):
        instance_grid = self.manager.screens[1].ids.grid_card
        instance_grid.clear_widgets()
        for news in result:
            instance_grid.add_widget(CardNews(
                path_image = self.directory+"/data/logonews.png",
                text_title = news['bTitleNews'],
                text_body  = news['bTextNews']
            ))

    def clear_dict_order(self):
        self.dict_order['master_id']=None
        self.dict_order['service_id']=None
        self.dict_order['servicetime_id']=None

    def update_date(self):
        date_dialog = MDDatePicker(
        callback=self.set_date)
        date_dialog.open()
        
    def date_init(self):
        lcurrent_date = datetime.date(datetime.today())
        self.manager.screens[2].ids.user_order.ids.text_date.text = lcurrent_date.strftime("%d %B %Y")
        self.manager.screens[2].ids.master.ids.text_date.text = lcurrent_date.strftime("%d %B %Y")
        self.manager.screens[2].ids.service.ids.text_date.text = lcurrent_date.strftime("%d %B %Y")
        self.manager.screens[2].ids.timetable.ids.text_date.text = lcurrent_date.strftime("%d %B %Y")
        
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
                    Clock.schedule_once(lambda dt: self.get_list_servicetime(), 0.5)
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
        self.manager.screens[2].ids.user_order.ids.text_date.text = ldate.strftime("%d %B %Y")
        self.manager.screens[2].ids.master.ids.text_date.text = ldate.strftime("%d %B %Y")
        self.manager.screens[2].ids.service.ids.text_date.text = ldate.strftime("%d %B %Y")
        self.manager.screens[2].ids.timetable.ids.text_date.text = ldate.strftime("%d %B %Y")
        self.dict_order['date'] = str(ldate)
    
    def clear_time_list(self):
        self.manager.screens[2].ids.timetable.ids.common_list.clear_widgets()       
        
    def show_advanced_info(self, dialog_text):
        dialog = MDDialog(
            title="Информация:",
            size_hint=(0.8, 0.5),
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
        self.resp = UrlRequest(self.url_createorder, 
                method='POST', 
                req_headers=header, 
                on_success=self.success_getdata, 
                req_body=order_json, ca_file=cert.where(), verify=True) 

if __name__ == '__main__':
    BarberApp().run()