from bot_dash import db 

class User(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    username=db.Column(db.String(150), unique=True, nullable=False)
    password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120),unique=True, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username


class Sensor1(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    sensor_value=db.Column(db.Float )


class Sensor2(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    sensor_value=db.Column(db.Float )