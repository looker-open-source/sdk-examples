from pprint import pprint


# https://flask.palletsprojects.com/en/1.1.x/testing/
def test_project_list(flask_client):
    projects = flask_client.get("/projects")
    pprint(projects)
    assert len(projects) > 0
