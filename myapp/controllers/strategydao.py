import abc
import datetime
from datetime import date
import json 
from decision_making.buy_sell import buy_sell
from decision_making.buy_sell_rlt import buy_sell_rlt
from decision_making.buy_sell_stop import buy_sell_stop
from decision_making.buy_sell_rlt_stop import buy_sell_rlt_stop
from datetime import timedelta

from myapp.models.users import Strategy,Strategy_type,Strategies_Grades,Trades,Daily_metric,Total_metric,db
db.create_all()
from sqlalchemy import and_
# HERE IMPORT STRATEGY FEATURES TABLE FROM CELERY TASK
from celery_task import price_data,Strategy_features
# from background_jobs.celery_task import price_data,Strategy_features



import time

class StrategyDAO():
    
    def saveStrategy(self,s,End_time,Start_time ): 
    
     
        sc = {
            "buying_angle":s.startegy_values[0] ,
            "selling_angle":  s.startegy_values[1],
            "optimization":s.startegy_values[2],
            "relative_angle": s.startegy_values[3],
            "stop_order":  s.startegy_values[4],
            "less_than_buy": s.startegy_values[5]
        }
 
        print 'score',sc
        
        data  = json.dumps(sc)
        score = json.loads(data)

       

        print 'SAVED STRATEY',score
 
        Created_at = time.strftime("%a, %d %b %Y %H:%M:%S")

        if sc["optimization"]=="None" and sc["stop_order"]=="None":
            Opti = "No"
        else:
            Opti = "YES"


        # if not stored that strategy than store it.

        # saving into the startegy table 
        db_data = Strategy(Strategy_type_id = 'SMA', Symbol = 'TVIX',Created_at = Created_at, Params = score, Start_time= Start_time, End_time =  End_time,Optimization=Opti,isFavourite = False)
        db.session.add(db_data)
        db.session.commit()


    def updateStrategy(self,MStrategy,params):
       
        Symbol = 'TVIX'
        Applied  = True 
        Created_at = time.strftime("%a, %d %b %Y %H:%M:%S") 
        db_data = Strategies_Grades(Strategy_type_id = 'SMA' ,Created_at =  Created_at,isFavourite = True, Params = params)
        db.session.add(db_data)
        db.session.commit()


    def insertTrade(self,Trade):
        pass


class StrategyProcessor(object):

    def __init__(self):
        self.type = None
        self.price = None 
        self.generatedAt = None 

    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def applyStrategy(self,s,start,end):
        pass


