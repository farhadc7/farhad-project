# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 21:38:44 2020

@author: farhad
"""


from DWX_ZeroMQ_Connector_v2_0_1_RC8 import DWX_ZeroMQ_Connector

a=DWX_ZeroMQ_Connector()

a._generate_default_order_dict()

a._DWX_MTX_GET_ALL_OPEN_TRADES_()

a._DWX_MTX_MODIFY_TRADE_BY_TICKET_(128844168,200,200)
a._DWX_MTX_CLOSE_TRADE_BY_TICKET_(128844168)


a._DWX_MTX_NEW_TRADE_() # when this send with no args, default order dict will send

a._DWX_MTX_CLOSE_TRADES_BY_MAGIC_(123456)

#subscribe to hystorical data of mt4 :
a._DWX_MTX_SEND_MARKETDATA_REQUEST_()

#subscribe to real market data :
# this will fill a dict of our object named Market_Data_DB
a._DWX_MTX_SUBSCRIBE_MARKETDATA_('EURUSD')
print("response is: ")
print(a._get_response_())
a._DWX_MTX_SUBSCRIBE_MARKETDATA_(_symbol='GBPUSD')

a._Market_Data_DB['EURUSD']


a._Market_Data_DB.keys()
a._DWX_MTX_UNSUBSCRIBE_MARKETDATA_("EURUSD")
a._DWX_MTX_UNSUBSCRIBE_ALL_MARKETDATA_REQUESTS_()
a._DWX_MTX_GET_ALL_OPEN_TRADES_()
    