from ..utils import db
from datetime import datetime, timezone

class Services(db.Model):
    __tablename__= 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text(),nullable=True)
    status = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_monthly_pay = db.Column(db.Boolean(), nullable=False)
    cost = db.Column(db.Float(), nullable=False)
    payed_at = db.Column(db.DateTime, nullable=True)
    start_payment = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        response = {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "is_monthly_pay": self.is_monthly_pay,
            "cost": self.cost,
            "payed_at": self.payed_at,
            "start_payment": self.start_payment,
            "user_id": self.user_id
        }
        return response
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
