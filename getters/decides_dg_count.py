from datetime import datetime
import pandas as pd
import json
import os
from flask import url_for
import sys
sys.dont_write_bytecode=True

#FUNCTION THAT RETURNS START_DATE VALUES AND DECIDES THE DATA GROUPING COUNT VALUE


def check(ENTERED_DATE):

    #CONVERTING ENTERED_DATE TO WEEKDAY NAME
    dt = datetime.fromtimestamp(ENTERED_DATE/1000.0).strftime('%Y-%m-%d')
    year, month, day = (int(x) for x in dt.split('-'))  
    answer = pd.to_datetime(datetime(year, month, day)).weekday_name
    print answer
    #CHECKING WHETHER TO CHANGE DATAGROUPING COUNT VALUE OR NOT

    if answer=='Monday':

        START_DATE = ENTERED_DATE-(86400000*3)
        
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        filename = os.path.join(SITE_ROOT,'infile.json')
        with open(filename) as f:
            a = json.load(f)  
            a['rangeSelector']['buttons'][0]['count'] = 3

        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        filename = os.path.join(SITE_ROOT,'infile.json')
        with open(filename, 'w') as w:
            w.write(json.dumps(a))

        return START_DATE

    else:

        #IF ANSWER IS NOT MONDAY THEN TAKE PREVIOUS DAY VALUE

        START_DATE = ENTERED_DATE-(86400000)
        
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        filename = os.path.join(SITE_ROOT,'infile.json')
        with open(filename) as f:
            a = json.load(f)  
            a['rangeSelector']['buttons'][0]['count'] = 1


        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        filename = os.path.join(SITE_ROOT,'infile.json')
        with open(filename, 'w') as w:
            w.write(json.dumps(a))
        

        return START_DATE
    

        
        