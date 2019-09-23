import sys
sys.dont_write_bytecode=True
import requests,json,time,urllib2
import abc
import datetime
from datetime import date
from sqlalchemy import and_
from sqlalchemy import desc

from datetime import timedelta


from myapp.models.users import Strategy,Strategy_type,Strategies_Grades,Trades,Daily_metric,Total_metric,db

# Here import Price_data table of a celery task
from celery_task import price_data,Strategy_features
# from background_jobs.celery_task import price_data,Strategy_features


class DataDAO():

    def getTrades(self,symbol,St,start,end):
        a = DataDAOPostgreImpl()
        b = a.getTrades(symbol,St,start,end)
        return b

    def getPerformance(self,symbol,St,start,end):
        a = DataDAOPostgreImpl()
        b = a.getPerformance(symbol,St,start,end)
        return b 

    def MarketData(self,start,end):
        a = DataDAOPostgreImpl()
        b = a.MarketData(start,end)
        return b

    def getStrategies(self):
        a = DataDAOPostgreImpl()
        b = a.getStrategies()
        return b 



class DataDAOPostgre(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getTrades(symbol,St,start,end):
        pass
 
    @abc.abstractmethod
    def getPerformance(symbol,St,start,end):
        pass
     
    @abc.abstractmethod
    def MarketData(start,end):
        pass

class DataDAOPostgreImpl(DataDAOPostgre):

    def getTrades(self,symbol,St,end,start):
        
        print 'xxxxx',start,end

        db_data = Trades.query.filter(and_(Trades.Sell_time.between(start,end),Trades.Symbol=='TVIX'))

        # print db_data
        print db_data.count()
        fetchdata_length = db_data.count()
         
        TRADES = []
        buy_flags = []
        sell_flags = []

        current_strategy = St.startegy_values
        
        for i in range(0,fetchdata_length):

            if ( db_data[i].Strategy["buying_angle"] == current_strategy[0] and  db_data[i].Strategy["selling_angle"]==current_strategy[1] and  db_data[i].Strategy["optimization"]==current_strategy[2] and  db_data[i].Strategy["relative_angle"]==current_strategy[3] and  db_data[i].Strategy["stop_order"]==current_strategy[4] and  db_data[i].Strategy["less_than_buy"]==current_strategy[5]): 
               
                buy_price = round(db_data[i].buy_price,2)
                sell_price = round(db_data[i].sell_price,2)
                buy_value = round(db_data[i].buy_value,2)
                sell_value = round(db_data[i].sell_value,2)
                profit_loss = round(db_data[i].profit_loss,2)
                profit_loss_percentage  = round(db_data[i].profit_loss_percentage,2)
                buy_angle = round(db_data[i].buy_angle,2)
                Sell_angle = db_data[i].Sell_angle
                Optimization = db_data[i].Optimization
                Day_identifier = db_data[i].Day_identifier 

                TRADES.append([buy_price,sell_price,buy_value ,sell_value ,profit_loss,profit_loss_percentage,buy_angle,Sell_angle,Optimization,Day_identifier ])
                
                buy_dict = {
                    "x": None,
                    "title": 'B',
                    "text":'Buy'
                }

                sell_dict = {
                    "x": None,
                    "title": 'S',
                    "text":'Sell'
                }

                buy_dict["x"] = int(db_data[i].buy_time)
                sell_dict["x"] = int(db_data[i].Sell_time)

                buy_flags.append(buy_dict)
                sell_flags.append(sell_dict)


                print '--------------------------------I AM GETTING THE TRADES --------------------------------------------------'
       
            else:
                pass

        buy_flags = sorted(buy_flags, key = lambda i: i['x']) 
        sell_flags = sorted(sell_flags, key = lambda i: i['x'])
        print buy_flags,sell_flags
        return TRADES,buy_flags,sell_flags

       


    def getPerformance(self,symbol,St,end,start):
        # return 'Getting the performance'

        def myFunction(milliseconds):
            date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
            startday = date.strftime('%Y-%m-%d')
            datee = datetime.datetime.strptime(startday, "%Y-%m-%d")

            a = datee.year 
            b =  datee.month
            c =  datee.day
            return a,b,c 

        a,b,c = myFunction(start)
        start_date = date(a, b, c-1)
        a,b,c = myFunction(end)
        end_date = date(a, b, c+1)
        print start_date,end_date

        # Filter the daily_metric table based on the day identifiers 
        start_date = str(start_date)
        end_date = str(end_date)

        print start_date,end_date

        current_strategy = St.startegy_values
        print current_strategy

        db_fetch = Daily_metric.query.filter(and_( Daily_metric.Day_identifier.between(start_date,end_date), Daily_metric.Symbol=='TVIX',))
        
        fetchdata_length = db_fetch.count()
        
        print 'fetcheddata_length', fetchdata_length

        scores = {"Total_Profit": [], "Profit_Factor": [], "Profitable": [],"Max_Drawdown":[],"x":[]} 
       

        for i in range(0,fetchdata_length):

            if (db_fetch[i].Strategy["buying_angle"] == current_strategy[0] and db_fetch[i].Strategy["selling_angle"]==current_strategy[1] and db_fetch[i].Strategy["optimization"]==current_strategy[2] and db_fetch[i].Strategy["relative_angle"]==current_strategy[3] and  db_fetch[i].Strategy["stop_order"]==current_strategy[4] and db_fetch[i].Strategy["less_than_buy"]==current_strategy[5]): 
               

                a = db_fetch[i].Total_Profit
                b = db_fetch[i].Profit_Factor
                c = db_fetch[i].Profitable
                d = db_fetch[i].Max_Drawdown
                e = db_fetch[i].Day_identifier

                e = str(e)
                f =  datetime.datetime.strptime(e, "%Y-%m-%d %H:%M:%S").strftime('%s')
                d_in_ms = int(float(f)*1000)

                # d = datetime.strptime("20-12-2016", "%d-%m-%Y").strftime('%s.%f')
                # d_in_ms = int(float(d)*1000)
                # print(d_in_ms)

                scores["Total_Profit"].append(a) 
                scores["Profit_Factor"].append(b) 
                scores["Profitable"].append(c) 
                scores["Max_Drawdown"].append(d) 
                scores["x"].append(d_in_ms)
                # scores["x"].append(e)


        print '--------------------------------I AM GETTING THE PERFROMANCE OF A STRATEGYS --------------------------------------------------'
                 
        return scores
        


    # FOR STRATEGIES PAGE  
    def getStrategies(self):

        '''data = {
            "Strategies":[
                { "Strategy_id":"001","Strategy":"40_20_YES","Buy":40,"Sell":20,"Optimization":"YES","Total_profit":[1,2,13,4,-5,6,15,8,9,0,11,10],"Profit_factor":[10,1,11,2,0,3,9,4,8,5,7,6],"profitable":[10,1,9,2,8,3,7,4,6,5,12,11],"x":["Jan","Feb","Mar","APR","MAY","JUNE","JULY","AUG","SEP","OCT","NOV","DEC"],"TWENTY_TP":200,"TWEENTY_PF":20,"TWEENTY_PT":20,"TWEENTY_MD":5.5},
                { "Strategy_id":"002","Strategy":"30_10_NO","Buy":30,"Sell":10,"Optimization":"NO","Total_profit":[12,-2,3,-4,-1,-2,-4,8,9,1,11,10],"Profit_factor":[10,-1,11,2,0,-3,9,-4,8,-5,7,-6],"profitable":[10,1,9,-2,8,-3,7,4,-6,-5,12,-11],"x":["Jan","Feb","Mar","APR","MAY","JUNE","JULY","AUG","SEP","OCT","NOV","DEC"],"TWENTY_TP":400,"TWEENTY_PF":40,"TWEENTY_PT":25,"TWEENTY_MD":15.5},  
            ]
        }'''

        yourdict = {
            "Strategies":[]
        }

        strategy_names = []

        # LOADING THE LATEST STORED STRATEGIES
        entities = Strategy.query.order_by(desc(Strategy.Created_at)).limit(10).all()
          
        print 'length_entities',len(entities)

        for i in range(0,len(entities)):  

            # print entities[i].Created_at
            print entities[i].Symbol
            
            Optimization = entities[i].Optimization

            Strategy_id = entities[i].id

            params = entities[i].Params

            isFavourite = entities[i].isFavourite



            st = str(params["buying_angle"])+'_'+str(params["selling_angle"])+'_'+ "{}".format(entities[i].Optimization)
            Total_Profit = []
            Profit_factor = []
            profitable = []
            x = []

            def myFunction(milliseconds):
                date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
                startday = date.strftime('%Y-%m-%d')
                datee = datetime.datetime.strptime(startday, "%Y-%m-%d")
                a = datee.year 
                b =  datee.month
                c =  datee.day
                return a,b,c 


            starttime = entities[i].Start_time
            endtime = entities[i].End_time

            print 'starttime',starttime
            print 'endtime',endtime

            a,b,c = myFunction(starttime)
            start_date = str(date(a, b, c))
            a,b,c = myFunction(endtime)
            end_date = str(date(a, b, c+1))
                  

            print start_date,end_date
              
            # FROM DAILY METRIC GET THE VALUES 
            db_get = Daily_metric.query.filter(and_( Daily_metric.Day_identifier.between(start_date,end_date), Daily_metric.Symbol=='TVIX',))
        
            dailydata_length = db_get.count()

            print 'dailydata_length',dailydata_length

            Total_Profit = []
            Profit_factor = []
            profitable = []
            Max_Drawdown= []
            x = []

            current_strategy = [params["buying_angle"],params["selling_angle"],params["optimization"],params["relative_angle"],params["stop_order"],params["less_than_buy"]]
           
            # THIS LOOP WILL GET THE SAVED STARTEGY DAILY METRIC VALUES
            for i in range(0,dailydata_length):
               
                if (db_get[i].Strategy["buying_angle"] == current_strategy[0] and db_get[i].Strategy["selling_angle"]==current_strategy[1] and db_get[i].Strategy["optimization"]==current_strategy[2] and db_get[i].Strategy["relative_angle"]==current_strategy[3] and  db_get[i].Strategy["stop_order"]==current_strategy[4] and db_get[i].Strategy["less_than_buy"]==current_strategy[5]):  
                    
                    e = db_get[i].Day_identifier
                    e = str(e)
                    f =  datetime.datetime.strptime(e, "%Y-%m-%d %H:%M:%S").strftime('%s')
                    d_in_ms = int(float(f)*1000)
                    Total_Profit.append(db_get[i].Total_Profit)
                    Profit_factor.append(db_get[i].Profit_Factor)
                    profitable.append(db_get[i].Profitable)
                    Max_Drawdown.append(db_get[i].Max_Drawdown)
                    x.append(d_in_ms)


            print start_date,end_date 
            TWENTY_TP = 0 
            TWENTY_PF = 0
            TWENTY_PT = 0
            TWENTY_MD = 0

            db_gettotalmetric = Total_metric.query.filter(and_( Total_metric.Start_Date == starttime, Total_metric.End_Date == endtime ,))
            dailydata_length = db_gettotalmetric.count()
            for i in range(0,dailydata_length):

                if (db_gettotalmetric[i].Strategy["buying_angle"] == current_strategy[0] and db_gettotalmetric[i].Strategy["selling_angle"]==current_strategy[1] and db_gettotalmetric[i].Strategy["optimization"]==current_strategy[2] and db_gettotalmetric[i].Strategy["relative_angle"]==current_strategy[3] and  db_gettotalmetric[i].Strategy["stop_order"]==current_strategy[4] and db_gettotalmetric[i].Strategy["less_than_buy"]==current_strategy[5]):

                    TWEENTY_TP = round(db_gettotalmetric[i].Total_Profit,3)
                    TWEENTY_PF = round(db_gettotalmetric[i].Profit_Factor ,3)
                    TWEENTY_PT = round(db_gettotalmetric[i].Profitable,3)
                    TWENTY_MD  = db_gettotalmetric[i].Max_Drawdown

                    
            b = {
                "Strategy_id":Strategy_id ,
                "Strategy":st,
                "Buy":params["buying_angle"],
                "Sell":params["selling_angle"],
                "Optimization": Optimization,
                "Total_profit": Total_Profit,
                "Profit_factor": Profit_factor,
                "profitable": profitable,
                "Max_Drawdown":Max_Drawdown,
                "x": x ,
                "TWENTY_TP" : TWEENTY_TP , 
                "TWENTY_PF" : TWEENTY_PF,
                "TWENTY_PT" : TWEENTY_PT,
                "TWENTY_MD" : TWENTY_MD ,
                "isFavourite" : isFavourite
            }

            yourdict["Strategies"].append(b)
            # print yourdict

            n =  len(yourdict["Strategies"])
            strategy_names = []

            for i in range(0,n):
                a = yourdict["Strategies"][i]
                strategy_names.append(a["Strategy"])
            
       
        return yourdict, strategy_names


           
    def MarketData(self,START_DATE,END_DATE):

        # HERE DATA NEEDS TO BE FETCH IT FROM THE DATABASE
        '''stock_symbol = 'TVIX'
        START_DATE = str(START_DATE )
        END_DATE = str(END_DATE)
        url = 'https://api.tdameritrade.com/v1/marketdata/'+ stock_symbol +'/pricehistory?apikey=AMERITRADES79&periodType=day&frequencyType=minute&frequency=1&endDate='+END_DATE+'&startDate=' +START_DATE+ '&needExtendedHoursData=true'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        # return data

        stock_data = []

        for i in range (0,len(data['candles'])):
            stock_data.append([data['candles'][i]['datetime'],data['candles'][i]['open'],data['candles'][i]['high'],
            data['candles'][i]['low'],data['candles'][i]['close'],data['candles'][i]['volume']])
    
        return stock_data'''
      
        
     
        db_data = price_data.query.filter(and_(price_data.Time_stamp.between(START_DATE,END_DATE),price_data.stock_symbol=='TVIX'))
        

        fetchdata_length = db_data.count()
        print 'fetchdata_length',fetchdata_length

        stock_data = []
            
        # stock_data = [[db_data[i].Opening_price, db_data[i].High,db_data[i].Low,db_data[i].Closing_price,db_data[i].Volume ] for i in range(0,fetchdata_length)]
        
        for candle in db_data:

            Time_stamp = int(candle.Time_stamp)
            Opening = candle.Opening_price
            High = candle.High
            Low = candle.Low
            close = candle.Closing_price
            Volume = candle.Volume

            stock_data.append([Time_stamp,Opening,High,Low,close,Volume])

        # print stock_data
        import operator
        stock_data = sorted(stock_data, key=operator.itemgetter(0)) 
        print stock_data
        return stock_data
            
    
       



