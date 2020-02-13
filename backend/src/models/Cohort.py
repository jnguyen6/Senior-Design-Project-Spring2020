from app import db


class Cohort(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    paper = db.Column(db.String(30), unique=True, nullable=False)
    text = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f'<Cohort cid={self.cid} paper={self.paper} text={self.text} email={self.email}'
