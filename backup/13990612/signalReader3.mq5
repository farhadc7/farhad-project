//+------------------------------------------------------------------+
//|       response file is working fine and append new requests.
//
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
datetime lastCheckTime;
ENUM_TIMEFRAMES priceTimeFrame=PERIOD_M1;

//---
struct customSignal
  {
   int               type;
   string            provider;
   string            symbol;
   double            enterP;
   double            sl;
   double            tp;
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
void OnTick()
  {
   MqlRates prices[];
   ArraySetAsSeries(prices,true);


   datetime nowTime= TimeCurrent();
   if(lastCheckTime == NULL)
     {

      lastCheckTime = nowTime;
     }

   if(nowTime >= lastCheckTime) // waits for 10 minuts
     {

      lastCheckTime = nowTime +10;
      string orderStr=readFile();

      if(orderStr != "ok") // ok means its a repeated signal. must be replace by python
        {
         if(orderStr != "") 
           {

            StringSplit(orderStr,u_sep,orderArr);
            newSignal =createOrder(orderArr);

            // create prices array
            CopyRates(newSignal.symbol,priceTimeFrame,0,5,prices);
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

               if(newSignal.type != 0)
                 {
                  bool res=executeOrder(newSignal);
                  newSignal.res_comment = "success";
                 } //
              }
            else
              {
               newSignal.res_comment="008: repeated request";
              }
           }
         else
           {
            newSignal.res_comment="008: file is empty";
           }

         listSize+=1;
         ArrayResize(orderList,listSize);
         orderList[listSize-1] = newSignal;
         writeResponse(newSignal);
         

        }
     }
  }

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
            if(MathAbs(bid - enterPrice)*symbolDigits < 50)   // agar ekhtelaf gheymat voord ba ask kamtar az 50 pont bashad . dar lahze vared sho.
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
     }else
   if(type == 1)  // signal type is buy;
     {

      if(ask < enterPrice)
         return 4; //buyStop

      for(int i=1; i< ArraySize(prices); i++)
        {
         if(prices[i].close <= enterPrice)
           {
            if(MathAbs(ask - enterPrice)*symbolDigits < 50)
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
int executeOrder(customSignal& order)
  {
   string comment=order.comment;
   bool result=false;
   int _type=order.type;
   switch(_type)
     {
      case 1 :
         result=trade.Buy(order.vol, order.symbol, ask, order.sl, order.tp,comment);
         break;
      case 2 :
         result = trade.Sell(order.vol, order.symbol, bid, order.sl, order.tp, comment);
         break;
      case 3 :
         result= trade.BuyLimit(order.vol, order.enterP,order.symbol, order.sl, order.tp,0,0, comment);
         break;
      case 4 :
         result = trade.BuyStop(order.vol, order.enterP,order.symbol, order.sl, order.tp,0,0, comment);

         break;
      case 5 :
         result = trade.SellLimit(order.vol, order.enterP,order.symbol, order.sl, order.tp,0,0, comment);
         break;
      case 6 :
         result = trade.SellStop(order.vol, order.enterP,order.symbol, order.sl, order.tp,0,0, comment);
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
   temp.close = StringToDouble(orderInArr[6]);
   temp.vol = StringToDouble(orderInArr[7]);
   temp.newVol = StringToDouble(orderInArr[8]);
   temp.comment = temp.provider+"-"+temp.symbol;

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
      if(rawSignal != "ok")
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
  
void writeResponse(customSignal& finalSignal)
  {
   string res= finalSignal.symbol+ ","+finalSignal.provider+","+finalSignal.ticket+","+finalSignal.comment+","+finalSignal.res_comment+","+finalSignal.result+"\n";
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+ResultFileName,FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI|FILE_COMMON);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for writing",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_COMMONDATA_PATH));
      
      if(responseFileLastPointer != 0){
         FileSeek(file_handle,responseFileLastPointer,SEEK_SET);
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
