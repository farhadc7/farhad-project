//+------------------------------------------------------------------+
//|                                                   Inspector1.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+

#include<Trade\Trade.mqh>

CTrade trade;
datetime lastCheckTime;
void OnTick()
  {

   datetime nowTime= TimeCurrent();
   if(lastCheckTime == NULL)
     {

      lastCheckTime = nowTime;
     }

   if(nowTime >= lastCheckTime) // waits for 10 minuts
     {
      lastCheckTime = nowTime +10;

      if(PositionsTotal() > 0)
        {
         for(int i=0 ; i< PositionsTotal(); i++)
           {
            string symbol = PositionGetSymbol(i);
            ulong ticket = PositionGetTicket(i);
            int digits=SymbolInfoInteger(symbol,SYMBOL_DIGITS);
            ulong digitsNum = MathPow(10,digits);

            if(PositionSelectByTicket(ticket))
              {
               double current_price=NormalizeDouble(PositionGetDouble(POSITION_PRICE_CURRENT),digits);
               double enter_price= NormalizeDouble(PositionGetDouble(POSITION_PRICE_OPEN),digits);
               double sl_price =NormalizeDouble(PositionGetDouble(POSITION_SL),digits);
               double tp_price =NormalizeDouble(PositionGetDouble(POSITION_TP),digits);

               int type= PositionGetInteger(POSITION_TYPE);

               if(type == POSITION_TYPE_BUY)
                 {

                  double profitPoints = (current_price - enter_price) * digitsNum;
                  Print(profitPoints);

                  if(profitPoints >= 300 && profitPoints < 500)
                    {
                     
                     Print("trail sopted");
                     trade.PositionModify(ticket,enter_price + (.0001),0);  // trail stop to 5 pip above entering point

                    }
                  else
                     if(profitPoints >= 500 && profitPoints < 700)
                       {
                        trade.PositionModify(ticket, enter_price + (.0030), 0);    // trail stop to 30 pip above enterig point

                       }
                     else
                        if(profitPoints >= 700 && profitPoints < 1000)
                          {
                           trade.PositionModify(ticket, enter_price + (.0050), 0);   // trail stop to 30 pip above enterig point
                          }

                 }
               else
                  if(type == POSITION_TYPE_SELL)
                    {

                     double profitPoints = (enter_price - current_price) * digitsNum;

                     if(profitPoints >= 300 && profitPoints < 500)
                       {
                        Print("trail stop");
                        trade.PositionModify(ticket,enter_price - (.0001), 0);   // trail stop to 5 pip above entering point

                       }
                     else
                        if(profitPoints >= 500 && profitPoints < 700)
                          {
                           trade.PositionModify(ticket, enter_price - (.0030), 0);    // trail stop to 30 pip above enterig point

                          }
                        else
                           if(profitPoints >= 700 && profitPoints < 1000)
                             {
                              trade.PositionModify(ticket, enter_price - (.0050), 0);   // trail stop to 30 pip above enterig point
                             }

                    }
              }
           }
        }

     }
  }
//+------------------------------------------------------------------+
