# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 23:57:40 2020

@author: farhad
"""
from SignalDto import SignalDto
from Utils import Utils
from time import sleep
from selenium import webdriver

"""FOR3X_SIGNAL"""
class FOR3X_SIGNAL:
    
    
    def __init__(self,driver):
        self.driver= driver

    utils= Utils()
    
    def get_message(self, chName):
        print('getting signal from '+chName+' started')

        try:
            result=self.driver.find_elements_by_xpath("//div[@class='im_history_col']//div[@class='im_history_messages_peer' and not(@style='display: none;')]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text' and not(@style='display: none;')]")[-1]
            time1= self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer']//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[-1].get_attribute('data-content')
            sleep(2)

            checkText1="SL"
            checkText2="TP"
            myText=""
            
            if( (result.text != '')) :
                if( (str.find(result.text,checkText1) != -1) ) :
                     if(str.find(result.text,checkText2) != -1):
                         if(self.utils.checkTime(time1)):
                             print('getting signal from '+chName+' finished succesfully')
                             return result.text
                         
            print('getting signal from '+chName+' finished : no signal message!')
            return None
        except:
            print('getting signal from '+chName+' finished failed')
            return 'failed'
                
                    
            
        #     if(str.find(results[-1].text,checkText) != -1):
        #         myText= results[-2].text
        #     else :
        #         myText= results[-1].text
        #     if(str.find(myText,"TAKE PROFIT") != -1):
        #        return myText
        #     else:
        #        return None
        # except:
        #     return None

    
    
    def createSignalDto(self,msg,chName):
        print('creating signalDto for '+chName+ ' started')
        lines=str.splitlines(msg)
        signalDto= SignalDto()
        
        signalDto.provider = chName
        #signalDto.signalTime =self.utils.getDate(msgTime)
       
        enter= lines[0].split(" ")# first line is USDCAD BUY 1.3045
        
        signalDto.symbol = enter[0]
        signalDto.enter_type = 1 if enter[1] == "BUY" else 2
        signalDto.enterPrice = float(enter[2])
        
        signalDto.sl = float(lines[1].split(" ")[1]) #SL 1.2960
        signalDto.tp = float(lines[2].split(" ")[1]) #TP 1.2960
        

            
        print('creating signalDto for '+chName+ ' finished')         
        return {0:signalDto}