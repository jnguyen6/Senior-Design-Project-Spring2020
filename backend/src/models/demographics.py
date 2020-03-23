from app import db

"""
Represents the demographics data file for patients
"""
class Demographics(db.Model):
    accountId = db.Column(db.Integer, primary_key=True)

    gender = db.Column(db.String(1), nullable=False)
    birthYear = db.Column(db.Integer)
    income = db.Column(db.Integer)
    billAmount = db.Column(db.Integer)
    OptOut = db.Column(db.String(50), nullable=True)


    def __repr__(self):
        return f'<Account Id ={self.uid} Birth Year={self.birthYear} Gender={self.gender} Income={self.income} Bill Amount={self.billAmount} OptOut Status={self.OptOut}'
