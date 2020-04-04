from app import db

class Patient(db.Model):
    accountId = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(30), unique=False, nullable=False)
    birth_year = db.Column(db.Integer, unique=False, nullable=False)
    address_zip = db.Column(db.String(30), unique=False, nullable=False)
    family_income = db.Column(db.Integer, unique=False, nullable=False)
    bill_amount = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'<Account ID={self.accountId} Gender={self.gender} Birth Year={self.birth_year} Address Zip={self.address_zip} Family Income={self.family_income} Bill Amount={self.bill_amount}'