//+------------------------------------------------------------------+
// trail stop all open positions |
//+------------------------------------------------------------------+

#include<Trade\Trade.mqh>

CTrade trade;
datetime lastCheckTime;

int level=1;
void OnTick()
  {

   datetime nowTime= TimeCurrent();
   if(lastCheckTime == NULL)
     {

      lastCheckTime = nowTime;
     }

   if(nowTime >= lastCheckTime) // waits for 10 secs
     {
      lastCheckTime = nowTime +10;

      if(PositionsTotal() > 0)
        {
            trailStop(); 
        }
     }
  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void trailStop()
  {

   for(int i=0 ; i< PositionsTotal(); i++)
     {
      string symbol = PositionGetSymbol(i);
      ulong ticket = PositionGetTicket(i);
      int digits=SymbolInfoInteger(symbol,SYMBOL_DIGITS);
      ulong digitsNum = MathPow(10,digits);
      double point =  1 / MathPow(10,digits);
      bool result;

      if(PositionSelectByTicket(ticket))
        {
         double current_price=NormalizeDouble(PositionGetDouble(POSITION_PRICE_CURRENT),digits);
         double enter_price= NormalizeDouble(PositionGetDouble(POSITION_PRICE_OPEN),digits);
         double sl_price =NormalizeDouble(PositionGetDouble(POSITION_SL),digits);
         double tp_price =NormalizeDouble(PositionGetDouble(POSITION_TP),digits);
         int type= PositionGetInteger(POSITION_TYPE);
         double profitPoints =0;

         if(type == POSITION_TYPE_BUY)
           {
            profitPoints = (current_price - enter_price) * digitsNum;

           }
         else
            if(type == POSITION_TYPE_SELL)
              {
               profitPoints = (enter_price - current_price) * digitsNum;
               point = -1 * point;
              }

         if(profitPoints > 0)
           {
            Print(symbol,"profit in pips is:",profitPoints);

            if(profitPoints >= 500 && profitPoints < 700)
              {

               Print(symbol," trail sopted 1");
               result =  modify_sl_Position(ticket, enter_price, point, 50); // trail stop to 5 pip above entering point

              }
            else
               if(profitPoints >= 500 && profitPoints < 700)
                 {
                  result =  modify_sl_Position(ticket, enter_price, point, 500);

                 }
               else
                  if(profitPoints >= 700 && profitPoints < 1000)
                    {
                     result =  modify_sl_Position(ticket, enter_price, point, 700);
                    }
                  else
                     if(profitPoints >= 1000)
                       {
                        result =  modify_sl_Position(ticket, enter_price, point, 1000);
                       }

            Print("result of ", symbol, "is : ", result);

           }
        }
     }
  }
  


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool modify_sl_Position(ulong ticket, double enterPrice, double point, int diff)
  {

   return trade.PositionModify(ticket, enterPrice + (point * diff), 0);

  }
  
  void closePositions(){
  
       for(int i=0 ; i< PositionsTotal(); i++){
       
      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
         trade.PositionClose(ticket);
       }
   
  }
//+------------------------------------------------------------------+
