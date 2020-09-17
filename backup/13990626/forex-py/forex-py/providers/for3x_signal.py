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
class FOR3X_SIGNAL:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
 

    
    
    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        msg = msg.lower().replace('limit','').replace('stop','')
        lines=str.splitlines(msg)
        signalDto= SignalDto()
        
        signalDto.provider = chName
        #signalDto.signalTime =self.utils.getDate(msgTime)
       
        enter= lines[0].split(" ")# first line is USDCAD BUY 1.3045
        
        signalDto.symbol = enter[0]
        signalDto.enter_type = 1 if enter[1] == "buy" else 2
        signalDto.enterPrice = float(enter[-1])
        
        signalDto.sl = float(lines[1].split(" ")[1]) #SL 1.2960
        signalDto.tp = float(lines[2].split(" ")[1]) #TP 1.2960
        

            
        print('creating signalDto for '+chName+ ' finished')         
        return {0:signalDto}