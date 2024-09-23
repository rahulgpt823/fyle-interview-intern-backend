
import pytest
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from core.libs.exceptions import FyleError



def test_ready_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'ready'
    assert 'time' in data

def test_fyle_error_handling(app, client):
    @app.route('/test-fyle-error')
    def raise_fyle_error():
        raise FyleError(message="Test Fyle Error", status_code=418)

    response = client.get('/test-fyle-error')
    assert response.status_code == 418
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Test Fyle Error'

def test_validation_error_handling(app, client):
    @app.route('/test-validation-error')
    def raise_validation_error():
        raise ValidationError(message="Test Validation Error")

    response = client.get('/test-validation-error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'ValidationError'
    assert 'Test Validation Error' in str(data['message'])

def test_integrity_error_handling(app, client):
    @app.route('/test-integrity-error')
    def raise_integrity_error():
        raise IntegrityError(statement=None, params=None, orig=Exception("Test Integrity Error"))

    response = client.get('/test-integrity-error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'IntegrityError'
    assert 'Test Integrity Error' in data['message']

def test_http_exception_handling(app, client):
    @app.route('/test-http-exception')
    def raise_http_exception():
        raise NotFound("Test Not Found")

    response = client.get('/test-http-exception')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'NotFound'
    assert 'Test Not Found' in data['message']

def test_unhandled_exception(app, client):
    @app.route('/test-unhandled-exception')
    def raise_unhandled_exception():
        raise ValueError("Test Unhandled Exception")

    response = client.get('/test-unhandled-exception')
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == 'InternalServerError'
    assert 'Test Unhandled Exception' in data['message']

def test_blueprint_registration(client):
    # Test that routes from registered blueprints are accessible
    response = client.get('/student/assignments')
    assert response.status_code == 401  # Assuming authentication is required

    response = client.get('/teacher/assignments')
    assert response.status_code == 401  # Assuming authentication is required

