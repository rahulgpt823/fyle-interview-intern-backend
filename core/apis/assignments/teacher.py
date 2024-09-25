from flask import Blueprint, jsonify
from marshmallow import ValidationError
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs.exceptions import FyleError

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    print(f"Teacher ID: {p.teacher_id}")
    print(f"Number of assignments: {len(teachers_assignments)}")
    for assignment in teachers_assignments:
        print(f"Assignment ID: {assignment.id}, State: {assignment.state}, Teacher ID: {assignment.teacher_id}")
    assignments_dump = AssignmentSchema(many=True).dump(teachers_assignments)
    return APIResponse.respond(data=assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    try:
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
        assignment = Assignment.get_by_id(grade_assignment_payload.id)
        if not assignment:
            return jsonify({'error': 'FyleError', 'message': 'No assignment with this id was found'}), 404
        
        if assignment.state == AssignmentStateEnum.DRAFT:
            return jsonify({'error': 'FyleError', 'message': 'Cannot grade a draft assignment'}), 400
        
        if assignment.state == AssignmentStateEnum.GRADED:
            return jsonify({'error': 'FyleError', 'message': 'Assignment is already graded'}), 400
        
        if assignment.teacher_id != p.teacher_id:
            return jsonify({'error': 'FyleError', 'message': 'This assignment belongs to some other teacher'}), 403
        
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)
    except ValidationError as err:
        return jsonify({'error': 'ValidationError', 'message': err.messages}), 400
    except FyleError as e:
        return jsonify({'error': 'FyleError', 'message': str(e)}), e.status_code
    except Exception as e:
        return jsonify({'error': 'FyleError', 'message': 'An unexpected error occurred'}), 500