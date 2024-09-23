import pytest
from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs.exceptions import FyleError  

def test_get_assignments_student_1(client, h_student_1):
    response = client.get('/student/assignments', headers=h_student_1)
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1

def test_get_assignments_student_2(client, h_student_2):
    response = client.get('/student/assignments', headers=h_student_2)
    assert response.status_code == 200
    data = response.json['data']
    assert len(data) == 0  # Student 2 should have no assignments

def test_post_assignment_null_content(client, h_student_1):
    response = client.post('/student/assignments', headers=h_student_1, json={'content': None})
    assert response.status_code == 400
    assert "Content cannot be null" in response.json['error']

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'
    response = client.post('/student/assignments', headers=h_student_1, json={'content': content})
    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_submit_assignment_student_1(client, h_student_1, setup_data):
    # First, create a draft assignment
    content = 'Test Assignment'
    create_response = client.post('/student/assignments', headers=h_student_1, json={'content': content})
    assert create_response.status_code == 200
    assignment_id = create_response.json['data']['id']

    # Now submit the assignment
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': assignment_id, 'teacher_id': 2})
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.get_data(as_text=True)}")
    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

def test_submit_nonexistent_assignment(client, h_student_1):
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': 9999, 'teacher_id': 2})
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.get_data(as_text=True)}")
    assert response.status_code == 404
    assert "No assignment with this id was found" in response.json['error']

def test_assignment_resubmit_error(client, h_student_1, setup_data):
    # First, create a draft assignment
    content = 'Test Assignment for Resubmit'
    create_response = client.post('/student/assignments', headers=h_student_1, json={'content': content})
    assert create_response.status_code == 200
    assignment_id = create_response.json['data']['id']

    # First submission
    first_response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': assignment_id, 'teacher_id': 2})
    print(f"First submission response status: {first_response.status_code}")
    print(f"First submission response data: {first_response.get_data(as_text=True)}")
    assert first_response.status_code == 200

    # Attempt to resubmit
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': assignment_id, 'teacher_id': 2})
    print(f"Resubmission response status: {response.status_code}")
    print(f"Resubmission response data: {response.get_data(as_text=True)}")
    assert response.status_code == 400
    assert "only a draft assignment can be submitted" in response.json['error'].lower()
def test_upsert_assignment_validation_error(client, h_student_1):
    response = client.post('/student/assignments', headers=h_student_1, json={'content': ''})
    assert response.status_code == 400
    assert 'error' in response.json

def test_upsert_assignment_fyle_error(client, h_student_1, mocker):
    
    mocker.patch('core.models.assignments.Assignment.upsert', side_effect=FyleError('Test Fyle Error', 400))
    response = client.post('/student/assignments', headers=h_student_1, json={'content': 'Test Content'})
    assert response.status_code == 400
    assert 'Test Fyle Error' in response.json()['error']

def test_submit_assignment_validation_error(client, h_student_1):
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': 'not_an_integer', 'teacher_id': 2})
    assert response.status_code == 400
    assert 'error' in response.json

def test_submit_assignment_unexpected_error(client, h_student_1, mocker):
    mocker.patch('core.models.assignments.Assignment.submit', side_effect=Exception('Unexpected error'))
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': 1, 'teacher_id': 2})
    assert response.status_code == 500
    assert 'An unexpected error occurred' in response.json['error']

# New test cases to cover missing lines
def test_upsert_assignment_unexpected_error(client, h_student_1, mocker):
    mocker.patch('core.models.assignments.Assignment.upsert', side_effect=Exception('Unexpected error'))
    response = client.post('/student/assignments', headers=h_student_1, json={'content': 'Test Content'})
    assert response.status_code == 500
    assert 'An unexpected error occurred' in response.json['error']

def test_submit_assignment_fyle_error(client, h_student_1, mocker):
    mocker.patch('core.models.assignments.Assignment.submit', side_effect=FyleError('Test Fyle Error', 400))
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': 1, 'teacher_id': 2})
    assert response.status_code == 400
    assert 'Test Fyle Error' in response.json()['error']

def test_list_assignments_empty(client, h_student_1, mocker):
    mocker.patch('core.models.assignments.Assignment.get_assignments_by_student', return_value=[])
    response = client.get('/student/assignments', headers=h_student_1)
    assert response.status_code == 200
    assert len(response.json['data']) == 0
    