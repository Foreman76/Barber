# -*- coding: utf-8 -*-
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class CardNews(MDCard):
    text_title = StringProperty('Title')
    text_body  = StringProperty('Body news')