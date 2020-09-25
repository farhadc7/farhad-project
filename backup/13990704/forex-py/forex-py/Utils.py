# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 23:05:42 2020

@author: farhad
"""

import datetime

class Utils:
    def checkDigits(self,symbol):
        return True
    
    def extractTime(self,t):
        return str.split(t," ")[0]
    
    def priorMinute(self, timeStr):
           temp= str.split(timeStr,':')
           a=int(temp[1]) - 1
           temp[1] = str(a)
           return temp[0] + ':' + temp[1]
   
    def getDate(self, signalTime):
        today=datetime.date.today()
        
        return today.strftime(today.strftime("%Y/%m/%D")) + " : "+signalTime
    
    def stringToDate(self, strDate):
        date_time_obj = datetime.datetime.strptime(strDate, '%I:%M:%S %p')
        min_added =datetime.timedelta(minutes=120)
        check_date = (date_time_obj + min_added).time()
        real_time = date_time_obj.time()
        now_time = datetime.datetime.now().time()
        
        check_date_validation = now_time <= check_date
        #if now_time.hour > check_date.hour :
           # check_date_validation = True for 0 hour must make think
        
        if( now_time >= real_time and check_date_validation) :
            return True
        else:
            print('time is not ok !')
            return False
        
    def checkTime(self, timeStr):
        #timeStr=self.driver.find_elements_by_xpath("//div[contains(@class,'im_history_messages_peer')]//div[contains(@class,'im_history_message_wrap')]//div[@class='im_message_text']//ancestor::div//span[contains(@class,'im_message_date_text')]")[index].get_attribute('data-content')
        if(self.stringToDate(timeStr)) :
            return True
        return False
    
    def find_all(self, obj, subStr):
        res: bool = True
        subArr= subStr.split(' ')
        for s in subArr:
            if(obj.find(s) ==-1):
                res = False
        return res
                
                
    