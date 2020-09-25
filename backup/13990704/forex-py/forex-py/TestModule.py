# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 21:52:11 2020

@author: farhad
"""


import logging
import datetime
from datetime import datetime 
 

start= datetime.now()
logfileName=start.strftime("%Y-%m-%d-%H-%M-%S")+'.log'
logging.basicConfig(filename=logfileName,level=logging.DEBUG , format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.info("debug farahad")
logging.error('error error')