import flask_restful  # type: ignore
import flask_restful.fields  # type: ignore


# TODO: make a function to be able to express input as a dictionary
# like the output is and then convert to a
# flask_restful.reqparse.RequestParser instance

# `POST /users` input
create_user = flask_restful.reqparse.RequestParser()
create_user.add_argument("email")
create_user.add_argument("first_name")
create_user.add_argument("last_name")
create_user.add_argument("organization")
create_user.add_argument("org_role")
create_user.add_argument("tshirt_size")

# `POST /users`  and `GET /users/<id>` output
user_details = {
    "id": flask_restful.fields.String,
    "email": flask_restful.fields.String,
    "first_name": flask_restful.fields.String,
    "last_name": flask_restful.fields.String,
    "date_created": flask_restful.fields.DateTime,
    "organization": flask_restful.fields.String,
    "org_role": flask_restful.fields.String,
    "tshirt_size": flask_restful.fields.String,
}
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
