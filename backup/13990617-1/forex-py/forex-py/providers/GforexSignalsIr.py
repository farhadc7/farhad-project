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
    
    def get_message(self, chName):
        print('getting signal from '+chName+' started')
        try:
            result1=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer' and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']")[-1].text
            time1= self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer']//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[-1].get_attribute('data-content')
            results =[[result1,time1]]
            sleep(2)
            try:
                result2=self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer') and not(contains(@class,'ng-hide'))]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']")[-2].text
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
                    if(str.find(re[0],"TAKE PROFIT") != -1):
                        if(self.utils.checkTime(re[1])):
                            print('getting signal from '+chName+' finished succesfully')
                            return re[0]

            print('getting signal from '+chName+' finished : no signal message!')
            return None
        except:
            print('getting signal from '+chName+' finished failed')
            return 'failed'
        
                        
        
      
    def checkTime(self, index):
        timeStr=self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer')]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[index].get_attribute('data-content')
        if(self.utils.stringToDate(timeStr)) :
            return True
        return False

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