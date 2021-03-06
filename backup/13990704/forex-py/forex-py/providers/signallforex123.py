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
class signallforex123:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    
    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        lines=str.splitlines(msg)
        signals={}
        counter =-1
        for line in lines :
            line =line.lower()
            
            if line.find('buy') !=-1 or line.find('sell') !=-1:
                counter+=1
                signals[counter]= SignalDto()
                signals[counter].provider = chName
                
                enter= line.replace('limit ','').split(" ")# Gold buy limit 1922.00
                signals[counter].symbol = enter[0]
                signals[counter].enter_type = 1 if enter[1] == "buy" else 2
                signals[counter].enterPrice = float(enter[2])
                
            elif line.find('sl') !=-1 : #Tp1:1.1840
                signals[counter].sl =line.replace(' ','').split(':')[1]
                
            elif line.find('tp') !=-1:
                if(signals[counter].tp == 0):
                    signals[counter].tp = float(line.replace(' ','').split(':')[1])
                elif(signals[counter].tp2 == 0):
                    signals[counter].tp2 = float(line.replace(' ','').split(':')[1])
                elif(signals[counter].tp3 == 0):
                    signals[counter].tp3 = float(line.replace(' ','').split(':')[1])
                

            
        print('creating signalDto for '+chName+ ' finished')         
        return signals