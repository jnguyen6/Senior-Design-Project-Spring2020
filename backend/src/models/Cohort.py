from app import db

class Cohort(db.Model):
    uid = db.Column(db.Integer, primary_key=True)

    cid = db.Column(db.Integer)
    paper = db.Column(db.Integer)
    text = db.Column(db.Integer)
    email = db.Column(db.Integer)

    ageMin = db.Column(db.Integer)
    ageMax = db.Column(db.Integer)
    gender = db.Column(db.String(1), nullable=False)
    incomeMin = db.Column(db.Integer)
    incomeMax = db.Column(db.Integer)
    billAmountMin = db.Column(db.Integer)
    billAmountMax = db.Column(db.Integer)

    def __repr__(self):
        return f'<Unique Id ={self.uid} Cohort cid={self.cid} Age range={self.ageMax}-{self.ageMax} Gender={self.gender} Income Range={self.incomeMin}-{self.incomeMax} Bill range={self.billAmountMin}-{self.billAmountMax}'

    def initialize(self, ageMin, ageMax, gender, incomeMin, incomeMax, billAmountMin, billAmountMax):
        self.ageMin = ageMin
        self.ageMax = ageMax
        self.gender = gender
        self.incomeMin = incomeMin
        self.incomeMax = incomeMax
        self.billAmountMin = billAmountMin
        self.billAmountMax = billAmountMax