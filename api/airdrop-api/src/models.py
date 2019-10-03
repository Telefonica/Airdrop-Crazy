from src import db

class Phone(db.Model):
    __tablename__ = 'hashes'
    hash = db.Column(db.String(64), primary_key=True)
    phone = db.Column(db.String(15))