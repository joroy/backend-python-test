
import re
import json

import pytest

from alayatodo import (
    alayatodo,
    PER_PAGE
)


@pytest.fixture
def client():
    print("Init client")
    alayatodo.app.config['TESTING'] = True
    client = alayatodo.app.test_client()

    with alayatodo.app.app_context():
        alayatodo.init_db()
        alayatodo.run_migrations()

    yield client


def login(client, username, password, follow_redirects=True):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=follow_redirects)


def logout(client, follow_redirects=True):
    return client.get('/logout', follow_redirects=True)


def test_root(client):
    response = client.get('/')
    data = response.get_data()
    assert response.status_code == 200
    assert len(data) > 0


def test_login_success(client):
    rv = login(client, "user1", "user1", follow_redirects=False)
    assert rv.headers.get('location') != "http://localhost/login"


def test_login_failure(client):
    rv = login(client, "user1", "user2", follow_redirects=False)
    assert rv.headers.get('location') == "http://localhost/login"


def test_no_todo_wihtout_description(client):
    login(client, "user1", "user1")
    response = client.post('/todo/', data=dict(
        description=''), follow_redirects=True)

    assert(re.search('Description is required', response.get_data(as_text=True)))


def test_add_todo_success(client):
    login(client, "user1", "user1")
    response = client.post('/todo/', data=dict(
        description='New todo'), follow_redirects=True)

    assert(not re.search('Description is required', response.get_data(as_text=True)))


def _get_one_todo(client):
    response = client.get('/todo/1/json')
    data = json.loads(response.get_data(as_text=True))
    return data


def test_todo_json(client):
    login(client, "user1", "user1")
    todo = _get_one_todo(client)
    assert(todo['description'] == "Vivamus tempus")


def test_todo_done_success(client):
    login(client, "user1", "user1")
    todo = _get_one_todo(client)
    before = todo['done']

    client.post('/todo/1/mark_as_done', data=dict(
                done='1'), follow_redirects=True)
    todo_after = _get_one_todo(client)
    after = todo_after['done']

    assert(not before)
    assert (after)


# REMARK: Flaky test, should refactor by adding
# a JSON response to /todo route instead
def test_pagination(client):
    login(client, "user1", "user1")
    response = client.get('/todo/')
    assert(re.search('<b>1 - {}</b> todos in\ntotal <b>5'.format(PER_PAGE),
           response.get_data(as_text=True)))
