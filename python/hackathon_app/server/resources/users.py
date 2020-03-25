import dataclasses
import datetime

import flask_restful  # type: ignore
import flask_restful.fields  # type: ignore

from . import mappers
import sheets
from ..services import looker


class UserBuilder:
    @dataclasses.dataclass
    class User:
        """Object for `marshall_with` to pull data from."""

        id: str
        email: str
        first_name: str
        last_name: str
        date_created: datetime.datetime
        organization: str
        org_role: str
        tshirt_size: str

    def build_user(
        self, *, user: sheets.User, email: str, first_name: str, last_name: str
    ) -> "User":
        return self.User(
            id=user.id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_created=user.date_created,
            organization=user.organization,
            org_role=user.org_role,
            tshirt_size=user.tshirt_size,
        )


class Users(flask_restful.Resource, UserBuilder):
    def __init__(self, sheets: sheets.Sheets, looker: looker.Looker):
        self.sheets = sheets
        self.looker = looker
        super()

    @flask_restful.marshal_with(mappers.user)
    def get(self):
        return self.sheets.users.rows()

    @flask_restful.marshal_with(mappers.user_details)
    def post(self):
        create_user = mappers.create_user.parse_args()
        looker_user_id = self.looker.create_user(
            create_user.email, create_user.first_name, create_user.last_name
        )
        sheets_user = sheets.User(
            id=str(looker_user_id),
            organization=create_user.organization,
            org_role=create_user.org_role,
            tshirt_size=create_user.tshirt_size,
        )
        self.sheets.users.create(sheets_user)
        return self.build_user(sheets_user)
