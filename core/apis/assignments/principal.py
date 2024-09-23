from flask import Blueprint, jsonify
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core.models.teachers import Teacher
from core.apis.decorators import authenticate_principal, accept_payload
from core import db

principal_api = Blueprint('principal_api', __name__)

@principal_api.route('/assignments', methods=['GET'])
@authenticate_principal
def get_assignments(principal):
    assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    print(f"Fetched assignments: {assignments}")
    return jsonify({
        'data': [assignment.to_dict() for assignment in assignments]
    }), 200

@principal_api.route('/teachers', methods=['GET'])
@authenticate_principal
def get_teachers(principal):
    teachers = Teacher.query.all()
    return jsonify({
        'data': [teacher.to_dict() for teacher in teachers]
    }), 200

@principal_api.route('/assignments/grade', methods=['POST'])
@authenticate_principal
@accept_payload
def grade_assignment(payload, principal):
    assignment_id = payload.get('id')
    grade = payload.get('grade')

    if not assignment_id or not grade:
        return jsonify({'error': 'Missing assignment id or grade'}), 400

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    if assignment.state == AssignmentStateEnum.DRAFT:
        return jsonify({'error': 'Cannot grade a draft assignment'}), 400

    try:
        grade_enum = GradeEnum(grade)
    except ValueError:
        return jsonify({'error': 'Invalid grade'}), 400

    assignment.grade = grade_enum
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    return jsonify({
        'data': assignment.to_dict()
    }), 200