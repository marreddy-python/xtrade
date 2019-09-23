import time
from getters.api import td_ameritrade
from getters.decides_dg_count import check
from getters.export import highcharts_export
from celery_task import db
from flask import session
from models_celery.tables import price_data
from celery_task import Strategy_features
from sqlalchemy import and_
from decimal import *
import json
import sys
sys.dont_write_bytecode=True

from sqlalchemy.types import Integer


class MarketSimulator:

    def __init__(self):
        self.symbols = []
        self.strategyTypes = None
        self.MarketDataReader = None
        self.MarketDAO = None

    def run(self):
      
        data_main = DataLoader()
        dataLoader =  data_main.DataLoader(self.MarketDAO,self.MarketDataReader)
        
        # THis loop will save the candle information
        for i in range(len(self.symbols)):

            endtime = int(time.time()*1000.0) 
            starttime = endtime - 86400000*20

            print(starttime,endtime)

            a = data_main.readData(self.symbols[i],starttime,endtime)
            # print(a)

            data_main.transformAndSave(a)
         
            # This loop will save the angle information
            for j in range(len(self.strategyTypes)):
                SMA_main = SMAPreprocessor()
                SMA_main.generateStrategyData(self.symbols[i],starttime,endtime,a)
        
 
    def loadSymbols(self,symbols):
        self.symbols =  symbols
       
    def loadStrategyTypes(self,Preprocessor):
        self.strategyTypes = Preprocessor
    
    def setMarketDAO(self,MarketDAO):
        self.MarketDAO = MarketDAO
       
    def setReader(self,MarketDataReader):
        self.MarketDataReader = MarketDataReader


class DataLoader:
    
    def __init__(self):
        self.MarketDataReader = None
        self.MarketDAO = None
        
    def DataLoader(self,MarketDAO,MarketDataReader):
        self.MarketDataReader = MarketDataReader
        self.MarketDAO = MarketDAO
  
    def readData(self,symbol,startTime,endTime):

        A = AmeritradeAdapter()
        a = A.getMarketData(symbol,startTime,endTime)
        return a

    def transformAndSave(self,a):
        
        M = MarketDAOImpl()
        M.connectToPostgreDB()
        M.saveCandle(a)
        M.makeAuditLogEntryForTheDay()


class Candle:

    def __init__(self,TimeStramp,High,Low,Open,Close,Volume):
        self.TimeStramp = TimeStramp
        self.High = High
        self.Low = Low
        self.Open = Open
        self.Close = Close
        self.Volume = Volume 

