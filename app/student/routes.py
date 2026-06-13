from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Subject, Enrollment, Grade

student = Blueprint('student', __name__)

@student.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        flash('Access denied.', 'error')
        return redirect(url_for('admin.dashboard'))
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student/dashboard.html', enrollments=enrollments)

@student.route('/subjects')
@login_required
def subjects():
    if current_user.role != 'student':
        flash('Access denied.', 'error')
        return redirect(url_for('admin.dashboard'))
    enrolled_ids = [e.subject_id for e in Enrollment.query.filter_by(student_id=current_user.id).all()]
    subjects = Subject.query.all()
    return render_template('student/subjects.html', subjects=subjects, enrolled_ids=enrolled_ids)

@student.route('/enroll/<int:subject_id>', methods=['POST'])
@login_required
def enroll(subject_id):
    if current_user.role != 'student':
        flash('Access denied.', 'error')
        return redirect(url_for('admin.dashboard'))

    existing = Enrollment.query.filter_by(
        student_id=current_user.id,
        subject_id=subject_id
    ).first()

    if existing:
        flash('Already enrolled in this subject!', 'error')
        return redirect(url_for('student.subjects'))

    subject = Subject.query.get_or_404(subject_id)
    if subject.slots <= 0:
        flash('No available slots!', 'error')
        return redirect(url_for('student.subjects'))

    enrollment = Enrollment(student_id=current_user.id, subject_id=subject_id)
    subject.slots -= 1
    db.session.add(enrollment)
    db.session.commit()

    flash(f'Successfully enrolled in {subject.name}!', 'success')
    return redirect(url_for('student.dashboard'))

@student.route('/grades')
@login_required
def grades():
    if current_user.role != 'student':
        flash('Access denied.', 'error')
        return redirect(url_for('admin.dashboard'))
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student/grades.html', enrollments=enrollments)