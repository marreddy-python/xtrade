
# THIS FILE WILL DECIDE THE START AND END DATES FOR 1DAY (FOR THE CHART)

from celery_task import price_data,Strategy_features
from sqlalchemy import and_
from sqlalchemy import desc
from datetime import datetime
import pandas as pd

def myFunction():

    entities = price_data.query.order_by(desc(price_data.Time_stamp)).limit(1).all()
    print ('length_entities',len(entities))
    
    end_date =  entities[0].Time_stamp 
    print (end_date) 

    #CONVERTING ENTERED_DATE TO WEEKDAY NAME
    dt = datetime.fromtimestamp(end_date/1000.0).strftime('%Y-%m-%d')
    year, month, day = (int(x) for x in dt.split('-'))  
    print (year,month,day)

    answer = pd.to_datetime(datetime(year,month, day)).weekday_name
    print (answer)
    
    if answer=='Monday':
        start_date =  end_date - (86400000*3)
    else:
        start_date =  end_date - (86400000*1)
    
    rows = price_data.query.count()
    print ('ROWS',rows)

    return start_date,end_date

    # return start_date










