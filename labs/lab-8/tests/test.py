import pytest
from unittest.mock import patch

# tbh i've been researching pytest for (potential) work and see why it is so
# useful

def test_signup_page_loads(client):
    """signup page loads"""
    response = client.get('/signup')
    assert response.status_code == 200

def test_success_page_loads(client):
    """success page loads"""
    response = client.get('/success')
    assert response.status_code == 200

def test_error_page_loads(client):
    """error page loads"""
    response = client.get('/error')
    assert response.status_code == 200

@patch('app.insert')
def test_successful_signup(mock_insert, client):
    """successful user signup"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'john@example.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert response.status_code == 302 # homepage redir
    mock_insert.assert_called_once()

@patch('app.get_one')
def test_successful_login(mock_get_one, client):
    """successful user login"""
    import bcrypt

    signup_data = {
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'john@example.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    }

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(signup_data['Password'].encode('utf-8'), salt)

    mock_user = type('MockUser', (), {
        'FirstName': signup_data['FirstName'],
        'LastName': signup_data['LastName'],
        'Email': signup_data['Email'],
        'PhoneNumber': signup_data['PhoneNumber'],
        'Password': hashed_password.decode('utf-8')
    })()
    mock_get_one.return_value = mock_user

    response = client.post('/login', data={
        'Email': signup_data['Email'],
        'Password': signup_data['Password']
    })
    assert response.status_code == 302 # success redir
