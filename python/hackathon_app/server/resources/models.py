import flask
import flask_restful  # type: ignore
import flask_restful.fields  # type: ignore

import sheets

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

