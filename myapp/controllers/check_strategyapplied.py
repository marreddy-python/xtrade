from myapp.models.users import Trades,db,Strategy
import json 
def applied_or_not(s,start,end):
   
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

    current_strategy = score 

    db_get_strategies =  Trades.query.filter(Trades.Symbol=='TVIX').all()
    fetched_length = len(db_get_strategies)
    print fetched_length
    stored_strategies = []

    for st in range(0,fetched_length):
        strategies = db_get_strategies[st].Strategy  
        if  db_get_strategies[st].buy_time == start and db_get_strategies[st].Sell_time == end:
            stored_strategies.append(strategies)

    # Check if current strategy is exist in strategies table 
    if (current_strategy in stored_strategies):  
        return 'exist'
    else:
        return 'notexist'


def strategy_savedornot(s,start,end):
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

    current_strategy = score 
   
    db_get_strategies =  Strategy.query.filter(Strategy.Symbol=='TVIX').all()
    fetched_length = len(db_get_strategies)
    print fetched_length
    stored_strategies = []

    for st in range(0,fetched_length):
        strategies = db_get_strategies[st].Strategy  
        if  db_get_strategies[st]. Start_time == start and db_get_strategies[st].End_time == end:
            stored_strategies.append(strategies)

    # Check if current strategy is exist in strategies table 
    if (current_strategy in stored_strategies):  
        return 'saved'
    else:
        return 'notsaved'


 