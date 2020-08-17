# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 19:39:33 2020

@author: farhad
"""



# import os

# #############################################################################
# #############################################################################
# _path = '<PATH_TO_ROOT_DIR_CONTAINING_DWX_ZEROMQ_CONNECTOR>'
# os.chdir(_path)
#############################################################################
#############################################################################

from pandas import Timedelta, to_datetime
from threading import Thread, Lock
from time import sleep
import random
from SignalDto import SignalDto
from mql.DWX_ZeroMQ_Connector_v2_0_1_RC8 import DWX_ZeroMQ_Connector
from mql.MODULES.DWX_ZMQ_Execution import DWX_ZMQ_Execution
from mql.MODULES.DWX_ZMQ_Reporting import DWX_ZMQ_Reporting





class SimpleSendSignal2():

    
    def __init__(self):
        self._lock = Lock()
        self._zmq = DWX_ZeroMQ_Connector(_verbose=False)
        # Modules
        self._execution = DWX_ZMQ_Execution(self._zmq)
        self._reporting = DWX_ZMQ_Reporting(self._zmq)


    ##########################################################################
    
    def _run_(self,a:tuple):
        signalDto=a[1]
        
        """
        Logic:
            
            For each symbol in self._symbols:
                
                1) Open a new Market Order every 2 seconds
                2) Close any orders that have been running for 10 seconds
                3) Calculate Open P&L every second
                4) Plot Open P&L in real-time
                5) Lot size per trade = 0.01
                6) SL/TP = 10 pips each
        """
        
        _t = Thread(name="{}_Trader".format(signalDto.symbol),
                    target=self._trader_, args=(a,"a"))
        
        _t.daemon = True
        _t.start()
        
        print('[{}_Trader] Alright, here we go.. Gerrrronimooooooooooo!  ..... xD'.format(signalDto.symbol))
        
        #self._traders.append(_t)
        
        print('\n\n+--------------+\n+ LIVE UPDATES +\n+--------------+\n')
        
        # _verbose can print too much information.. so let's start a thread
        # that prints an update for instructions flowing through ZeroMQ
        self._updater_ = Thread(name='Live_Updater',
                               target=self._updater_,
                               args=(.01,))
        
        self._updater_.daemon = True
        self._updater_.start()
        
    ##########################################################################
    
    def _updater_(self, _delay=0.1):
        
        while True:
            
            try:
                # Acquire lock
                self._lock.acquire()
                
                print('farhads: \r{}'.format(str(self._zmq._get_response_())), end='', flush=True)
                
            finally:
                # Release lock
                self._lock.release()
        
            sleep(2)
            
    ##########################################################################
    
    def _trader_(self,t,b):
       print(t[0])
       signalDto=t[1]
        
       while True:
           
           try:
                  # Acquire lock
            self._lock.acquire()
             
            _default_order = self._zmq._generate_default_order_dict()
            _default_order['_symbol'] = signalDto.symbol
            _default_order['_lots'] = signalDto.lots
            _default_order['_SL'] = signalDto.sl
            _default_order['_TP'] = signalDto.tp
            _default_order['_comment'] = '{0}_Trader_{1}'.format(signalDto.provider,signalDto.symbol)
            _default_order['_action'] = 'OPEN'
            _default_order['_price'] = signalDto.enterPrice
            
            """
            https://docs.mql4.com/trading/ordersend
            
            Default Order:
            --
            {'_action': 'OPEN',
             '_type': 0,
             '_symbol': EURUSD,
             '_price':0.0,
             '_SL': 100,                     # 10 pips
             '_TP': 100,                     # 10 pips
             '_comment': 'EURUSD_Trader',
             '_lots': 0.01,
             '_magic': 123456}
            
            """
            hd:dict
            counter=0
            self._zmq._DWX_MTX_SUBSCRIBE_MARKETDATA_(signalDto.symbol)
            print("subscirbed")
            while counter !=10 :
                try:
                    print("subscribe")
                    sleep(10)
                    print('after wait')
                    if self._zmq._valid_response_() :
                        print(self._zmq._get_response_())
                        last_data= list(self._zmq._Market_Data_DB[signalDto.symbol].values())[-1]
                    
                    if last_data != None:
                        break
                except :
                    counter+=1
                    print("server answer: ")
                    print(self._zmq._thread_data_output)
                    continue
                
            
            if counter ==10:
                 print("fuck!!!!")
                

            bid_price=last_data[0]
            ask_price=last_data[1]
            

           
            '''
            https://docs.mql4.com/constants/tradingconstants/orderproperties
            '''
            if signalDto.enter_type == 'sell':
                    
                    if signalDto.enterPrice >= last_data[0] :
                        _default_order['_type']=5
                    else :
                        _default_order['_type']=3
                        
            elif signalDto.enter_type == 'buy':
                
                if signalDto.enterPrice <=last_data[0] :
                        _default_order['_type']=4
                else :
                        _default_order['_type']=2
            print("default order:")
           # _default_order['_type']=0
            print(_default_order)
            
            self._zmq._DWX_MTX_NEW_TRADE_(_default_order)
            _ret2 = self._execution._execute_(_default_order,
                                                        _verbose=False,
                                                         _delay=0.1,_wbreak=10)
            sleep(10)
            
            if self._zmq._valid_response_(_ret2) == False:
               # print("zmq response Flase: ")
               # print (self._zmq._get_response_())
                
                return False
            else :
                print("zmq response True: ")
                print (self._zmq._get_response_())
                return True

           finally:
             self._lock.release()
            
    ##########################################################################
    
    def _stop_(self):
        
        self._market_open = False
        
        for _t in self._traders:
        
            # Setting _market_open to False will stop each "trader" thread
            # from doing anything more. So wait for them to finish.
            _t.join()
            
            print('\n[{}] .. and that\'s a wrap! Time to head home.\n'.format(_t.getName()))
        
        # Kill the updater too        
        self._updater_.join()
        
        print('\n\n{} .. wait for me.... I\'m going home too! xD\n'.format(self._updater_.getName()))
        
        # Send mass close instruction to MetaTrader in case anything's left.
        self._zmq._DWX_MTX_CLOSE_ALL_TRADES_()
        
    ##########################################################################
