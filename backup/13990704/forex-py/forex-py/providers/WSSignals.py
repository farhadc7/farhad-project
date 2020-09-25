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


class WSSignals:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    

    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        
        signalDto= SignalDto()
        signalDto.provider = chName
        
        lines=str.splitlines(msg)
        for line in lines :
            
            item=line.lower()            
            posEnter=str.find(item,'buy')+str.find(item,'sell')
            posTP=str.find(item,'tp')
            posSL=str.find(item,'sl')
            item= item.split(' ')
            
            if posEnter !=-2 : 
                signalDto.symbol=item[0]
                signalDto.enter_type = 1 if item[2] == "buy" else 2
                signalDto.enterPrice = item[-1]

            elif posSL != -1 :
                signalDto.sl =item[1]
                    
            elif posTP != -1 :
                if(signalDto.tp == 0):
                    signalDto.tp = item[1]
                elif(signalDto.tp2 == 0):
                    signalDto.tp2 = item[1]
                elif(signalDto.tp3 == 0):
                    signalDto.tp3 = item[1]
            
        print('creating signalDto for '+chName+ ' finished')         
        return {0:signalDto}