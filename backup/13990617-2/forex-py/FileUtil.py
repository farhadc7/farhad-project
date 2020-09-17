# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 16:17:26 2020

@author: farhad
"""
import sys
from SignalDto import SignalDto
from time import sleep
class FileUtil:
    
    
    message: str=""
    def  writeOnFile(self,fileDir : str, signal: SignalDto):
        print('writing to file started!')
        fileDir="C:\\Users\\farhad\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\Data\\test.txt"
        f=None
        c=0
        while (c<10): 
            try: 
                f=open(fileDir,'r+')
                self.message= f.read()
                sleep(1)
                break
            except :
                 c+=1
                 print(sys.exc_info()[0])
                 sleep(1)
        
        counter=10
        while(counter>0):
            if( str.find(self.message, 'ok') >=0 or self.message == ''):
                f.truncate(0)
                f.seek(0)
                f.write(self.createStrSignal(signal))
                sleep(1)
                f.close()
                break
            else:
                sleep(3)
                counter-=1
                print('cannot write')
        
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
        
        
        
    