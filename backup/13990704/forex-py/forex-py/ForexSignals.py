# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:41:35 2020

@author: farhad
"""

from time import sleep
from SignalFinder import BotEngine
from Utils import Utils
from datetime import date
from datetime import datetime
from mql.SimpleSendSignal2 import SimpleSendSignal2
from mql.SimpleSendSignal import SimpleSendSignal
from SignalDto import SignalDto
from selenium import webdriver
import logging

# today = date.today()
# print(today.strftime("%d/%m/%Y") + "aaa")

# utils = Utils()

# print(utils.extractTime("sdaf adsf"))
# start= datetime.now()
# logfileName=start.strftime("%Y-%m-%d-%H-%M-%S")+'.log'
# logging.basicConfig(filename=logfileName,level=logging.INFO , format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# logging.info('project started!')
driver = webdriver.Firefox()
driver.get("https://web.telegram.org/#/im")
sleep(25)


telegrambot = BotEngine(driver)
telegrambot.setListOfVendors()

telegrambot.getNewMessage()

# signal= SignalDto();
# signal.provider = "forex-signal"
# signal.tp=500
# signal.sl=500
# signal.symbol='EURUSD'
# signal.enterPrice =1.20850
# signal.lots=.01
# signal.enter_type='buy'


# a=SimpleSendSignal();
# test=('a',signal)
# #print("end response: ")
# #print(a._run_(test))

# b= SimpleSendSignal();
# b._trader_(signal)



