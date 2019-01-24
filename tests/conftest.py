# import os
# import tempfile

# import pytest

# from alayatodo import alayatodo


# @pytest.fixture
# def app():
#     """Create and configure a new app instance for each test."""
#     # create a temporary file to isolate the database for each test
#     db_fd, db_path = tempfile.mkstemp()
#     # create the app with common test config
#     app = create_app({
#         'TESTING': True,
#         'DATABASE': db_path,
#     })

#     # create the database and load test data
#     with app.app_context():
#         init_db()
#         get_db().executescript(_data_sql)

#     yield app

#     # close and remove the temporary database
#     os.close(db_fd)
#     os.unlink(db_path)


# @pytest.fixture
# def client():
#     db_fd, alayatodo.app.config['DATABASE'] = tempfile.mkstemp()
#     alayatodo.app.config['TESTING'] = True
#     client = alayatodo.app.test_client()

#     with alayatodo.app.app_context():
#         alayatodo.init_db()
#         alayatodo.run_migrations()

#     yield client

#     os.close(db_fd)
#     os.unlink(alayatodo.app.config['DATABASE'])
