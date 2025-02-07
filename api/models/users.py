from ..utils import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45))
    phone_number = db.Column(db.String(45))
    password_hash = db.Column(db.Text(),nullable=False)
    balance = db.Column(db.Float(), default=0.0)
    status = db.Column(db.Integer())
    is_admin = db.Column(db.Boolean(), default=False)
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    services = db.relationship('Order', backref='costumer', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


