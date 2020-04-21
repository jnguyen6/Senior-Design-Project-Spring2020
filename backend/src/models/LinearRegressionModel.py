from app import db

class LinearRegressionPredictionModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)

    b0_age_email = db.Column(db.Float, unique=False, nullable=False)
    b1_age_email = db.Column(db.Float, unique=False, nullable=False)
    b2_age_email = db.Column(db.Float, unique=False, nullable=False)

    b0_age_paper = db.Column(db.Float, unique=False, nullable=False)
    b1_age_paper = db.Column(db.Float, unique=False, nullable=False)
    b2_age_paper = db.Column(db.Float, unique=False, nullable=False)

    b0_age_text = db.Column(db.Float, unique=False, nullable=False)
    b1_age_text = db.Column(db.Float, unique=False, nullable=False)
    b2_age_text = db.Column(db.Float, unique=False, nullable=False)

    b0_income_email = db.Column(db.Float, unique=False, nullable=False)
    b1_income_email = db.Column(db.Float, unique=False, nullable=False)
    b2_income_email = db.Column(db.Float, unique=False, nullable=False)

    b0_income_paper = db.Column(db.Float, unique=False, nullable=False)
    b1_income_paper = db.Column(db.Float, unique=False, nullable=False)
    b2_income_paper = db.Column(db.Float, unique=False, nullable=False)

    b0_income_text = db.Column(db.Float, unique=False, nullable=False)
    b1_income_text = db.Column(db.Float, unique=False, nullable=False)
    b2_income_text = db.Column(db.Float, unique=False, nullable=False)

    b0_gender_email = db.Column(db.Float, unique=False, nullable=False)
    b1_gender_email = db.Column(db.Float, unique=False, nullable=False)
    b2_gender_email = db.Column(db.Float, unique=False, nullable=False)

    b0_gender_paper = db.Column(db.Float, unique=False, nullable=False)
    b1_gender_paper = db.Column(db.Float, unique=False, nullable=False)
    b2_gender_paper = db.Column(db.Float, unique=False, nullable=False)

    b0_gender_text = db.Column(db.Float, unique=False, nullable=False)
    b1_gender_text = db.Column(db.Float, unique=False, nullable=False)
    b2_gender_text = db.Column(db.Float, unique=False, nullable=False)

    b0_bill_email = db.Column(db.Float, unique=False, nullable=False)
    b1_bill_email = db.Column(db.Float, unique=False, nullable=False)
    b2_bill_email = db.Column(db.Float, unique=False, nullable=False)

    b0_bill_paper = db.Column(db.Float, unique=False, nullable=False)
    b1_bill_paper = db.Column(db.Float, unique=False, nullable=False)
    b2_bill_paper = db.Column(db.Float, unique=False, nullable=False)

    b0_bill_text = db.Column(db.Float, unique=False, nullable=False)
    b1_bill_text = db.Column(db.Float, unique=False, nullable=False)
    b2_bill_text = db.Column(db.Float, unique=False, nullable=False)


    def __repr__(self):
        return f'<Assigned Unique ID={self.uid}'