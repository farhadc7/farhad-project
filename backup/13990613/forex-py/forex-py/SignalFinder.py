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
from selenium.webdriver.common.keys import Keys
from FileUtil import FileUtil


class BotEngine:
    def __init__(self,driver):
        self.driver = driver
        
    recentSignals={'amirFX_signal':0}
    signalVendors={'a': 1}
    utils = Utils() 
    fileUtil = FileUtil()
    
    #{'Forex signals': 'GforexSignalsIr'}
    
    def setListOfVendors(self):
        self.signalVendors.update({'amirFX_signal': GforexSignalsIr(self.driver)})
    
    def getNewMessage(self):
        coutner=1;
        while(coutner >0):
            try:
                sleep(5)

                for key in self.recentSignals:
                    newLastTime=self.find_last_update_time(key)
                    
                    if newLastTime[1] == self.recentSignals[key] or newLastTime == None:
                        print('repeated signal for '+key+' provider')
                        continue
                    else:
                        print('preparing new signal started in signalFinder!')
                        provider=self.signalVendors[key]
                        self.recentSignals[key] = newLastTime[1]
                        newLastTime[0].click()
                        # self.driver.find_elements_by_xpath("//span[text()='{0}']/ancestor::a[@class='im_dialog']"
                        #                                    .format(self.signalVendors[key]))[0].click()
                        sleep(1)
                        signalText=provider.get_message(key,'3:50' ) #commented for test  self.utils.extractTime(newLastTime[1])
                        if signalText != None :  
                            signalObj= provider.createSignalDto(signalText,'3:50',key) #commented for test newLastTime[1]
                            if(signalObj.enterPrice !=0):
                                self.fileUtil.writeOnFile("s",signalObj)  
                            else: 
                                self.recentSignals[key]=0
                                   
            except :
                continue
                    


    def find_last_update_time(self, chName):
        sleep(1)
        whichgroup=1
        
        elem= self.driver.find_element_by_xpath("//input[contains(@class,'im_dialogs_search_field')]")
        elem.clear()
        elem.send_keys(chName)
        sleep(2)
        providerCH=self.driver.find_elements_by_xpath("//span/ancestor::a[@class='im_dialog']")[0]
        sleep(2)
        last_time=providerCH.find_element_by_xpath("//div[@class='im_dialog_date']").text     #self.driver.find_elements_by_xpath("//span/ancestor::a[@class='im_dialog']//div[@class='im_dialog_date']")[0].text
        
        #if len(last_time) == 3 :
         #   return None   # commented for test
        
        return [providerCH, last_time]





    
    
    
    
    
    
    
        