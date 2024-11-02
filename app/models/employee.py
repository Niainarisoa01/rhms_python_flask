from app import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    hire_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    
    # Relations
    leaves = db.relationship('Leave', backref='employee', lazy=True)
    
    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>' 