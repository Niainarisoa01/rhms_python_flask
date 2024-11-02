from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.employee import Employee
from app.models.department import Department
from app.models.user import User
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, FloatField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import datetime

bp = Blueprint('employee', __name__, url_prefix='/employees')

class EmployeeForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date de naissance', validators=[DataRequired()])
    gender = SelectField('Genre', choices=[('M', 'Masculin'), ('F', 'Féminin')], validators=[DataRequired()])
    address = StringField('Adresse')
    phone = StringField('Téléphone')
    department_id = SelectField('Département', coerce=int)
    position = StringField('Poste', validators=[DataRequired()])
    salary = FloatField('Salaire', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    employees = Employee.query.paginate(page=page, per_page=10)
    departments = Department.query.all()
    return render_template('employees/list.html', 
                         title='Liste des Employés',
                         employees=employees,
                         departments=departments)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = EmployeeForm()
    if form.validate_on_submit():
        # Créer l'utilisateur
        user = User(
            email=form.email.data,
            username=form.email.data.split('@')[0],
            role='employee'
        )
        user.set_password('password123')  # Mot de passe par défaut
        db.session.add(user)
        db.session.flush()  # Pour obtenir l'ID de l'utilisateur

        # Créer l'employé
        employee = Employee(
            user_id=user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            address=form.address.data,
            phone=form.phone.data,
            department_id=form.department_id.data,
            position=form.position.data,
            salary=form.salary.data,
            hire_date=datetime.utcnow().date()
        )
        db.session.add(employee)
        db.session.commit()
        
        flash('Employé ajouté avec succès')
        return redirect(url_for('employee.index'))
    
    return render_template('employees/add.html', 
                         title='Ajouter un Employé',
                         form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employees/view.html',
                         title=f'Profil de {employee.first_name} {employee.last_name}',
                         employee=employee) 

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    
    if form.validate_on_submit():
        # Mise à jour des informations de l'employé
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.date_of_birth = form.date_of_birth.data
        employee.gender = form.gender.data
        employee.address = form.address.data
        employee.phone = form.phone.data
        employee.department_id = form.department_id.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        
        # Mise à jour de l'email de l'utilisateur
        employee.user.email = form.email.data
        
        db.session.commit()
        flash('Employé modifié avec succès')
        return redirect(url_for('employee.view', id=employee.id))
    
    # Pré-remplir le formulaire avec les données actuelles
    form.email.data = employee.user.email
    
    return render_template('employees/edit.html',
                         title=f'Modifier {employee.first_name} {employee.last_name}',
                         form=form,
                         employee=employee)