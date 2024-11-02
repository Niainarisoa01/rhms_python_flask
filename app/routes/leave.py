from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.leave import Leave
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime, timedelta

bp = Blueprint('leave', __name__, url_prefix='/leaves')

class LeaveForm(FlaskForm):
    leave_type = SelectField('Type de congé', 
                           choices=[
                               ('vacation', 'Congés payés'),
                               ('sick', 'Congé maladie'),
                               ('personal', 'Congé personnel')
                           ],
                           validators=[DataRequired()])
    start_date = DateField('Date de début', validators=[DataRequired()])
    end_date = DateField('Date de fin', validators=[DataRequired()])
    reason = TextAreaField('Motif')

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError('La date de fin doit être postérieure à la date de début')

@bp.route('/')
@login_required
def index():
    if current_user.is_admin:
        leaves = Leave.query.order_by(Leave.created_at.desc()).all()
    else:
        leaves = Leave.query.filter_by(employee_id=current_user.employee.id)\
                          .order_by(Leave.created_at.desc()).all()
    return render_template('leaves/list.html', 
                         title='Demandes de congés',
                         leaves=leaves)

@bp.route('/request', methods=['GET', 'POST'])
@login_required
def request_leave():
    form = LeaveForm()
    if form.validate_on_submit():
        leave = Leave(
            employee_id=current_user.employee.id,
            leave_type=form.leave_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            reason=form.reason.data,
            status='pending'
        )
        db.session.add(leave)
        db.session.commit()
        flash('Votre demande de congé a été soumise avec succès')
        return redirect(url_for('leave.index'))
    
    return render_template('leaves/request.html',
                         title='Demande de congé',
                         form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    leave = Leave.query.get_or_404(id)
    if not current_user.is_admin and leave.employee_id != current_user.employee.id:
        flash('Vous n\'êtes pas autorisé à voir cette demande de congé')
        return redirect(url_for('leave.index'))
    
    return render_template('leaves/view.html',
                         title='Détails du congé',
                         leave=leave)

@bp.route('/<int:id>/approve', methods=['POST'])
@login_required
def approve(id):
    if not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à approuver les congés')
        return redirect(url_for('leave.index'))
    
    leave = Leave.query.get_or_404(id)
    leave.status = 'approved'
    db.session.commit()
    flash('La demande de congé a été approuvée')
    return redirect(url_for('leave.view', id=id))

@bp.route('/<int:id>/reject', methods=['POST'])
@login_required
def reject(id):
    if not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à rejeter les congés')
        return redirect(url_for('leave.index'))
    
    leave = Leave.query.get_or_404(id)
    leave.status = 'rejected'
    db.session.commit()
    flash('La demande de congé a été rejetée')
    return redirect(url_for('leave.view', id=id))

@bp.route('/calculate-days', methods=['POST'])
@login_required
def calculate_days():
    data = request.get_json()
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    
    # Calculer le nombre de jours ouvrables (lundi-vendredi)
    days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 0-4 représentent lundi-vendredi
            days += 1
        current_date += timedelta(days=1)
    
    return jsonify({'days': days})

@bp.route('/my-leaves')
@login_required
def my_leaves():
    leaves = Leave.query.filter_by(employee_id=current_user.employee.id)\
                       .order_by(Leave.created_at.desc()).all()
    return render_template('leaves/my_leaves.html',
                         title='Mes congés',
                         leaves=leaves) 