class SMAStrategyProcessor(StrategyProcessor):

    start_date = None
    end_date = None
    St = None


    def applyStrategy(self,s,end,start):

        global start_date,end_date,Strategy 

        # Get the data from Strategy_Features table
        db_data = Strategy_features.query.with_entities(Strategy_features.Feature).all()
        
        print 'length_of_angle',len(db_data)
    
        # fetched_data = db_data.count()
        fetched_data = len(db_data)
    
        # STOCK_DATA STORES THE MARKET DATA ALONG WITH THE ANGLE INFOMATION 
        stock_data = []
        for i in range(0,fetched_data):

            a =  db_data[i].Feature
            Time_stamp = a["Time_stamp"]
            Opening = a["Open"]
            High = a["High"]
            Low = a["Low"]
            close = a["Close"]
            Volume = a["Volume"]
            Angle = a["Angle"]

            if Time_stamp >= start and Time_stamp <= end:

                stock_data.append([Time_stamp,Opening,High,Low,close,Volume,Angle])

            
        print start,end
       
        sc = {
            "buying_angle":s.startegy_values[0] ,
            "selling_angle":  s.startegy_values[1],
            "optimization":s.startegy_values[2],
            "relative_angle": s.startegy_values[3],
            "stop_order":  s.startegy_values[4],
            "less_than_buy": s.startegy_values[5]
        }
 
        print 'score',sc
        
        data  = json.dumps(sc)
        stgy = json.loads(data)

        start_date = start
        end_date = end
        St = stgy
        current_strategy = stgy

        #GLOBAL VARIABLES
        buy_price = 0
        sell_price = 0
        buy_value = 0
        sell_value = 0
        profit_loss = 0
        profit_loss_percentage = 0
        buy_angle = 0
        Sell_angle = 0
        Symbol = 'TVIX'
        Type = 'SMA'
        buy_time = 0
        Sell_time = 0
        Opmz = 0
        Day_identifier = 0

        # Get all strategies from the strategy table
        db_get_strategies =  Strategy.query.filter(Strategy.Symbol=='TVIX').all()
        fetched_length = len(db_get_strategies)
        stored_strategies = []
        for st in range(0,fetched_length):
            strategies = db_get_strategies[st].Params
            if  db_get_strategies[st].Start_time == start and db_get_strategies[st].End_time == end:
                    stored_strategies.append(strategies)
                    
        # Check if current strategy is exist in strategies table 
        if (current_strategy in stored_strategies):
            pass
        else:
            # iterate over the lenth of candles
            for i in range(0,len(stock_data)):

                market_data = stock_data[i]
                time = market_data[0]
                price = market_data[4]
                angle = market_data[6]
                
                if angle == 'angle calculation is not possible':
                    pass
                else:   
                
                    if current_strategy["optimization"] == 'None' and current_strategy["stop_order"] == 'None':
                        decision = buy_sell(current_strategy["buying_angle"],current_strategy["selling_angle"],angle)
                        Opti = "No"
            
                    elif current_strategy["stop_order"] == 'None':
                        decision = buy_sell_rlt(current_strategy["buying_angle"],current_strategy["selling_angle"],current_strategy["relative_angle"],angle)
                        Opti = "Yes"
                    elif current_strategy["optimization"] == 'None':
                        decision = buy_sell_stop(current_strategy["buying_angle"],current_strategy["selling_angle"],angle,buy_price,price,current_strategy["less_than_buy"])
                        Opti = "Yes"
                    else:
                        decision = buy_sell_rlt_stop(current_strategy["buying_angle"],current_strategy["selling_angle"],current_strategy["relative_angle"],angle,buy_price,price,current_strategy["less_than_buy"])
                        Opti = "Yes"

                    print time,angle,decision

                    if decision == 1:
                        # update the global buy_price,buy_value,buying_angle,buy_time varaibles
                        buy_price = price 
                        buy_angle = angle
                        buy_value = buy_price * 1400
                        buy_time = time
                    
                    elif decision == 2:
                    
                        # update the global sell_price,sell_value,selling_angle,sell_time
                        # Give same day identifier if the trade happend in the same day 

                        sell_price = price 
                        print price
                        sell_value = sell_price * 1400
                        sell_angle = angle
                        sell_time = time
                        profit_loss = -(buy_value - sell_value)
                        profit_loss_percentage =((profit_loss/sell_value))*100

                        current_candle_time = time

                        print sell_price,sell_value,sell_angle,sell_time,profit_loss,profit_loss_percentage

            
                        date = datetime.datetime.fromtimestamp(current_candle_time/1000.0)
                        Day_identifier = date.strftime('%Y-%m-%d')

                        
                        # ENTERING THE VALUES INTO THE TRADES TABLE
                        data_into_db = Trades(buy_price = buy_price,sell_price = sell_price,buy_value = buy_value, sell_value = sell_value ,
                                    profit_loss = profit_loss  , profit_loss_percentage =  profit_loss_percentage ,buy_angle = buy_angle,Sell_angle = sell_angle ,Symbol = 'TVIX',
                                    Type = 'SMA',buy_time = buy_time, Sell_time = sell_time ,Optimization = Opti ,Day_identifier = Day_identifier,Strategy = current_strategy)
                    
                        db.session.add(data_into_db)
                        db.session.commit()
    
                    else:
                        pass 
        
            # After all trades enters into the database call metric class for calculation of metric values with starting and ending time 
            #  After metric calculation call total metric values for calculation of metric values for 20days
            
            metric_calc = MetricImpl()
            print St
            metric_calc.getMetric(start_date,end_date,St)
          
            metric_calc.Tot_met(start_date,end_date,St)
            
        # return 'Strategy applied successfully for 20days'
    

class Trade():

    def __init__(self,Type,price,at,post):
        self.type = Type
        self.price = price 
        self.at = at
        self.post = post
    
    def __new__(cls):
        return [Type,price,at,post]


class Signal():

    def __init__(self,Type,price,generatedAt):
        self.Type = Type
        self.price = price 
        self.generatedAt = generatedAt

    def __new__(cls):
        return [Type,price,generatedAt]



class Broker():

    def __init__(self,Type,price,generatedAt):
        self.Type = Type
        self.price = price 
        self.generatedAt = generatedAt

    def __new__(cls):
        return [Type,price,generatedAt]



