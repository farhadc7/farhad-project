//+------------------------------------------------------------------+
//|  this project tasks:
 //     1. every ten seconds check signal file if there is new signal , take it.
 //     1.1. if the daily target is reached, program will stop taking new signal. all orders and positions will be close. 
//      2. if there is not, create order from signal string .     
//      3.check if there is similary signal or not.
//      4.if no similar signal , execute it.
//      5. if day is changed, reset target. 
//         
//
//to do: weather close all positions if next day is arrived or keep them.



//+------------------------------------------------------------------+
#property copyright "Copyright © 2006-2016"
#property version "1.06"
#property strict

#include<Trade\Trade.mqh>
#include <JAson.mqh>

//C:\Users\farhad\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Data
//1,EURUSD,signalProvider,1.19,1.17,1.20,0,0.01,0,0
//1,NZDCHF,signalProvider,0.6140,0.5800,0.6800,0,0.01,0,0

CTrade trade;
input string InpFileName="test.txt"; // file name
input string InpDirectoryName="Data"; // directory name
input string ResultFileName="resultFile.txt";
ushort u_sep=StringGetCharacter(",",0);
ulong responseFileLastPointer=0;

double ask;
double bid;
int symbolDigits;

string orderArr[];
string signalsArr[1];
int signalArrSize=1;
datetime lastCheckTime;
ENUM_TIMEFRAMES priceTimeFrame=PERIOD_M10;
datetime signalDate=NULL;
int hitDailytTarget=0;
string resultReportName;
int checkTimeForNewSignal = 3600;
int dailyTarget =1600;


//---
struct customSignal
  {
   int               type;
   string            provider;
   string            symbol;
   double            enterP;
   double            sl;
   double            tp;
   double            tp2;
   double            tp3;
   double            close;
   double            vol;
   double            newVol;
   ulong             ticket;
   bool              result;
   string            comment;
   string            res_comment;
  };

struct orderTypes
  {
   string            open;
   string            close;
   string            modify_tp;
   string            modify_vol;
   string            modify_sl;
  };

