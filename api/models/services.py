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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Services {self.name}>"
