from pprint import pprint
from typing import List

import json
import sheets


def get_json(flask_client, url: str):
    response = flask_client.get(url)
    result = response.json
    return result


def get_projects(flask_client):
    data = get_json(flask_client, "/projects")
    assert len(data) > 0
    # projects: List[sheets.Project] = []
    # for item in result:
    #     projects.append(sheets.Project(item))
    # return projects
    return data

def get_project(flask_client, project_id):
    data = get_json(flask_client, f"/projects/{project_id}")
    # return sheets.Project(data)
    return data


# https://flask.palletsprojects.com/en/1.1.x/testing/
def test_project_list(flask_client):
    get_projects(flask_client)


def test_get_project(flask_client):
    projects = get_projects(flask_client)
    project = projects[0]
    project_id = project["id"]
    assert project_id is not None
    actual = get_json(flask_client, f"/projects/{project_id}")
    assert project["id"] == actual["id"]
    reg = actual["registration"]
    assert reg is not None
    user = reg["user"]
    assert user is not None
    assert user["id"] is not None
    assert user["org_role"] is not None
