import pytest
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

@pytest.mark.usefixtures("setup_database", "setup_assignments")
class TestPrincipalAPI:
    def test_get_teachers(self, client, h_principal):
        response = client.get('/principal/teachers', headers=h_principal)
        assert response.status_code == 200
        assert isinstance(response.json['data'], list)
        assert len(response.json['data']) > 0
        for teacher in response.json['data']:
            assert 'id' in teacher
            assert 'user_id' in teacher

    def test_get_assignments(self, client, h_principal):
        response = client.get('/principal/assignments', headers=h_principal)
        assert response.status_code == 200
        data = response.json['data']
        assert len(data) == 2  # Only SUBMITTED and GRADED assignments should be returned
        states = [assignment['state'] for assignment in data]
        assert AssignmentStateEnum.SUBMITTED.value in states
        assert AssignmentStateEnum.GRADED.value in states

    def test_grade_assignment_draft_assignment(self, client, h_principal, setup_data):
        draft_assignment = next(a for a in setup_data['assignments'] if a.state == AssignmentStateEnum.DRAFT)
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': draft_assignment.id,
                'grade': GradeEnum.A.value
            },
            headers=h_principal
        )
        assert response.status_code == 400
        assert 'Cannot grade a draft assignment' in response.json['error']

    def test_grade_assignment(self, client, h_principal, setup_data):
        submitted_assignment = next(a for a in setup_data['assignments'] if a.state == AssignmentStateEnum.SUBMITTED)
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': submitted_assignment.id,
                'grade': GradeEnum.C.value
            },
            headers=h_principal
        )
        assert response.status_code == 200
        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == GradeEnum.C.value

    def test_regrade_assignment(self, client, h_principal, setup_data):
        graded_assignment = next(a for a in setup_data['assignments'] if a.state == AssignmentStateEnum.GRADED)
        new_grade = GradeEnum.A if graded_assignment.grade != GradeEnum.A else GradeEnum.B
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': graded_assignment.id,
                'grade': new_grade.value
            },
            headers=h_principal
        )
        assert response.status_code == 200
        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == new_grade.value

    def test_grade_assignment_not_found(self, client, h_principal):
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 9999,  # Non-existent assignment ID
                'grade': GradeEnum.A.value
            },
            headers=h_principal
        )
        assert response.status_code == 404
        assert 'Assignment not found' in response.json['error']

    def test_grade_assignment_invalid_grade(self, client, h_principal, setup_data):
        submitted_assignment = next(a for a in setup_data['assignments'] if a.state == AssignmentStateEnum.SUBMITTED)
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': submitted_assignment.id,
                'grade': 'INVALID_GRADE'
            },
            headers=h_principal
        )
        assert response.status_code == 400
        assert 'Invalid grade' in response.json['error']

    def test_grade_assignment_missing_id(self, client, h_principal):
        response = client.post(
            '/principal/assignments/grade',
            json={
                'grade': GradeEnum.A.value
            },
            headers=h_principal
        )
        assert response.status_code == 400
        assert 'Missing assignment id or grade' in response.json['error']

    def test_grade_assignment_missing_grade(self, client, h_principal, setup_data):
        submitted_assignment = next(a for a in setup_data['assignments'] if a.state == AssignmentStateEnum.SUBMITTED)
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': submitted_assignment.id
            },
            headers=h_principal
        )
        assert response.status_code == 400
        assert 'Missing assignment id or grade' in response.json['error']