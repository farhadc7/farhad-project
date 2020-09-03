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
        sleep(2)

        try:
            result1=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer']//div[@class='im_history_message_wrap']//div[@class='im_message_text']")[-1]
            sleep(2)
            try:
                
                result2=self.driver.find_elements_by_xpath("//div[@class='im_history_messages_peer']//div[@class='im_history_message_wrap']//div[@class='im_message_text']")[-2]
                results=[result1,result2]
            except :
                results=[result1]
                print(sys.exc_info()[0])
                print("not second message")

            checkText="سیگنال های رایگان امروز"
            myText=""
            
            for re in results :
                if( (re.text != '')) :
                    if( (str.find(re.text,checkText) == -1) ) :
                         if(str.find(re.text,"TAKE PROFIT") != -1):
                             print('getting signal from '+chName+' finished succesfully')
                             return re.text

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
 
        for item in lines :
            isFourDigit=False
                        
            posSymbol=str.find(item,'#')
            posBuy=str.find(item,'BUY')
            posTP=str.find(item,':white_check_mark:')
            posSL=str.find(item,':x:')
            
            if posSymbol != -1 : 
                signalDto.symbol=str.strip(item[1:]) # :7
                #isFourDigit=self.utils.checkDigits(signalDto.symbol)

            elif posBuy != -1 :
                signalDto.enterPrice = float(item[7:]) # :14

            elif posSL != -1 :
                signalDto.sl = float(item[3:]) # :10
                    
            elif posTP != -1 :
                if(signalDto.tp == 0):
                    signalDto.tp = float(item[18:]) # :25
                elif(signalDto.tp2 == 0):
                    signalDto.tp2 = float(item[18:]) # :25
                elif(signalDto.tp3 == 0):
                    signalDto.tp3 = float(item[18:]) # :25
            signalDto.vol=0.01
            
        print('creating signalDto for '+chName+ ' finished')         
        return signalDto