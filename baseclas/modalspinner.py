# -*- coding: utf-8 -*-

from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty

class ModalSpinner(ModalView):
    text_title = StringProperty('Загрузка...')