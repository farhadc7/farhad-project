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
from datetime import datetime
from Utils import Utils
from selenium.webdriver.common.keys import Keys
from FileUtil import FileUtil

from providers.GforexSignalsIr import GforexSignalsIr
from providers.Eagl777 import Eagl777
from providers.for3x_signal import FOR3X_SIGNAL
from providers.WallstreetFXsignals import WallstreetFXsignals
from providers.wolfofforexplus import wolfofforexplus
from providers.forexsignalzz import forexsignalzz
from providers.light_forex import light_forex
from providers.WSSignals import WSSignals
from providers.blue_forex_signals import blue_forex_signals
from providers.FXMZ51 import FXMZ51
from providers.professoroff import professoroff
from providers.signallforex123 import signallforex123
import logging



class BotEngine:
    def __init__(self,driver):
        self.driver = driver
        start= datetime.now()
        logfileName=start.strftime("%Y-%m-%d-%H-%M-%S")+'.log'
        logging.basicConfig(filename=logfileName,level=logging.INFO , format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
    recentSignals={'forexsignalzz':0,
                   'amirFX_signal':0,
                    'FOR3X_SIGNAL':0,
                    'Eagl777':0 ,
                    'WallstreetFXsignals':0,
                    'wolfofforexplus':0, 
                    'light_forex':0,
                    'FXMZ51':0,
                    'signallforex123':0,
                    'professoroff':0
                    
                    
                    
                    #'WSSignals':0 #,'blue_forex_signals':0
                    }
    #recentSignals={ 'blue_forex_signals':0}
    signalVendors={'a':  1}
    utils = Utils() 
    fileUtil = FileUtil()
    
    #{'Forex signals': 'GforexSignalsIr'}
    
    def setListOfVendors(self):
        self.signalVendors.update({'amirFX_signal':[ GforexSignalsIr(self.driver),'TAKE PROFIT']})
        self.signalVendors['FOR3X_SIGNAL'] = [FOR3X_SIGNAL(self.driver),'sl tp']
        self.signalVendors['signalTest']= [Eagl777(self.driver),'sl tp']
        self.signalVendors['Eagl777']= [Eagl777(self.driver),'sl tp']
        self.signalVendors['WallstreetFXsignals']= [WallstreetFXsignals(self.driver),'Trade Alert!']
        self.signalVendors['wolfofforexplus']= [wolfofforexplus(self.driver),'stop loss take profit']
        self.signalVendors['forexsignalzz']=[forexsignalzz(self.driver),'new signal']
        self.signalVendors['light_forex']=[light_forex(self.driver),'sl tp']
        self.signalVendors['FXMZ51'] = [FXMZ51(self.driver),'@ s/ t/']
        self.signalVendors['professoroff'] = [professoroff(self.driver),'tp sl']
        self.signalVendors['signallforex123'] = [signallforex123(self.driver),'tp sl']
        
        #self.signalVendors['blue_forex_signals']=[blue_forex_signals(self.driver),'at.']
        #self.signalVendors['WSSignals']=[WSSignals(self.driver),'sl tp']
        #self.signalVendors['AmirFx VIP signal'] = [GforexSignalsIr(self.driver),'TAKE PROFIT']

    def getNewMessage(self):
        coutner=1;
        while(coutner >0):
            try:
                sleep(1)

                for key in self.recentSignals:
                    try:     
                        newMessages=self.find_last_update_time(key) #return last two messages webElement-time
                        
                        print('before getting time')
                        logging.info('%s new update is %s last update is %s',
                                      key,newMessages[0], self.recentSignals[key])
                        
                        
                        if newMessages == None or newMessages[0] == self.recentSignals[key]  :
                            print('repeated signal for '+key+' provider')
                            logging.info('%s repeated signal',key)
                            continue
                        else:
                            print('%s preparing new signal started in signalFinder!',key)
                            logging.info('%s get new signal',key)
                            provider=self.signalVendors[key][0]
                            self.recentSignals[key] = newMessages[0]
    
                            sleep(2)
                            signalTxtArr=self.get_message(key,self.signalVendors[key][1]) 
                            if signalTxtArr != [] : 

                                for sigTxt in signalTxtArr : # when more than one valid message founded
                                     logging.info('%s signal text is : %s',key,sigTxt )
                                     signalObjs= provider.createSignalDto(sigTxt,key)

                                     if(signalObjs[0].enterPrice !=0):
                                        for signal in signalObjs.values(): # when more than one signal exists in a message 
                                            if(signal !=0):
                                                signal.vol = 0.01
                                                self.fileUtil.writeOnFile("s",signal)
                                            sleep(10)
                                     else: 
                                        logging.error('%s why here!!',key)
                                        print('why here!!????')
                                        self.recentSignals[key]=0
                    except IndexError: # INNER TRY
                        print('in INNER index error signalFinder: %s',key)
                        logging.error('%s in INNER except signalFinder: %s',key,sys.exc_info()[0])
                        self.recentSignals[key]=0
                        print(sys.exc_info()[0])
                        continue

                    except :
                        print('in INNER expect error signalFinder: %s',key)
                        print(sys.exc_info()[0])
                        continue
                        
                                   
            except : # outer try
                print('in OUTER except signalFinder: ')
                self.recentSignals[key]=0
                print(sys.exc_info()[0])
                logging.error('%s in outer except signalFinder: %s',key,sys.exc_info()[0])
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
                sleep(5)
                break;

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
                firstLastMessageTime = self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(contains(@class,'ng-hide'))]//span[@class='im_message_date_text nocopy']")[-1].get_attribute('data-content')
                if firstLastMessageTime == '8:07:48 AM' :
                    print('aaaaaa')
                sleep(2)
                break;
            except:
                sleep(2)
                c3-=1
                
                
        try:
            secondLastMessageTime = self.driver.find_elements_by_xpath("//div[@class = 'im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(contains(@class,'ng-hide'))]//span[@class='im_message_date_text nocopy']")[-2].get_attribute('data-content')
            if firstLastMessageTime == '8:07:48 AM' :
                    print('aaaaaa')
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
        logging.info('%s getting signal message started',chName)
        try:
            result1=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']")[-1].text
            time1= self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//span[contains(@class,'im_message_date_text')]")[-1].get_attribute('data-content')
            results =[[result1,time1]]
            sleep(2)
            try:
                result2=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']")[-2].text
                time2= self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//span[contains(@class,'im_message_date_text')]")[-2].get_attribute('data-content')
                results.append([result2,time2])
            except :
                print(sys.exc_info()[0])
                print("not second message")
            
            try:
                result3 = self.driver.find_elements_by_xpath("//div[@class = 'im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]")[-1].text
                time3   = self.driver.find_elements_by_xpath("//div[@class ='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]//ancestor::div[contains(@class,'im_content_message_wrap')]//span[contains(@class,'im_message_date_text')]")[-1].get_attribute('data-content')
                
                result4 = self.driver.find_elements_by_xpath("//div[@class = 'im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]")[-2].text
                time4   = self.driver.find_elements_by_xpath("//div[@class ='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap') and not(@style='display: none;')]//div[contains(@class,'im_message_media')]//div[@class='im_message_photo_caption' and not(@style='display: none;')]//ancestor::div[contains(@class,'im_content_message_wrap')]//span[contains(@class,'im_message_date_text')]")[-2].get_attribute('data-content')
                
                results.append([result3,time3])
                results.append([result4,time4])
            except:
                print(sys.exc_info()[0])
                print("not message in picture")

            signalArr  = []
            
            for re in results :
                if( (re[0] != '')) :
                    if( self.utils.find_all(re[0].lower(),identityStr.lower()) ==True):
                        
                        if(self.utils.checkTime(re[1])):
                            print('getting signal from '+chName+' finished succesfully')
                            
                            logging.info('%s getting signal message successfully ended',chName)
                            #return re[0]
                            signalArr.append(re[0])
                            

            print('getting signal from '+chName+' finished!')
            #return None
            return signalArr
        except:
            print('getting signal from '+chName+' finished failed')
            return 'failed'




    
    
    
    
    
    
    
        