# Abstract class implementation for MarketDAO
import abc
class MarketDAO(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def saveCandle(self,a):
        pass
    @abc.abstractmethod
    def makeAuditLogEntryForTheDay():
        pass
    @abc.abstractmethod
    def connectToPostgreDB():
        pass
    
class MarketDAOImpl(MarketDAO):  
    def connectToPostgreDB(slef):

        print('connected to postgresql')


    def saveCandle(slef,a):
        
        candles_length = len(a)

       #IN THE LOOP ENTER THE CANDLES INFO TO THE  DATABASE  
        for i in range(0,candles_length):
            candle = a[i]

            db_pricedata = price_data.query.filter(and_(price_data.Time_stamp == candle[0],price_data.stock_symbol=='TVIX'))      
            db_pricedata_length = db_pricedata.count()

            if db_pricedata_length == 0:
        
                stock_symbol = 'TVIX'
                Time_stamp = candle[0]
                Opening_price = candle[1]
                Closing_price = candle[4]
                High = candle[2]
                Low = candle[3]
                Volume = candle[5]
                Recorded_at = time.strftime("%d/%m/%Y")
        
                register = price_data(stock_symbol = stock_symbol,Time_stamp = Time_stamp,Opening_price = Opening_price,
                Closing_price = Closing_price,High = High,Low = Low, Volume = Volume , Recorded_at = Recorded_at)

                db.session.add(register)
                db.session.commit()
        
                # print('candles are saved successfully')
         
            else: 
                # print 'data already exists in a database'
                pass
    
        

        # print('candles are saved successfully')
         
    

    def makeAuditLogEntryForTheDay(self):
        print('AutoLogEntryForTheDay is done')
        


# MARKETDATAREADER
class MarketDataReader(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def getMarketData(self):
        pass

class AmeritradeAdapter(MarketDataReader):
    def _apiAuthentication():
        print ('auhenticated with ameritrade')

    def __init__(self):
        self.__symbol= None
        self.__startTime = None
        self.__endTime = None

    def getMarketData(self,symbol,startTime,endTime):
        self.__symbol= symbol
        self.__startTime = startTime
        self.__endTime = endTime
        
        # API REQUEST NEEDS TO BE HERE 

        print('loading market data')
        print(startTime,endTime)

        startTime = str(startTime)
        endTime = str(endTime)
        data = td_ameritrade(symbol,startTime,endTime)
        return data 


class StrategyPreprocessor(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def generateStrategyData(self):
        pass

class SMAPreprocessor(StrategyPreprocessor):
    def __init__(self):
        self.__symbol= None
        self.__startTime = None
        self.__endTime = None
    
    def generateStrategyData(self,symbol,startTime,endTime,loaded_data):
        self.__symbol= symbol
        self.__startTime = startTime
        self.__endTime = endTime

        self.__loaded_data = loaded_data
        
        print(' ANGLE CALCULATION ')

        High_main = HighChartsAdapter()

        print loaded_data[1][0]

        print len(loaded_data)
    
        for i in range(0,len(loaded_data)):
            # CHECK IF ANGLE IS ALREADY CALCULATED OR NOT if not calculate
            db_angledata = Strategy_features.query.filter(and_(Strategy_features.Day_identifier == loaded_data[i][0],Strategy_features.Symbol=='TVIX'))
            db_angledata_length = db_angledata.count()
    
            if db_angledata_length == 0 :
                
                endtime = loaded_data[i][0]
                # checking to decide the end date
                starttime = check(endtime)
                print endtime,starttime
                a = High_main.getMarketData(symbol,starttime,endtime)
            else:
                pass

        #a = High_main.getMarketData(symbol,startTime,endTime)
        
        smimpl =  SMADAOImpl()
        smimpl.connectToPostgreDB()
        smimpl.storeStrategyData()


class AngleGenerator(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def getMarketData(self):
        pass

class HighChartsAdapter(AngleGenerator):

    def __init__(self):
        self.__symbol= None
        self.__startTime = None
        self.__endTime = None

    def getMarketData(self,symbol,startTime,endTime):
        print 'startTime',startTime
        print 'endTime',endTime

        # print startTime,endTime
       
        db_data = price_data.query.filter(and_(price_data.Time_stamp.between(startTime,endTime),price_data.stock_symbol=='TVIX'))
        
    

        fetchdata_length = db_data.count()
        print fetchdata_length

        stock_data = []
            
        if fetchdata_length == 0 :
            pass
        else:

        # CONVERTING FETCHED DATA INTO THE LIST FORMAT INORDER TO SEND TO HIGHCHARTS EXPORT SERVER 
            for i in range(0,fetchdata_length):

                Time_stamp = db_data[i].Time_stamp
                Opening = db_data[i].Opening_price
                High = db_data[i].High
                Low = db_data[i].Low
                close = db_data[i].Closing_price
                Volume = db_data[i].Volume

                stock_data.append([Time_stamp,Opening,High,Low,close,Volume])

            '''for candle in db_data:

                Time_stamp = int(candle.Time_stamp)
                Opening = candle.Opening_price
                High = candle.High
                Low = candle.Low
                close = candle.Closing_price
                Volume = candle.Volume
                

                stock_data.append([Time_stamp,Opening,High,Low,close,Volume])'''

                # print stock_data
           
            angle = highcharts_export(stock_data)
            print angle
            stock_length  = len(stock_data)
            print stock_length
            candle_info = stock_data[stock_length-1]
            print candle_info
        
     
            score = {"Time_stamp":None ,"Open": None, "High": None,"Low": None, "Close": None,"Volume": None, "Angle": None,}    

            score["Time_stamp"] = candle_info[0] 
            score["Open"] = candle_info[1] 
            score["High"] = candle_info[2] 
            score["Low"] = candle_info[3] 
            score["Close"] = candle_info[4] 
            score["Volume"] = candle_info[5] 
            score["Angle"] = angle 

            data  = json.dumps(score)
            data = json.loads(data)

            print data 

            Day_identifier = candle_info[0]

            register = Strategy_features(Feature = data , Strategy_type_id = 'SMA',  Symbol = 'TVIX',Day_identifier = Day_identifier )

            db.session.add(register)
            db.session.commit() 


class SMADA0(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def storeStrategyData(self):
        pass

class SMADAOImpl(SMADA0):
    def connectToPostgreDB(slef):
        print('connected to postgresql')
    def storeStrategyData(self):

        print('stored the angle infomation into the database')
        
        
        





