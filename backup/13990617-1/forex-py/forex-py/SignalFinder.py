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
from providers.WallstreetFXsignals import WallstreetFXsignals
from providers.wolfofforexplus import wolfofforexplus
from providers.forexsignalzz import forexsignalzz



class BotEngine:
    def __init__(self,driver):
        self.driver = driver
        
    recentSignals={'forexsignalzz':0,'amirFX_signal':0,'FOR3X_SIGNAL':0,'AmirFx VIP signal':0,'Eagl777':0 , 'WallstreetFXsignals':0, 'wolfofforexplus':0}
    signalVendors={'a':  1}
    utils = Utils() 
    fileUtil = FileUtil()
    
    #{'Forex signals': 'GforexSignalsIr'}
    
    def setListOfVendors(self):
        self.signalVendors.update({'amirFX_signal':[ GforexSignalsIr(self.driver),'TAKE PROFIT']})
        self.signalVendors['FOR3X_SIGNAL'] = [FOR3X_SIGNAL(self.driver),'SL']
        self.signalVendors['AmirFx VIP signal'] = [GforexSignalsIr(self.driver),'TAKE PROFIT']
        self.signalVendors['signalTest']= [Eagl777(self.driver),'sl']
        self.signalVendors['Eagl777']= [Eagl777(self.driver),'sl']
        self.signalVendors['WallstreetFXsignals']= [WallstreetFXsignals(self.driver),'Trade Alert!']
        self.signalVendors['wolfofforexplus']= [wolfofforexplus(self.driver),'stop loss']
        self.signalVendors['forexsignalzz']=[forexsignalzz(self.driver),'new signal']
    
    def getNewMessage(self):
        coutner=1;
        while(coutner >0):
            try:
                sleep(1)

                for key in self.recentSignals:
                    try:
                        newMessages=self.find_last_update_time(key) #return last two messages webElement-time
                        
                        print('before getting time')
                        if newMessages == None or newMessages[0] == self.recentSignals[key]  :
                            print('repeated signal for '+key+' provider')
                            continue
                        else:
                            print('preparing new signal started in signalFinder!')
                            provider=self.signalVendors[key][0]
                            self.recentSignals[key] = newMessages[0]
    
                            sleep(2)
                            signalText=self.get_message(key,self.signalVendors[key][1]) 
                            if signalText != None :  
                                signalObjs= provider.createSignalDto(signalText,key) 
                                
                                if(signalObjs[0].enterPrice !=0):
                                    for signal in signalObjs.values(): 
                                        if(signal !=0):
                                            signal.vol = 0.01
                                            self.fileUtil.writeOnFile("s",signal)
                                        sleep(10)
                                else: 
                                    print('why here!!????')
                                    self.recentSignals[key]=0
                    except: # INNER TRY
                        print('in INNER except signalFinder: ')
                        self.recentSignals[key]=0
                        print(sys.exc_info()[0])
                        continue
                                   
            except : # outer try
                print('in OUTER except signalFinder: ')
                self.recentSignals[key]=0
                print(sys.exc_info()[0])
                continue
                    

    def find_last_update_time(self, chName):
        print('start finding last update time')
        c1=5
        while c1>0: 
            try: 
                elem= self.driver.find_element_by_xpath("//input[contains(@class,'im_dialogs_search_field')]")
                sleep(2)
                elem.clear()
                elem.send_keys(chName)
                break;
                sleep(1)
            except :
                sleep(2)
                c1-=1
                
        c2=5
        while c2>0: 
            try:      
                self.driver.find_elements_by_xpath("//div[@class='im_dialogs_col']//li[contains(@class,'im_dialog_wrap')]/a")[0].click()
                sleep(2)
                break;
            except :
                sleep(2)
                c2-=1
        c3=5      
        while c3>0:
            try:
                firstLastMessageTime = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//span[@class='im_message_date_text nocopy']")[-1].get_attribute('data-content')
                sleep(2)
                break;
            except:
                sleep(2)
                c3-=1
                
                
        try:
            secondLastMessageTime = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//span[@class='im_message_date_text nocopy']")[-2].get_attribute('data-content')
        except :
            secondLastMessageTime=""
            print('no second message')
        
        # providerCH=self.driver.find_elements_by_xpath("//span/ancestor::a[@class='im_dialog']")[0]
        # sleep(2)
        # last_time=providerCH.find_element_by_xpath("//div[@class='im_dialog_date']").text     #self.driver.find_elements_by_xpath("//span/ancestor::a[@class='im_dialog']//div[@class='im_dialog_date']")[0].text
        sleep(2)
        print('end of finding last update time')
        return [firstLastMessageTime ,secondLastMessageTime]


    def get_message(self, chName, identityStr):
        print('getting signal from '+chName+' started')
        try:
            result1=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']")[-1].text
            time1= self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer']//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[-1].get_attribute('data-content')
            results =[[result1,time1]]
            sleep(2)
            try:
                result2=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']")[-2].text
                time2= self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer']//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[-2].get_attribute('data-content')
                results.append([result2,time2])
            except :
                print(sys.exc_info()[0])
                print("not second message")
            
            try:
                result3 = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]")[-1].text
                time3   = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]//ancestor::div//span[contains(@class,'im_message_date_text')]")[-1].get_attribute('data-content')
                
                result4 = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]")[-2].text
                time4   = self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]//ancestor::div//span[contains(@class,'im_message_date_text')]")[-2].get_attribute('data-content')
                
                results.append([result3,time3])
                results.append([result3,time4])
            except:
                print(sys.exc_info()[0])
                print("not message in picture")

            myText=""
            
            for re in results :
                if( (re[0] != '')) :
                    if(str.find(re[0],identityStr) != -1):
                        if(self.utils.checkTime(re[1])):
                            print('getting signal from '+chName+' finished succesfully')
                            return re[0]

            print('getting signal from '+chName+' finished : no signal message!')
            return None
        except:
            print('getting signal from '+chName+' finished failed')
            return 'failed'




    
    
    
    
    
    
    
        