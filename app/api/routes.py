from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.models import User, Subject, Enrollment

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{
        'id': s.id,
        'code': s.code,
        'name': s.name,
        'units': s.units,
        'schedule': s.schedule,
        'slots': s.slots
    } for s in subjects])

@api.route('/students', methods=['GET'])
def get_students():
    students = User.query.filter_by(role='student').all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'email': s.email
    } for s in students])

@api.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')

    existing = Enrollment.query.filter_by(
        student_id=student_id,
        subject_id=subject_id
    ).first()

    if existing:
        return jsonify({'message': 'Already enrolled!'}), 400

    subject = Subject.query.get(subject_id)
    if not subject or subject.slots <= 0:
        return jsonify({'message': 'No available slots!'}), 400

    enrollment = Enrollment(student_id=student_id, subject_id=subject_id)
    subject.slots -= 1
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({'message': 'Enrolled successfully!'}), 201

@api.route('/grades/<int:student_id>', methods=['GET'])
def get_grades(student_id):
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'subject': e.subject.name,
        'status': e.status,
        'grade': e.grade.grade if e.grade else None,
        'remarks': e.grade.remarks if e.grade else None
    } for e in enrollments])