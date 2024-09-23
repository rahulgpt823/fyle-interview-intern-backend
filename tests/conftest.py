import pytest
import json
from core import create_app, db
from core.models.users import User
from core.models.principals import Principal
from core.models.teachers import Teacher
from core.models.students import Student
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

# pytest_plugins = ['pytest-mock']

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()



@pytest.fixture(scope='function', autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        # Create users as per requirements
        users = [
            User(id=1, username="student1", email="student1@example.com"),
            User(id=2, username="student2", email="student2@example.com"),
            User(id=3, username="teacher1", email="teacher1@example.com"),
            User(id=4, username="teacher2", email="teacher2@example.com"),
            User(id=5, username="principal", email="principal@example.com")
        ]
        db.session.add_all(users)
        
        # Create principal, teachers, and students
        principal = Principal(user_id=5)
        teachers = [Teacher(user_id=3), Teacher(user_id=4)]
        students = [Student(user_id=1), Student(user_id=2)]
        db.session.add(principal)
        db.session.add_all(teachers)
        db.session.add_all(students)
        
        db.session.commit()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        yield db.session

@pytest.fixture(scope='function')
def setup_data(session):
    # Create assignments
    assignments = [
        Assignment(id=1,state=AssignmentStateEnum.SUBMITTED, student_id=1, teacher_id=3, content="ESSAY T1"),
        Assignment(id=2,state=AssignmentStateEnum.GRADED, student_id=1, teacher_id=3, content="ESSAY T2", grade=GradeEnum.B),
        Assignment(id=3,state=AssignmentStateEnum.DRAFT, student_id=1, teacher_id=None, content="DRAFT ESSAY")
    ]
    session.add_all(assignments)
    session.commit()
    return {
        'assignments': assignments
    }

@pytest.fixture(scope='function')
def setup_assignments(session):
    # Create assignments for testing
    assignments = [
        # Add assignments as needed for your tests
    ]
    session.add_all(assignments)
    session.commit()
    return assignments

@pytest.fixture
def h_student_1():
    return {'X-Principal': json.dumps({'student_id': 1, 'user_id': 1})}

@pytest.fixture
def h_student_2():
    return {'X-Principal': json.dumps({'student_id': 2, 'user_id': 2})}

@pytest.fixture
def h_teacher_1():
    return {'X-Principal': json.dumps({'teacher_id': 1, 'user_id': 3})}

@pytest.fixture
def h_teacher_2():
    return {'X-Principal': json.dumps({'teacher_id': 2, 'user_id': 4})}

@pytest.fixture
def h_principal():
    return {'X-Principal': json.dumps({'principal_id': 1, 'user_id': 5})}