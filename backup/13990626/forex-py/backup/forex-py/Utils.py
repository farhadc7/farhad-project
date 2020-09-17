# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 23:05:42 2020

@author: farhad
"""
from datetime import date

class Utils:
    def checkDigits(self,symbol):
        return True
    
    def extractTime(self,t):
        return str.split(t," ")[0]
   
    def getDate(self, signalTime):
        today=date.today()
        today.strftime("%d/%m/%Y")
        return today + " : "+signalTime
    