customSignal orderList[];
customSignal newSignal;
int listSize=0;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnInit()
  {
   trade.LogLevel(LOG_LEVEL_ALL);
   datetime current= TimeCurrent();
   MqlDateTime time;
   TimeToStruct(current,time);
   resultReportName = time.year +"-"+ time.mon +"-"+ time.day +"-"+ time.hour +"-"+ time.min +"-"+ time.sec;

  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick()
  {
   MqlRates prices[];
   ArraySetAsSeries(prices,true);


   datetime nowTime= TimeCurrent();
   if(lastCheckTime == NULL)
     {
      lastCheckTime = nowTime;
     }


   hitDailytTarget = checkIfDateChanged(hitDailytTarget);  // changed, hitDaily target will be zero.

   if(nowTime >= lastCheckTime && hitDailytTarget !=2) // waits for 10 secs and daily target is not hitted yet.
     {
      hitDailytTarget =checkTotalProfit(); // if total profit is bigger than 160 , stop the process. else it will be 1.
      if(hitDailytTarget == 1)
        {

         Print("*************check for new signal");
         lastCheckTime = nowTime +10;
         string orderStr=readFile();

         Print("file content is : ",orderStr);

         if(orderStr != "ok") // ok means its a repeated signal. must be replace by python
           {
            if(orderStr != "")
              {

               StringSplit(orderStr,u_sep,orderArr);
               newSignal =createOrder(orderArr);

               Print("signal Object is : ");
               Print(newSignal.type,',',newSignal.symbol,",",newSignal.enterP,",",newSignal.sl,",",newSignal.tp,",",newSignal.provider);

               // create prices array
               CopyRates(newSignal.symbol,priceTimeFrame,0,10,prices);
               symbolDigits = SymbolInfoInteger(newSignal.symbol,SYMBOL_DIGITS);
               ask= NormalizeDouble(SymbolInfoDouble(newSignal.symbol,SYMBOL_ASK),symbolDigits);
               bid= NormalizeDouble(SymbolInfoDouble(newSignal.symbol,SYMBOL_BID),symbolDigits);
               newSignal.enterP= NormalizeDouble(newSignal.enterP,symbolDigits);
               newSignal.sl = NormalizeDouble(newSignal.sl, symbolDigits);
               newSignal.tp = NormalizeDouble(newSignal.tp, symbolDigits);

               if(orderExists(newSignal.comment) == false)   // checks if there is no same order excecuted
                 {

                  // define order type to enter.
                  newSignal=processSignal(newSignal,priceTimeFrame,prices);
                  Print("order type is : ",newSignal.type);
                  if(newSignal.type != 0)
                    {
                     bool res=executeOrder(newSignal);
                     trade.PrintResult(); // print result of excecution
                     Print(trade.ResultComment());
                    }
                 }
               else
                 {
                  Print("request repeated");
                  newSignal.res_comment="008: repeated request";
                 }
              }
            else
              {
               Print("file is empty");
               newSignal.res_comment="008: file is empty";
              }

            listSize+=1;
            ArrayResize(orderList,listSize);
            orderList[listSize-1] = newSignal;
            writeResponse(newSignal);


           }
         Print("this request has been executed before");
        }
      else
        {
         Print("daily target hitted !!!! ({:o)");
        }

     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
customSignal processSignal(customSignal& signal, ENUM_TIMEFRAMES time, MqlRates& prices[])
  {

   if(signal.enterP == ask || signal.enterP == bid)
      return signal;

   int type = findSignalType(prices,signal.enterP, signal.type);

   if(type ==0)
     {
      Print("missed entring point");
      signal.res_comment = "008: missed entring point ";
     }
   signal.type = type;

   return signal;
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool normalSymbol(double price)
  {
   string priceStr = DoubleToString(price);
   int len=StringLen(StringSubstr(priceStr,StringFind(priceStr,".",0)+1));
   if(len == 5)
      return true; // 5 digits

   return false; // 3 digits
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int findSignalType(MqlRates& prices[], double enterPrice, int type) // bayad barrsai shavad aya signal dir be dast reside va az time vorood gozashte ya na.
  {
// agar dar yek zaman kotah masalan 5 daghighe ghemat hadaghal yek bar ba vorood barkhod dashte bashad , tasmim migirim ke gheymat dir reside va agar fasele kam bashad mitavanim
// dar lahze vared shavim.
// agar barkhordi nadashtebashad, yani bayad az pending order  - limit- estefade konim,
//int points=100000;
//if(!isNormalSymbol)
//   points =1000;

   if(type == 2)  // signal type is sell
     {

      if(bid > enterPrice)
         return 6;//sellstop

      for(int i=1; i< ArraySize(prices); i++)
        {
         if(prices[i].close >= enterPrice)   // agar yiki az gheymat ha balatar az gheymat vorood bashad.
           {
            if(MathAbs(bid - enterPrice)*symbolDigits < 100)   // agar ekhtelaf gheymat voord ba ask kamtar az 50 pont bashad . dar lahze vared sho.
              {
               return 2; //sell
              }
            else   // if atleast one is upper than enter price  but current price distance from enter price is too much.
              {
               return 0; //fail
              }
           }
        } // if non of the prices is above the enter price, it's sellLimit.
      return 5; //sellLimit
     }
   else
      if(type == 1)  // signal type is buy;
        {

         if(ask < enterPrice)
            return 4; //buyStop

         for(int i=1; i< ArraySize(prices); i++)
           {
            if(prices[i].close <= enterPrice)
              {
               if(MathAbs(ask - enterPrice)*symbolDigits < 100)
                 {
                  return 1; // buy
                 }
               else
                 {
                  return 0; //fail
                 }
              }
           }
         return 3; // buyLimit
        }
   return 0;
  }



//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool executeOrder(customSignal& order)
  {
   string comment=order.comment;
   bool result=false;
   int _type=order.type;
   trade.SetDeviationInPoints(30);
   datetime ex=TimeCurrent()+(checkTimeForNewSignal);
   int c=10;
   switch(_type)
     {
      case 1 :
         while(c>0)
           {
            result=trade.Buy(order.vol, order.symbol, ask, order.sl, order.tp,comment);
            if(result == true)
              {
               break;
              }
            else
              {
               c--;
              }
           }
         break;
      case 2 :
         while(c>0)
           {
            result = trade.Sell(order.vol, order.symbol, bid, order.sl, order.tp, comment);
            if(result == true)
              {
               break;
              }
            else
              {
               c--;
              }
           }
         break;
      case 3 :
         while(c>0)
           {
            result= trade.BuyLimit(order.vol, order.enterP,order.symbol, order.sl, order.tp,ORDER_TIME_SPECIFIED,ex, comment);
            if(result == true)
              {
               break;
              }
            else
              {
               c--;
              }
           }
         break;
      case 4 :
         while(c>0)
           {
            result = trade.BuyStop(order.vol, order.enterP,order.symbol, order.sl, order.tp,ORDER_TIME_SPECIFIED,ex, comment);
            if(result == true)
              {
               break;
              }
            else
              {
               c--;
              }
           }
         break;
      case 5 :
         while(c>0)
           {
            result = trade.SellLimit(order.vol, order.enterP,order.symbol, order.sl, order.tp,ORDER_TIME_SPECIFIED,ex, comment);
            if(result == true)
              {
               break;
              }
            else
              {
               c--;
              }
           }
         break;
      case 6 :
         while(c>0)
           {
            result = trade.SellStop(order.vol, order.enterP,order.symbol, order.sl, order.tp,ORDER_TIME_SPECIFIED,ex, comment);
            if(result == true)
              {
               break;
              }
            else
              {
               c--;
              }
           }
         break;
     }
   order.ticket = trade.ResultOrder(); // get ticket
   order.result = result;
   order.res_comment = trade.ResultComment(); // Gets the broker comment

   return result;
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
customSignal createOrder(string& orderInArr[])
  {
   customSignal temp;
   temp.type= orderInArr[0];
   temp.symbol = orderInArr[1];
   temp.provider =orderInArr[2];
   temp.enterP =StringToDouble(orderInArr[3]);
   temp.sl = StringToDouble(orderInArr[4]);
   temp.tp = StringToDouble(orderInArr[5]);
   temp.tp2 = StringToDouble(orderInArr[6]);
   temp.tp3 = StringToDouble(orderInArr[7]);
   temp.close = StringToDouble(orderInArr[8]);
   temp.vol = StringToDouble(orderInArr[9]);
   temp.newVol = StringToDouble(orderInArr[10]);
   temp.comment = temp.provider+"-"+temp.symbol;
   StringToLower(temp.symbol);
   if(temp.symbol == "gold")
     {
      temp.symbol = "XAUUSD";
     }
   StringToUpper(temp.symbol);
   return temp;
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string readFile()
  {
   string rawSignal="";
   bool reapeatedFile=false;
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI|FILE_COMMON);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for reading",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_COMMONDATA_PATH));
      //--- additional variables
      //--- read data from the file
      while(!FileIsEnding(file_handle))
        {
         rawSignal=FileReadString(file_handle);
        }
      int a=  StringLen(rawSignal);
      if(StringLen(rawSignal) !=0 & rawSignal != "ok")
        {
         FileWriteString(file_handle,"\nok");
        }
      //--- close the file
      FileClose(file_handle);
      PrintFormat("Data is read, %s file is closed",InpFileName);
      return rawSignal;
     }
   else
      PrintFormat("Failed to open %s file, Error code = %d",InpFileName,GetLastError());
   return "";
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void writeResponse(customSignal& finalSignal)
  {
   string res=TimeCurrent()+"," +finalSignal.symbol+ ","+finalSignal.type+","+finalSignal.provider+","+finalSignal.ticket+","+finalSignal.enterP+","+finalSignal.sl+","+finalSignal.tp+","+finalSignal.comment+","+finalSignal.res_comment+","+finalSignal.result+"\n";
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+resultReportName+".txt",FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI|FILE_COMMON);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for writing",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_COMMONDATA_PATH));

      if(responseFileLastPointer != 0)
        {
         FileSeek(file_handle,0,SEEK_END);
        }

      FileWriteString(file_handle,res);
      responseFileLastPointer = FileTell(file_handle);

      //--- close the file
      FileClose(file_handle);
      PrintFormat("Data is read, %s file is closed",InpFileName);
     }
   else
      PrintFormat("Failed to open %s file, Error code = %d",InpFileName,GetLastError());
  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool orderExists(string comment)
  {
   if(OrdersTotal()>0)
     {

      for(int i=0; i< OrdersTotal(); i++)
        {
         ulong ticket=OrderGetTicket(i);
         if(OrderSelect(ticket))
           {
            if(OrderGetString(ORDER_COMMENT) == comment)
              {
               return true;
              }
           }
        }
     }

   if(PositionsTotal() >0)
     {
      for(int i=0; i< PositionsTotal(); i++)
        {
         ulong ticket=PositionGetTicket(i);
         if(PositionSelectByTicket(ticket))
           {
            if(PositionGetString(POSITION_COMMENT) == comment)
              {
               return true;
              }
           }
        }
     }
   return false;
  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int checkTotalProfit() // if total profit is greater than 1600 , will close all positions, and return 2 else return 1;
  {
   double totalProfit=0;
   if(PositionsTotal() > 0)
     {

      for(int i=0 ; i< PositionsTotal(); i++)
        {
         string symbol = PositionGetSymbol(i);
         int digits=SymbolInfoInteger(symbol,SYMBOL_DIGITS);
         ulong digitsNum = MathPow(10,digits);
         double current_price =NormalizeDouble(PositionGetDouble(POSITION_PRICE_CURRENT),digits);
         double enter_price = NormalizeDouble(PositionGetDouble(POSITION_PRICE_OPEN),digits);
         ulong ticket = PositionGetTicket(i);
         double symbolProfit;
         int type= PositionGetInteger(POSITION_TYPE);

         if(PositionSelectByTicket(ticket))
           {

            if(type == POSITION_TYPE_BUY)
              {
               symbolProfit= (current_price - enter_price) * digitsNum;

              }
            else
               if(type == POSITION_TYPE_SELL)
                 {
                  symbolProfit = (enter_price - current_price) * digitsNum;
                 }

           }

         totalProfit += symbolProfit;
        }
     }

   if(totalProfit > dailyTarget) // we reach daily 1500 . must save it and have more strict strategy for further signals.
     {
      closePositions();
      return 2;
     }
   return 1;
  }



//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void closePositions()
  {

   for(int i=0 ; i< PositionsTotal(); i++)
     {

      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
         trade.PositionClose(ticket);
     }
     
   if(OrdersTotal() >0){
      for(int i=0; i< OrdersTotal(); i++){
         ulong ticket  =OrderGetTicket(i);
         
         if( OrderSelect(ticket)){
            trade.OrderDelete(ticket);
         }
      }
   }

  }
  
  int checkIfDateChanged(int hitDailytTarget){ // check if we are in the same day or next day. if day is changed, we reset hitdailyTarget.
      MqlDateTime date, newDate;
      
      TimeToStruct(signalDate , date);
      TimeToStruct(TimeCurrent(),newDate);
      
      
      if (date.day == newDate.day){
         return hitDailytTarget;
      }else {
         closePositions();
         return 0; 
      }
  }

//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
//bool checkNewOrder(customSignal& _order)
//  {
//
//   string _comment=_order.provider + "-" + _order.symbol;
//
//   if(listSize>0 && orderList[listSize-1].comment == _comment)
//     {
//      return false;
//     }
//   return true;
//  }
