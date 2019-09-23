# from run import db
from config import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Post(db.Model):
   
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),unique=True, nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(50),unique=True, nullable=False)


class Strategy(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    Strategy_type_id = db.Column(db.String, nullable=False)
    # Tags = db.Column(db.String, nullable=False)
    Symbol = db.Column(db.String,nullable = False)
    Created_at = db.Column(db.DateTime)
    Params = db.Column(db.JSON)
    # Last_accessed = (db.DateTime)
    isFavourite = db.Column(db.Boolean,nullable = False)
    Start_time = db.Column(db.BigInteger, nullable=False)
    End_time = db.Column(db.BigInteger, nullable=False)
    Optimization = db.Column(db.String,nullable = False)
    
    addresses = db.relationship("Strategies_Grades",backref = "owner")



class Strategy_type(db.Model):

    Strategy_type_id = db.Column(db.Integer,primary_key=True,nullable = True)
    Strategy_type_name = db.Column(db.String, nullable=False)


class Strategies_Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Strategy_id = db.Column(db.Integer, db.ForeignKey("strategy.id"))
    Symbol = db.Column(db.String,nullable = False)
    isFavourite = db.Column(db.Boolean,nullable = False)
    Applied = db.Column(db.DateTime,nullable = False)
    

class Trades(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    buy_price =  db.Column(db.Float,nullable = False)
    sell_price =  db.Column(db.Float,nullable = False)
    buy_value =  db.Column(db.Float,nullable = False)
    sell_value =  db.Column(db.Float,nullable = False)
    profit_loss =  db.Column(db.Float,nullable = False)
    profit_loss_percentage =  db.Column(db.Float,nullable = False)
    buy_angle =  db.Column(db.Float,nullable = False)
    Sell_angle =  db.Column(db.Float)
    Symbol = db.Column(db.String,nullable= False)
    Type =db.Column(db.String,nullable= False)
    buy_time = db.Column(db.BigInteger, nullable=False)
    Sell_time = db.Column(db.BigInteger, nullable=False)
    Optimization =  db.Column(db.String,nullable= False)
    Day_identifier =  db.Column(db.String,nullable= False)
    Strategy = db.Column(db.JSON)


# Daily_metric table stores all the performance values for 20days
class Daily_metric(db.Model):

    id = db.Column(db.Integer,primary_key=True,nullable= False)
    Strategy = db.Column(db.JSON)
    Symbol = db.Column(db.String,nullable = False)
    Profit_loss = db.Column(db.Integer)
    Profit_loss_percentage = db.Column(db.Integer)
    Type = db.Column(db.String,nullable= False)
    Total_Profit = db.Column(db.Float)
    Profit_Factor = db.Column(db.Float)
    Profitable = db.Column(db.Float)
    Max_Drawdown = db.Column(db.Integer)
    Day_identifier = db.Column(db.DateTime,nullable= False)


class Total_metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Strategy_id = db.Column(db.String)
    Strategy = db.Column(db.JSON)
    Total_Profit = db.Column(db.Float)
    Profit_Factor = db.Column(db.Float)
    Profitable = db.Column(db.Float)
    Max_Drawdown = db.Column(db.Float)
    Start_Date = db.Column(db.BigInteger,nullable = False)
    End_Date = db.Column(db.BigInteger,nullable = False)

