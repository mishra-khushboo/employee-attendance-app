import pytest
from app import app, employees, attendance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True  # simulate login
        yield client


# ----------------------
# UNIT TESTS
# ----------------------

def test_add_employee_logic():
    employees.clear()

    emp = {'id': 1, 'name': 'Test User', 'department': 'IT'}
    employees.append(emp)

    assert len(employees) == 1
    assert employees[0]['name'] == 'Test User'


def test_delete_employee_logic():
    employees.clear()
    employees.append({'id': 1, 'name': 'A', 'department': 'IT'})

    # simulate delete logic
    eid = 1
    filtered = [e for e in employees if e['id'] != eid]

    assert len(filtered) == 0


# ----------------------
# INTEGRATION TESTS
# ----------------------

def test_dashboard_access(client):
    response = client.get('/dashboard')
    assert response.status_code == 200


def test_add_employee_route(client):
    employees.clear()

    response = client.post('/add_employee', data={
        'name': 'Rahul',
        'department': 'Engineering'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert len(employees) == 1
    assert employees[0]['name'] == 'Rahul'


def test_mark_attendance(client):
    employees.clear()
    attendance.clear()

    employees.append({'id': 1, 'name': 'Rahul', 'department': 'Engineering'})

    response = client.post('/mark_attendance', data={
        'emp_id': 1,
        'status': 'Present'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert len(attendance) == 1
    assert attendance[0]['status'] == 'Present'


def test_health_endpoint(client):
    response = client.get('/health')
    data = response.get_json()

    assert response.status_code == 200
    assert data['status'] == 'UP'