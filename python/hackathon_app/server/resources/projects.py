import flask
import flask_restful  # type: ignore
import flask_restful.fields  # type: ignore

from . import mappers
import sheets


# TODO: upgrade to python 3.8 to get typeddict and use for resource method
# return typing below

class ProjectBuilder:
    def build_project(self, project_id):
        project = self.sheets.projects.find(project_id)
        registration = self.sheets.registrations.find(project.registration_id)
        user = self.sheets.users.find(registration.user_id)
        registration.user = user
        hackathon = self.sheets.hackathons.find(registration.hackathon_id)
        registration.hackathon = hackathon
        project.registration = registration
        return project


class Projects(flask_restful.Resource, ProjectBuilder):
    def __init__(self, sheets: sheets.Sheets):
        self.sheets = sheets
        super()

    @flask_restful.marshal_with(mappers.projects)
    def get(self):
        return self.sheets.projects.rows()

    @flask_restful.marshal_with(mappers.project)
    def post(self):
        # TODO use flask_restful.reqparse.RequestParser() to parse json
        # and restrict input
        project = sheets.Project(**flask.request.json)
        self.sheets.projects.create(project)
        return self.build_project(project.id)


class Project(flask_restful.Resource, ProjectBuilder):
    def __init__(self, sheets: sheets.Sheets):
        self.sheets = sheets
        super()

    @flask_restful.marshal_with(mappers.project)
    def get(self, id):
        return self.build_project(id)

    @flask_restful.marshal_with(mappers.project)
    def patch(self, id):
        # TODO use flask_restful.reqparse.RequestParser() to parse json
        # and restrict input
        project = self.sheets.projects.find(id)
        for prop, val in flask.request.json.items():
            setattr(project, prop, val)
        self.sheets.projects.update(project)
        return self.build_project(project.id)
