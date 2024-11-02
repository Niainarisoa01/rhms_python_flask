from app import create_app, db
from app.models.user import User
from app.models.employee import Employee
from app.models.department import Department
from datetime import date, timedelta

def init_db():
    app = create_app()
    with app.app_context():
        # Créer les tables
        db.create_all()
        
        # Créer un département test
        dept = Department(name="Ressources Humaines", description="Département RH")
        db.session.add(dept)
        db.session.commit()
        
        # Créer un utilisateur admin
        admin = User(
            email="admin@example.com",
            username="admin",
            role="admin"
        )
        admin.set_password("password123")
        db.session.add(admin)
        db.session.commit()
        
        # Créer un employé admin
        admin_employee = Employee(
            user_id=admin.id,
            first_name="Admin",
            last_name="User",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            department_id=dept.id,
            position="Administrateur RH",
            salary=50000,
            hire_date=date.today() - timedelta(days=365)
        )
        db.session.add(admin_employee)
        db.session.commit()

if __name__ == "__main__":
    init_db() 