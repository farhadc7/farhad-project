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


class BotEngine:
    def __init__(self,driver):
        self.driver = driver
        
    signalVendors={'Forex signals':0}
    signalVendorsClassName={'Forex signals','GforexSignalsIr'}
    
    def getNewMessage(self):
        coutner=1;
        while(coutner >0):
            sleep(5)
            
            for key in self.signalVendors:
                print(key)
                newLastTime=self.find_last_update_time(key)
                if newLastTime == self.signalVendors[key]:
                    break
                else:
                    self.signalVendors[key] = newLastTime
                    provider =exec(self.signalVendorsClassName[key]+"("+self.driver+")")
                    signalText=provider.get_message(key, self.extractTime(newLastTime))
                    if signalText != None :
                        provider.createSignalDto(signalText,newLastTime,key)
                        
                    
                    
    def createSignalDto(self,msg,msgTime,chName):
        lines=str.splitlines(msg)
        signalDto= SignalDto()
        
        signalDto.provider = chName
        signalDto.signalTime =self.getDate(msgTime)
       
        
        for item in lines :
            isFourDigit=False
                        
            posSymbol=str.find(item,'#')
            posBuy=str.find(item,'BUY')
            posTP=str.find(item,':white_check_mark:')
            posSL=str.find(item,':x:')
            
            if posSymbol != -1 :
                signalDto.symbol=item[1:7]
                isFourDigit=self.checkDigits(signalDto.symbol)

            elif posBuy != -1 :
                if isFourDigit == False:
                    signalDto.enterPrice = float(item[7:14])
                else:
                    signalDto.enterPrice = float(item[7:13])
            
            elif posSL != -1 :
                if isFourDigit == False:
                    signalDto.sl = float(item[3 : 10])
                else:
                    signalDto.sl = float(item[3:9])
                    
            elif posTP != -1 :
                if isFourDigit == False:
                    signalDto.tp = float(item[18 : 25])
                else:
                    signalDto.tp.append(float(item[18:24])) 
                    
        return signalDto
            
                
                
        
    def checkDigits(self,symbol):
        return True
            
                

    def find_last_update_time(self, chName):
        sleep(1)
        
        last_time=self.driver.find_elements_by_xpath("//span[text()='Forex signals']/ancestor::a[@class='im_dialog']//div[@class='im_dialog_date']")[0].text
        return last_time
    
    def get_message(self, chName,newTime):
        newTime='5:08'
        sleep(1)
        self.driver.find_elements_by_xpath("//span[text()='{0}']/ancestor::a[@class='im_dialog']".format(chName))[0].click()
        try:
            results=self.driver.find_elements_by_xpath("//span[contains(@data-content,'{0}')]//ancestor::div[contains(@class,'im_content_message_wrap im_message_in')]//div[@class='im_message_text']".format(newTime))
            
            checkText="سیگنال های رایگان امروز"
            myText=""
            
            if(str.find(results[-1].text,checkText) != -1):
                myText= results[-2].text
            else :
                myText= results[-1].text
            if(str.find(myText,"TAKE PROFIT") != -1):
               return myText
            else:
               return None
        except:
            return None

    
    def extractTime(self,t):
       return str.split(t," ")[0]
   
    def getDate(self, signalTime):
        today=date.today()
        today.strftime("%d/%m/%Y")
        return today + " : "+signalTime
        
    


    
    
    
    
    
    
    
        