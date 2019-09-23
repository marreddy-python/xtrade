import sys
sys.dont_write_bytecode=True

from factory import get_ds,get_ss


class DataController():
    
    DS = get_ds()

    def __init__(self):
        self.symbols = None
        self.Strategy = None
        self.l = []
        self.start = None
        self.end = None

    def getTrades(self,symbols,Strategy,start,end):
        self.symbols = symbols
        self.Strategy = Strategy
        self.start = start 
        self.end = end
        a = self.DS.getTrades(symbols,Strategy,start,end)
        return a

    def getPerformance(self,symbol,Strategy,start,end):
        self.symbol = symbol 
        self.Strategy = Strategy
        self.start = start 
        self.end = end
        a = self.DS.getPerformance(symbol,Strategy,start,end)
        return a 


    def MarketData(self,start,end):
        self.start = start 
        self.end = end
        a = self.DS.MarketData(start,end)
        return a

    
    def getStrategies(self):
        data = self.DS.getStrategies()
        return data 





class StrategyController():
     
    SS = get_ss()

    def __init__(self):
        self.Strategy = None
        self.l = []
        self.symbol = None
        self.start = None
        self.end = None
    
    def saveStrategy(self,Strategy,Start_time,End_time):
        self.Strategy = Strategy
        b = self.SS.saveStrategy(Strategy,Start_time,End_time)
        return b 

    def getNewStrategy(self,l):
        self.l = l
    
    def updateStrategy(self,Strategy,params):
        self.Strategy = Strategy
        self.params = params
        b = self.SS.updateStrategy(Strategy,params)
        return b 


    def applyStrategy(self,symbol,Strategy,start,end):
        self.symbol = symbol
        self.Strategy = Strategy
        self.start = start 
        self.end = end
        b = self.SS.applyStrategy(symbol,Strategy,start,end)
        return b 

    def getProgress():
        pass


class Arena():

    def __init__(self,pStrategies,noOfStrategies,maximumlimit):
        self.pStrategies = None
        self.noOfStrategies = None
        self.maximumlimit = None

    def addStrategiesToArena(self,Strategy):
        self.Strategy = Strategy

    def deleteStrategiesFromArena(self,Strategy):
        self.Strategy = Strategy
    
    def createArena():
        pass


class Strategy():

    def __init__(self,id,startegy_values,isFavourite):
        self.id = id 
        self.startegy_values = startegy_values
        self.isFavourite = isFavourite

    def __new__(cls):
        return [id,startegy_values,isFavourite]


# THESE CALLS NEEDS NEEDS TO BE FROM THE UI 
'''loader = DataController()
Strategy = Strategy(1,[40,20,'NO'],'TRUE')
a = loader.getTrades('TVIX',Strategy ,'10000','20000')
print(a)
a = loader.MarketData('1565677800000','1565720940000')
print(a)
a = loader.getPerformance('TVIX',Strategy ,'10000','20000')
print(a)


startegy_loader = StrategyController()
b = startegy_loader.saveStrategy(Strategy)
print b 
b = startegy_loader.updateStrategy(Strategy,[2,[20,10,'YES'],'TRUE'])
print b 
b = startegy_loader.applyStrategy('TVIX',Strategy ,'10000','20000')
print b''' 

