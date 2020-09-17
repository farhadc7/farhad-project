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


class FXMZ51:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    


    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        
        lines=str.splitlines(msg)
        signalDto= SignalDto()
        
        signalDto.provider = chName
 
        for line in lines :
            item=line.lower()
                        
            posSymbol=str.find(item.lower(),'@')        
            posTP=str.find(item.lower(),'t/')
            posSL=str.find(item.lower(),'s/')
            
            if posSymbol != -1 : 
                item = item.replace(" ","") #gbp/jpy sell @ 138.800
                signalDto.symbol= item[0:7].replace('/','')
                signalDto.enter_type = 1 if item[7:11] == "buy" else 2
                signalDto.enterPrice = float(item.split('@')[1])

                
            elif posSL != -1 : #s/l=140.004
                signalDto.sl =float(item.split('=')[1])
                
            elif posTP != -1 :
                if(signalDto.tp == 0):
                    signalDto.tp = float(item.split('=')[1])
                elif(signalDto.tp2 == 0):
                    signalDto.tp2 = float(item.split('=')[1])
                elif(signalDto.tp3 == 0):
                    signalDto.tp3 = float(item.split('=')[1])
            
        print('creating signalDto for '+chName+ ' finished')         
        return {0:signalDto}