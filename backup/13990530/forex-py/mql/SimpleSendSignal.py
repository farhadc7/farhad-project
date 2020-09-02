# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:11:39 2020

@author: farhad
"""
from SignalDto import SignalDto
from mql.DWX_ZeroMQ_Connector_v2_0_1_RC8 import DWX_ZeroMQ_Connector
from mql.MODULES.DWX_ZMQ_Execution import DWX_ZMQ_Execution
from mql.MODULES.DWX_ZMQ_Reporting import DWX_ZMQ_Reporting
from pandas import Timedelta, to_datetime
from threading import Thread, Lock
from time import sleep
import random
from mql.MtraderApi import MTraderAPI


class SimpleSendSignal:
    

    def __init__(self,
                 _delay=0.1,
                 _broker_gmt=3,
                 _verbose=False,
                 _close_t_delta=5):
        self._broker_gmt = _broker_gmt
        self._zmq = DWX_ZeroMQ_Connector(_verbose=_verbose)

        # Modules
        self._execution = DWX_ZMQ_Execution(self._zmq)
        self._reporting = DWX_ZMQ_Reporting(self._zmq)
        
        


    def _trader_(self,signalDto: SignalDto):
        
        
        #while True
        try:
                    
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
            counter=0
            self._zmq._DWX_MTX_SUBSCRIBE_MARKETDATA_(signalDto.symbol)
            while counter !=10 :
                try:
                  
                    sleep(5)
                    last_data= list(self._zmq._Market_Data_DB[signalDto.symbol].values())[-1]
                    sleep(5)
                    if last_data != None:
                        break
                except :
                    counter+=1
                    continue
                
            
            if counter ==10:
                  print("fuck!!!!")
                
    
            bid_price=last_data[0]
            ask_price=last_data[1]
            
    
           
            # '''
            # https://docs.mql4.com/constants/tradingconstants/orderproperties
            # '''
            if signalDto.enter_type == 'sell':
                    
                    if signalDto.enterPrice >= last_data[0] :
                        _default_order['_type']=3 #Sell limit pending order
                    else :
                        _default_order['_type']=5 #Sell stop pending order
                        
            elif signalDto.enter_type == 'buy':
                
                if signalDto.enterPrice <=last_data[1] :
                        _default_order['_type']=2 #Buy limit pending order
                else :
                        _default_order['_type']=4 #Buy stop pending order
            
            # _ret2 = self._execution._execute_(_default_order,
            #                                               _verbose=False,
            #                                               _delay=0.1,_wbreak=10)
        
            print(_default_order)
            c=0
            while c<10 :
                 re=self._zmq._DWX_MTX_NEW_TRADE_(_default_order)
                 if self._zmq._valid_response_() == False:
                     c+=1
                     continue
                 else:
                     print(self._zmq._get_response_())
                     return True


        finally:
            print(self._zmq._get_response_())
             
 

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
