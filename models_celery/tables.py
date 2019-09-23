from celery_task import db

class price_data(db.Model):

    id = db.Column(db.Integer, primary_key = True,nullable=False)
    stock_symbol = db.Column(db.String, nullable=False)
    Time_stamp = db.Column(db.BigInteger, nullable=False)
    Opening_price = db.Column(db.Float, nullable=False)
    Closing_price = db.Column(db.Float, nullable=False)
    High = db.Column(db.Float, nullable=False)
    Low = db.Column(db.Float, nullable=False)
    Volume = db.Column(db.Float, nullable=False)
    Recorded_at = db.Column(db.String, nullable=False)

    # addresses = db.relationship("Strategy_features")


class Strategy_features(db.Model):

    id = db.Column(db.Integer, primary_key = True,nullable=False)
    # id = db.Column(db.Integer, db.ForeignKey('price_data.id'))
    Strategy_type_id = db.Column(db.String,nullable=False)
    Feature = db.Column(db.JSON,nullable=False) 
    Symbol = db.Column(db.String,nullable=False)
    Day_identifier = db.Column(db.BigInteger, nullable=False)


class Market_data_audit_log(db.Model):

    Entry_id = db.Column(db.Integer, primary_key = True,nullable=False)
    stock_symbol = db.Column(db.String, nullable=False)
    Day_identifier = db.Column(db.String, nullable=False)

