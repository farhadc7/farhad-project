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


class wolfofforexplus:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    
                        
        
      
    def checkTime(self, timeStr):
        #timeStr=self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer')]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[index].get_attribute('data-content')
        if(self.utils.stringToDate(timeStr)) :
            return True
        return False

    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        
        lines=str.splitlines(msg)
        signalDto= SignalDto()
        
        signalDto.provider = chName
 
        for line in lines :
            item=line.lower()
                        
            posSymbol=str.find(item,'#')
            posBuy=str.find(item.lower(),'in')          
            posTP=str.find(item.lower(),'take profit')
            posSL=str.find(item.lower(),'stop loss')
            
            if posSymbol != -1 : 
                signalDto.symbol=item.replace('#','').replace(' ','')

            elif posBuy != -1 :
                enter= item.replace(' ','').split(':')
                signalDto.enter_type = 1 if enter[2].lower().replace('in','') == "buy" else 2
                signalDto.enterPrice = float(enter[3])

            elif posSL != -1 :
                signalDto.sl =float(item.replace(' ','').split(':')[3])
                    
            elif posTP != -1 :
                if(signalDto.tp == 0):
                    signalDto.tp = float(item.replace(' ','').split(':')[3])
                elif(signalDto.tp2 == 0):
                    signalDto.tp2 = float(item.replace(' ','').split(':')[3])
                elif(signalDto.tp3 == 0):
                    signalDto.tp3 = float(item.replace(' ','').split(':')[3])
            
        print('creating signalDto for '+chName+ ' finished')         
        return {0:signalDto}