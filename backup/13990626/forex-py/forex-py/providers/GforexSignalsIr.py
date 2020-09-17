# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 23:57:40 2020

@author: farhad
"""
import sys
from SignalDto import SignalDto
from Utils import Utils
from time import sleep
from selenium import webdriver


class GforexSignalsIr:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    
 
        


    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        
        lines=str.splitlines(msg)
        signalDto= SignalDto()
        
        signalDto.provider = chName
 
        for item in lines :
            isFourDigit=False
                        
            posSymbol=str.find(item,'#')
            posBuy=str.find(item,'BUY')
            posSell=str.find(item,'SELL')
            posTP=str.find(item,':white_check_mark:')
            posSL=str.find(item,':x:')
            
            if posSymbol != -1 : 
                signalDto.symbol=item.replace('#','').replace(' ','')

            elif posBuy != -1 or posSell != -1:
                enter= item.split(' ')
                signalDto.enter_type = 1 if enter[0] == "BUY" else 2
                signalDto.enterPrice = enter[2]

            elif posSL != -1 :
                signalDto.sl =item.split(':')[2]
                    
            elif posTP != -1 :
                if(signalDto.tp == 0):
                    signalDto.tp = item.split(':')[2]
                elif(signalDto.tp2 == 0):
                    signalDto.tp2 = item.split(':')[2]
                elif(signalDto.tp3 == 0):
                    signalDto.tp3 = item.split(':')[2]
            
        print('creating signalDto for '+chName+ ' finished')         
        return {0:signalDto}