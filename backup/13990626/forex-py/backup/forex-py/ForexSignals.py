# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:41:35 2020

@author: farhad
"""


from selenium import webdriver
from time import sleep
from MyTelegram import BotEngine



testdic={"a":3,"b":5}
for key in testdic :
    print(testdic[key])

driver = webdriver.Firefox()
driver.get("https://web.telegram.org/#/im")
sleep(25)
telegrambot= BotEngine(driver)

telegrambot.getNewMessage()



