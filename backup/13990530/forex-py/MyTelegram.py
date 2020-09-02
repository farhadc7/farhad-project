# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:34:10 2020

@author: farhad
"""
from time import sleep
from selenium import webdriver
from SignalDto import SignalDto
from datetime import date
from providers.GforexSignalsIr import GforexSignalsIr
from Utils import Utils


class BotEngine:
    def __init__(self,driver):
        self.driver = driver
        
    recentSignals={'Forex signals':0}
    signalVendors={'a': 1}
    utils = Utils() 
    
    #{'Forex signals': 'GforexSignalsIr'}
    
    def setListOfVendors(self):
        self.signalVendors.update({'Forex signals': GforexSignalsIr(self.driver)})
    
    def getNewMessage(self):
        coutner=1;
        while(coutner >0):
            try:
                sleep(5)

                for key in self.recentSignals:
                    print(key)
                    newLastTime=self.find_last_update_time(key)
                    if newLastTime == self.recentSignals[key]:
                        continue
                    else:
                        provider=self.signalVendors[key]
                        self.recentSignals[key] = newLastTime
                        signalText=provider.get_message(key, self.utils.extractTime(newLastTime))
                        if signalText != None :
                            provider.createSignalDto(signalText,newLastTime,key)
            except :
                continue
                    


    def find_last_update_time(self, chName):
        sleep(1)
        whichgroup=1
        
        last_time=self.driver.find_elements_by_xpath("//span[text()='Forex signals']/ancestor::a[@class='im_dialog']//div[@class='im_dialog_date']")[whichgroup].text
        return last_time





    
    
    
    
    
    
    
        