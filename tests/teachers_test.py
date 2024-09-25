import pytest
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

def test_get_assignments_teacher_1(client, h_teacher_1, setup_data):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )
    
    assert response.status_code == 200
    
    data = response.json['data']
    assert len(data) == 3  # Assuming teacher 1 has 3 assignments
    for assignment in data:
        assert assignment['teacher_id'] == 1  # teacher_id for teacher 1

# def test_get_assignments_teacher_2(client, h_teacher_2):
#     response = client.get(
#         '/teacher/assignments',
#         headers=h_teacher_2
#     )
#     assert response.status_code == 200
#     data = response.json['data']
#     print(f"Response data: {data}")
#     assert len(data) == 1 

def test_grade_assignment_success(client, h_teacher_1, setup_data):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )
    
    assert response.status_code == 200
    data = response.json['data']
    assert data['grade'] == 'A'
    assert data['state'] == 'GRADED'

def test_grade_assignment_cross(client, h_teacher_2, setup_data):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )
    
    assert response.status_code == 403
    data = response.json
    assert data['error'] == 'FyleError'
    assert 'belongs to some other teacher' in data['message'].lower()

def test_grade_assignment_bad_grade(client, h_teacher_1, setup_data):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )
    
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'

def test_grade_assignment_bad_assignment(client, h_teacher_1):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )
    
    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'
    assert 'no assignment with this id was found' in data['message'].lower()

def test_grade_assignment_draft_assignment(client, h_teacher_1, setup_data):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 3,
            "grade": "A"
        }
    )
    
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
    assert 'cannot grade a draft assignment' in data['message'].lower()

def test_grade_already_graded_assignment(client, h_teacher_1, setup_data):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 2,
            "grade": "A"
        }
    )
    
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
    assert 'assignment is already graded' in data['message'].lower()

@pytest.mark.parametrize("grade", list(GradeEnum))
def test_grade_assignment_all_valid_grades(client, h_teacher_1, setup_data, grade):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": grade.value
        }
    )
    
    assert response.status_code == 200
    data = response.json['data']
    assert data['grade'] == grade.value

def test_grade_assignment_server_error(client, h_teacher_1, setup_data, mocker):
    mocker.patch('core.models.assignments.Assignment.mark_grade', side_effect=Exception("Unexpected error"))
    
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )
    
    assert response.status_code == 500
    data = response.json
    assert data['error'] == 'FyleError'
    assert 'an unexpected error occurred' in data['message'].lower()