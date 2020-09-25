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
class forexsignalfactory:
    
    
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
                
                enter= line.split(' ')# forexsignalfactory:anger: SELL USDJPY @ 107.20
                signals[counter].symbol = enter[2]
                signals[counter].enter_type = 1 if enter[1] == "buy" else 2
                signals[counter].enterPrice = float(enter[4])
                
                
            elif line.find('tp') !=-1:
                if(signals[counter].tp == 0):
                    signals[counter].tp = float(line.split(' ')[3])
                elif(signals[counter].tp2 == 0):
                    signals[counter].tp2 = float(line.split(' ')[3])
                elif(signals[counter].tp3 == 0):
                    signals[counter].tp3 = float(line.split(' ')[3])
                    
        enter= signals[counter].enterPrice 
        diff= abs((enter- signals[counter].tp ))*(2/3)
        
        if signals[counter].enter_type == 1 :
             signals[counter].sl = enter - diff
        else:
            signals[counter].sl = enter + diff
        
        print('creating signalDto for '+chName+ ' finished')         
        return signals