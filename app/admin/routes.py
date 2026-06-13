from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Subject, Enrollment, Grade

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    total_students = User.query.filter_by(role='student').count()
    total_subjects = Subject.query.count()
    total_enrollments = Enrollment.query.count()
    return render_template('admin/dashboard.html',
        total_students=total_students,
        total_subjects=total_subjects,
        total_enrollments=total_enrollments)

@admin.route('/subjects', methods=['GET', 'POST'])
@login_required
def subjects():
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        units = request.form.get('units')
        schedule = request.form.get('schedule')
        slots = request.form.get('slots')
        subject = Subject(code=code, name=name, units=units, schedule=schedule, slots=slots)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin.route('/subjects/<int:subject_id>')
@login_required
def view_subject(subject_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    subject = Subject.query.get_or_404(subject_id)
    enrollments = Enrollment.query.filter_by(subject_id=subject_id).all()
    return render_template('admin/subject_view.html', subject=subject, enrollments=enrollments)

@admin.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        units = request.form.get('units')
        schedule = request.form.get('schedule')
        slots = request.form.get('slots')

        existing = Subject.query.filter(Subject.code == code, Subject.id != subject_id).first()
        if existing:
            flash('Subject code already exists!', 'error')
            return redirect(url_for('admin.edit_subject', subject_id=subject_id))

        subject.code = code
        subject.name = name
        subject.units = units
        subject.schedule = schedule
        subject.slots = slots
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin.view_subject', subject_id=subject_id))

    return render_template('admin/subject_edit.html', subject=subject)

@admin.route('/subjects/delete/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    subject = Subject.query.get_or_404(subject_id)
    enrollments = Enrollment.query.filter_by(subject_id=subject_id).all()
    for enrollment in enrollments:
        grade = Grade.query.filter_by(enrollment_id=enrollment.id).first()
        if grade:
            db.session.delete(grade)
        db.session.delete(enrollment)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted!', 'success')
    return redirect(url_for('admin.subjects'))

@admin.route('/students')
@login_required
def students():
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    students = User.query.filter_by(role='student').all()
    return render_template('admin/students.html', students=students)

@admin.route('/students/<int:student_id>')
@login_required
def view_student(student_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    student = User.query.filter_by(id=student_id, role='student').first_or_404()
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    return render_template('admin/student_view.html', student=student, enrollments=enrollments)

@admin.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    student = User.query.filter_by(id=student_id, role='student').first_or_404()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing = User.query.filter(User.email == email, User.id != student_id).first()
        if existing:
            flash('Email already registered!', 'error')
            return redirect(url_for('admin.edit_student', student_id=student_id))

        student.name = name
        student.email = email
        if password:
            student.password = password
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('admin.view_student', student_id=student_id))

    return render_template('admin/student_edit.html', student=student)

@admin.route('/students/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    student = User.query.filter_by(id=student_id, role='student').first_or_404()
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    for enrollment in enrollments:
        grade = Grade.query.filter_by(enrollment_id=enrollment.id).first()
        if grade:
            db.session.delete(grade)
        db.session.delete(enrollment)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted!', 'success')
    return redirect(url_for('admin.students'))

@admin.route('/grades', methods=['GET', 'POST'])
@login_required
def grades():
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('student.dashboard'))
    if request.method == 'POST':
        enrollment_id = request.form.get('enrollment_id')
        grade_value = request.form.get('grade')
        remarks = request.form.get('remarks')
        
        # Robust conversion of grade input
        if grade_value == '' or grade_value is None:
            parsed_grade = None
        else:
            try:
                parsed_grade = float(grade_value)
            except (ValueError, TypeError):
                parsed_grade = None
                
        grade = Grade.query.filter_by(enrollment_id=enrollment_id).first()
        if grade:
            grade.grade = parsed_grade
            grade.remarks = remarks
        else:
            grade = Grade(enrollment_id=enrollment_id, grade=parsed_grade, remarks=remarks)
            db.session.add(grade)
        db.session.commit()
        flash('Grade updated!', 'success')
    enrollments = Enrollment.query.all()
    return render_template('admin/grades.html', enrollments=enrollments)