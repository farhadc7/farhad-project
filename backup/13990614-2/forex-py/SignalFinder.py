# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:34:10 2020

@author: farhad
"""
import sys
from time import sleep
from selenium import webdriver
from SignalDto import SignalDto
from datetime import date
from Utils import Utils
from selenium.webdriver.common.keys import Keys
from FileUtil import FileUtil

from providers.GforexSignalsIr import GforexSignalsIr
from providers.Eagl777 import Eagl777
from providers.FOR3X_SIGNAL import FOR3X_SIGNAL



class BotEngine:
    def __init__(self,driver):
        self.driver = driver
        
    recentSignals={'signalTest':0} #'amirFX_signal':0,'FOR3X_SIGNAL':0,'AmirFx VIP signal':0,'Eagl777':0
    signalVendors={'a':  1}
    utils = Utils() 
    fileUtil = FileUtil()
    
    #{'Forex signals': 'GforexSignalsIr'}
    
    def setListOfVendors(self):
        self.signalVendors.update({'amirFX_signal': GforexSignalsIr(self.driver)})
        self.signalVendors['FOR3X_SIGNAL'] = FOR3X_SIGNAL(self.driver)
        self.signalVendors['AmirFx VIP signal'] = GforexSignalsIr(self.driver)
        self.signalVendors['signalTest']= Eagl777(self.driver)
        self.signalVendors['Eagl777']= Eagl777(self.driver)
    
    def getNewMessage(self):
        coutner=1;
        while(coutner >0):
            try:
                sleep(1)

                for key in self.recentSignals:
                    newMessages=self.find_last_update_time(key) #return last two messages webElement-time
                    
                    
                    if newMessages == None or newMessages[0] == self.recentSignals[key]  :
                        print('repeated signal for '+key+' provider')
                        continue
                    else:
                        print('preparing new signal started in signalFinder!')
                        provider=self.signalVendors[key]
                        self.recentSignals[key] = newMessages[0]

                        sleep(2)
                        signalText=provider.get_message(key) 
                        if signalText != None :  
                            signalObjs= provider.createSignalDto(signalText,key) 
                            #signalObj.vol = 0.01
                            if(signalObjs[0].enterPrice !=0):
                                for signal in signalObjs.values():
                                    if(signal !=0):
                                        self.fileUtil.writeOnFile("s",signal)
                                    sleep(2)
                            else: 
                                print('why here!!????')
                                self.recentSignals[key]=0
                                   
            except :
                print('in except signalFinder: ')
                print(sys.exc_info()[0])
                continue
                    

    def find_last_update_time(self, chName):
        elem= self.driver.find_element_by_xpath("//input[contains(@class,'im_dialogs_search_field')]")
        elem.clear()
        elem.send_keys(chName)
        sleep(4)
        self.driver.find_elements_by_xpath("//div[@class='im_dialogs_col']//li[contains(@class,'im_dialog_wrap')]/a")[0].click()
        sleep(2)
        firstLastMessageTime = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer')]//div[contains(@class,'im_history_message_wrap')]//span[@class='im_message_date_text nocopy']")[-1].get_attribute('data-content')
        sleep(2)
        try:
            secondLastMessageTime = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer')]//div[contains(@class,'im_history_message_wrap')]//span[@class='im_message_date_text nocopy']")[-2].get_attribute('data-content')
        except :
            secondLastMessageTime=""
            print('no second message')
        
        # providerCH=self.driver.find_elements_by_xpath("//span/ancestor::a[@class='im_dialog']")[0]
        # sleep(2)
        # last_time=providerCH.find_element_by_xpath("//div[@class='im_dialog_date']").text     #self.driver.find_elements_by_xpath("//span/ancestor::a[@class='im_dialog']//div[@class='im_dialog_date']")[0].text
        # sleep(2)
        
        return [firstLastMessageTime ,secondLastMessageTime]





    
    
    
    
    
    
    
        