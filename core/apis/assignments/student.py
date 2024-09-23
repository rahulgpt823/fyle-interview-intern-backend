import traceback
from flask import Blueprint, jsonify, current_app
from marshmallow import ValidationError
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs.exceptions import FyleError

from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)

@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)

@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    try:
        if not incoming_payload.get('content'):
            return jsonify({"error": "Content cannot be null"}), 400
        
        assignment = AssignmentSchema().load(incoming_payload)
        assignment.student_id = p.student_id
        assignment.state = AssignmentStateEnum.DRAFT

        upserted_assignment = Assignment.upsert(assignment)
        db.session.commit()
        upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
        return APIResponse.respond(data=upserted_assignment_dump)

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except FyleError as e:
        current_app.logger.error(f"FyleError: {str(e)}")
        return jsonify({"error": str(e.message)}), e.status_code
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    try:
        submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

        submitted_assignment = Assignment.submit(
            _id=submit_assignment_payload.id,
            teacher_id=submit_assignment_payload.teacher_id,
            auth_principal=p
        )
        db.session.commit()
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
        return APIResponse.respond(data=submitted_assignment_dump)
    except ValidationError as e:
        current_app.logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except FyleError as e:
        current_app.logger.error(f"FyleError: {str(e)}")
        return jsonify({"error": str(e.message)}), e.status_code
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500