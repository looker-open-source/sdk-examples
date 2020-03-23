import flask
import flask_restful  # type: ignore
import flask_restful.fields  # type: ignore

import sheets


# TODO: upgrade to python 3.8 to get typeddict and use for resource method
# return typing below
# TODO: probably should have separate resource files where user, registration,
# hackathon etc are defined?
user = {
    "id": flask_restful.fields.String,
    "date_created": flask_restful.fields.DateTime,
    "organization": flask_restful.fields.String,
    "role": flask_restful.fields.String,
    "tshirt_size": flask_restful.fields.String,
}
hackathon = {
    "id": flask_restful.fields.String,
    "name": flask_restful.fields.String,
    "description": flask_restful.fields.String,
    "location": flask_restful.fields.String,
    "date": flask_restful.fields.DateTime,
    "duration_in_days": flask_restful.fields.Integer,
}
registration = {
    "id": flask_restful.fields.String,
    "user": flask_restful.fields.Nested(user),
    "hackathon": flask_restful.fields.Nested(hackathon),
    "date_registered": flask_restful.fields.DateTime,
    "attended": flask_restful.fields.Boolean,
}
projects = {
    "id": flask_restful.fields.String,
    "registration_id": flask_restful.fields.String,
    "title": flask_restful.fields.String,
    "description": flask_restful.fields.String,
    "date_created": flask_restful.fields.DateTime,
    "project_type": flask_restful.fields.String,
    "contestant": flask_restful.fields.Boolean,
    "locked": flask_restful.fields.Boolean,
    "technologies": flask_restful.fields.String,
}
project = {
    "id": flask_restful.fields.String,
    "registration": flask_restful.fields.Nested(registration),
    "title": flask_restful.fields.String,
    "description": flask_restful.fields.String,
    "date_created": flask_restful.fields.DateTime,
    "project_type": flask_restful.fields.String,
    "contestant": flask_restful.fields.Boolean,
    "locked": flask_restful.fields.Boolean,
    "technologies": flask_restful.fields.String,
}


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

    @flask_restful.marshal_with(projects)
    def get(self):
        return self.sheets.projects.rows()

    @flask_restful.marshal_with(project)
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

    @flask_restful.marshal_with(project)
    def get(self, id):
        return self.build_project(id)

    @flask_restful.marshal_with(project)
    def patch(self, id):
        # TODO use flask_restful.reqparse.RequestParser() to parse json
        # and restrict input
        project = self.sheets.projects.find(id)
        for prop, val in flask.request.json.items():
            setattr(project, prop, val)
        self.sheets.projects.update(project)
        return self.build_project(project.id)
