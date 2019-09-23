import requests,json,time,urllib2

import sys
sys.dont_write_bytecode=True

def td_ameritrade(stock_symbol,START_DATE,END_DATE):

    # access_token = "rBfeG4W9u5yfeRu9BcvHDxP5P7G0ZpAa3yl4/cgl4G2EU1tUR6s1cmyOleFr+YF5ACQrz+t5BywlKduNZJnNugNJmVO6I1S+yYujSojSL/dV4bSCmGdWTB4UqPbKolIeyjR6djcrM8pHY8vWbfMoTv2rg7l+e8UoQv01s2Es3yeG1S+OQEGSyXccwieb1VjmUm5yvAGv5StiYMA24R5gz1/4HYvXtGzoowRc2irU8h+30L23R187KwZzhK7t8XvXdUeHug76INbrWF0hvwaqyL5Yxzpl84kzACC+a2dQIXlMLE0BNJrqCr3xmD7fFKAyYK0IjoJ1c++jsW5f8Un48EQv3AY+qyUdOctocEZanHhvH5cjKo6mupeklyzR8VlPDpBqMQBp02m9W/ygfZNJV7cQ9aNtodUBATkKHbYDyfNPGS2nmndVhyQiBKEBcJFp9yU4KorUfy6xHOVSiAAldDgFHw89KwE/GpM08Tje4PKYrozYgf3CngA4/JqWcDBe6v9uA100MQuG4LYrgoVi/JHHvlAU6CMIxDHlw2hgfN5YyrkjC/5/v659qOROwN4Lj9aLwYFgrmdA0KkcPSxoXMZlueDIXX0F+roetAn4XKy7nQdocqdNOBvSBpAKZxAoXhqgpd86+dTvF+LGgbXxCyMmCkEf1xpr6NDOELm3kmkcmy3/9mJUFmqM0UtO+UoXaDezdWLoI8HdIehynXiXBnCNsY/vzH9qMzxpd7nQfsOsHfKvVwn0lu7k/ZY5HKA7ZF8UWmPeJ6WHZ5SoXrHIqYoGG4qqrc8XXNHYPy/Xguv5TzmJtkEmt6IEPqJAl5uuSZSZfADYdqNvIM76Thp2aLe+1JJHjoNTYf/E9hm6CGdUQo20TFYYCUYh5QImbP0OgHg+N7L+FQc9P6lE2KPwOhc1aDYMLm+GuOZUwejc+jc5Alu7i0Rz6LeMnj70SQ84ZmX/9fGr5J43fP1XRbvF6c3uS5cMwstu+JMfb+zvDjU72afv3E8uEjoUIu51b+7OdtyePChE71aBzpazYzWWvv8Zjdd+m4rf212FD3x19z9sWBHDJACbC00B75E"
    url = 'https://api.tdameritrade.com/v1/marketdata/'+ stock_symbol +'/pricehistory?apikey=AMERITRADES79&periodType=day&frequencyType=minute&frequency=1&endDate='+END_DATE+'&startDate=' +START_DATE+ '&needExtendedHoursData=true'
    
    '''header = {
        "Authorization": "Bearer "  +access_token 
    }'''

    #GETING DATA FROM TDAMERITRADE
    #request = urllib2.Request(url,headers=header)
    
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = json.loads(response.read())
     
    # LOGIC FOR CONVERTING MARKET DATA INTO THE LIST OF LISTS
    stock_data = []

    for i in range (0,len(data['candles'])):
        stock_data.append([data['candles'][i]['datetime'],data['candles'][i]['open'],data['candles'][i]['high'],
        data['candles'][i]['low'],data['candles'][i]['close'],data['candles'][i]['volume']])
    
    
    print len(stock_data)

    return stock_data

