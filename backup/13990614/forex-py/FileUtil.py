# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 16:17:26 2020

@author: farhad
"""

from SignalDto import SignalDto
from time import sleep
class FileUtil:
    
    message: str=""
    def  writeOnFile(self,fileDir : str, signal: SignalDto):
        print('writing to file started!')
        fileDir="C:\\Users\\farhad\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\Data\\test.txt"
        f=open(fileDir,'r+')
        self.message= f.read()
        
        counter=10
        while(counter>0):
            if( str.find(self.message, 'ok') or self.message == None):
                f.truncate(0)
                f.seek(0)
                f.write(self.createStrSignal(signal))
                f.close()
                break
            else:
                sleep(1)
                counter+=1
        
        if(counter==0):
            return

    
    def createStrSignal(self,signal : SignalDto):
        a=""
        a+= str(signal.enter_type)
        a+=','
        a+=signal.symbol
        a+=','
        a+= signal.provider
        a+=','
        a+= str(signal.enterPrice)
        a+=','
        a+= str(signal.sl)
        a+=','
        a+= str(signal.tp)
        a+=','
        a+= str(signal.tp2)
        a+=','
        a+= str(signal.tp3)
        a+=','
        a+=str(signal.close)
        a+=','
        a+= str(signal.vol)
        a+=','
        a+= str(signal.newVol)
        
        print('writing to file finished')
        
        return a
        
        
        
    