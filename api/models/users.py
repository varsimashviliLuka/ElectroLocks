from ..utils import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=True)
    phone_number = db.Column(db.String(45), nullable=True)
    password_hash = db.Column(db.Text(),nullable=False)
    balance = db.Column(db.Float(), default=0.0, nullable=True)
    status = db.Column(db.Integer(), default=0, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    services = db.relationship('Services', backref='users', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_permission(self):
        return self.is_admin