# METRIC CALCULATION FOR EACH STRATEGY 
class Metric(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def forEachTrade(self,t):
        pass

    @abc.abstractmethod
    def getMetric():
        pass

    @abc.abstractmethod
    def getFormattedMetricLabel():
        pass


class MetricImpl(Metric):

    '''def __init__(self,name,date,strategy,metric):
        self.name = None
        self.date = None 
        self.strategy = None'''

    def forEachTrade(self,t):
        pass

    def getFormattedMetricLabel():
        pass


    def getMetric(self,starttime,endtime,Strategy):

        def myFunction(milliseconds):
            date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
            startday = date.strftime('%Y-%m-%d')
            datee = datetime.datetime.strptime(startday, "%Y-%m-%d")
            a = datee.year 
            b =  datee.month
            c =  datee.day
            return a,b,c 

        a,b,c = myFunction(starttime)
        start_date = date(a, b, c)
        a,b,c = myFunction(endtime)
        end_date = date(a, b, c+1)

        def daterange(start_date, end_date):
            for n in range(int ((end_date - start_date).days)):
                yield start_date + timedelta(n)
        
        # get each day between starttime and endtime
        for single_date in daterange(start_date, end_date):
            required_day = single_date.strftime("%Y-%m-%d") 
        

            # Filter the database based on Day_identifier 
            db_data = Trades.query.filter(and_(Trades.Day_identifier == required_day,Trades.Symbol=='TVIX'))
          
            fetchdata_length = db_data.count()
           
            print fetchdata_length
        
            # a ARRAY HOLDS BOTH PORFITS/LOSSES 
            a = []

            for i in range(0,fetchdata_length):
                element = db_data[i].profit_loss
                a.append(element)

            Total_trades = len(a)

            # SEPEARTING WINING TRADES AND LOSING TRADES
            Winning_Trades = []
            losing_Trades = []
            for i in range(0,Total_trades):
                if a[i] > 0:
                    Winning_Trades.append(a[i])
                else:
                    losing_Trades.append(a[i])

            print 'Winning_Trades , losing_Trades',losing_Trades,Winning_Trades

            Winning_Trades_sum = sum(Winning_Trades) 
            print 'Winning_Trades_sum', Winning_Trades_sum
            losing_Trades_sum = sum(losing_Trades)
            print 'losing_Trades_sum',losing_Trades_sum

            Profit = Winning_Trades_sum - (-losing_Trades_sum)
           
            print 'PROFIT',Profit 

            print 'length_winning_trades,total_trades',len(Winning_Trades),Total_trades
            Winning_Trades_length = len(Winning_Trades)

            if Winning_Trades_sum !=0 and losing_Trades_sum !=0:
                Profit_Factor = Winning_Trades_sum / losing_Trades_sum
                print 'length_winning_trades,total_trades',len(Winning_Trades),Total_trades
                Profitable = float(Winning_Trades_length) / Total_trades
            else:
                Profit_Factor = 0
                Profitable = 0
            
            print 'PROFIT_FACTOR',Profit_Factor

            print 'Profitable',Profitable


            # Enter these values into the daily trade metrics 
            data_to_db = Daily_metric( Strategy =  Strategy,Symbol = 'TVIX',
                Total_Profit =  Profit ,Profit_Factor = Profit_Factor, Profitable = Profitable ,Max_Drawdown = None ,Type = 'SMA', Day_identifier = required_day )
            
            db.session.add(data_to_db)
            db.session.commit()
       




    def Tot_met(self,starttime,endtime,Strategy):


 
        def myFunction(milliseconds):
            date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
            startday = date.strftime('%Y-%m-%d')
            datee = datetime.datetime.strptime(startday, "%Y-%m-%d")
            a = datee.year 
            b =  datee.month
            c =  datee.day
            return a,b,c 

        a,b,c = myFunction(starttime)
        start_date = date(a, b, c)
        a,b,c = myFunction(endtime)
        end_date = date(a, b, c+1)

       
        st_da= str(start_date) 
        e_da = str(end_date)



        Tweenty_days_trades = Trades.query.filter(and_(Trades.Day_identifier.between(st_da,e_da),Trades.Symbol=='TVIX'))
        
        print Tweenty_days_trades.count()

        print '------------------------------------SUCCESS----------------------------------'

        print Tweenty_days_trades.count()

        fetchdata_length =  Tweenty_days_trades.count()

        print fetchdata_length

        WIINING_TRADES = []
        LOOSING_TRADES = []
        Total_Trades = []
        
        for t in range(0,fetchdata_length):
            element =  Tweenty_days_trades[t].profit_loss
            Total_Trades.append(element)

        Total_Trades_len = len(Total_Trades)

        Profit = 0
        Profit_Factor = 0
        Profitable = 0

        for i in range(0,Total_Trades_len):
            if Total_Trades[i] > 0:
                WIINING_TRADES.append(Total_Trades[i])
            else:
                LOOSING_TRADES.append(Total_Trades[i])
            
            WIINING_TRADES_SUM = sum(WIINING_TRADES) 
            LOOSING_TRADES_SUM = sum(LOOSING_TRADES)

            # print WIINING_TRADES_SUM,LOOSING_TRADES_SUM

            Profit = WIINING_TRADES_SUM - (-LOOSING_TRADES_SUM)

            Profit_Factor = None
            Profitable = None

            WIINING_TRADES_LENGTH = len(WIINING_TRADES ) 

            if WIINING_TRADES_SUM != 0 and LOOSING_TRADES_SUM !=0:
                Profit_Factor = WIINING_TRADES_SUM  / LOOSING_TRADES_SUM
                Profitable =  float(WIINING_TRADES_LENGTH) / Total_Trades_len
                
            else:
                WIINING_TRADES_SUM == 0 or LOOSING_TRADES_SUM == 0 
                print 'CALCULATION OF PROFIT_FACTOR AND PROFITABLE IS NOT POSSIBLE'
                Profit_Factor = 0
                Profitable = 0


        # Enter these values into the total_metric table
        data_to_db = Total_metric( Strategy = Strategy, Strategy_id = 'SMA', Total_Profit =  Profit ,Profit_Factor =  Profit_Factor, Profitable = Profitable ,Max_Drawdown = None,Start_Date = starttime,End_Date = endtime )
        db.session.add(data_to_db)
        db.session.commit()

        print '------------------------DONE --------------------------------------'