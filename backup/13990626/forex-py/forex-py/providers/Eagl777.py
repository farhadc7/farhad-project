# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 23:57:40 2020

@author: farhad
"""
from SignalDto import SignalDto
from Utils import Utils
from time import sleep
from selenium import webdriver

"""FOR3X_SIGNAL"""
class Eagl777:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    
    
    
    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        lines=str.splitlines(msg)
        signals={}
        counter =-1
        for line in lines :
            
            if line.lower().find('buy') !=-1 or line.lower().find('sell') !=-1:
                counter+=1
                signals[counter]= SignalDto()
                signals[counter].provider = chName
                
                enter= line.split(" ")# first line is Euraud Buy at 1.62000
                signals[counter].symbol = str.upper(enter[0])
                signals[counter].enter_type = 1 if str.upper(enter[1]) == "BUY" else 2
                try:
                    signals[counter].enterPrice = float(enter[4])
                except :
                    signals[counter].enterPrice = float(enter[3])
                
            elif line.lower().find('sl') !=-1 :
                signals[counter].sl = float(line.lower().replace('sl','').replace(' ',''))
            elif line.lower().find('tp') !=-1:
                signals[counter].tp = float(line.lower().replace('tp','').replace(' ',''))
                

            
        print('creating signalDto for '+chName+ ' finished')         
        return signals