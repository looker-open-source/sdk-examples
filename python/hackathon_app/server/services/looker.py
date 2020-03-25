from looker_sdk import methods40 as methods, models40 as models
import looker_sdk.error as error


class Looker:
    def __init__(self, sdk: methods.Looker40SDK):
        self.sdk = sdk

    def create_user(self, email, first_name, last_name) -> int:
        user = self.sdk.create_user(
            models.WriteUser(
                first_name=first_name, last_name=last_name, is_disabled=False
            )
        )
        assert user.id
        try:
            self.sdk.create_user_credentials_email(
                user_id=user.id, body=models.WriteCredentialsEmail(email=email)
            )
        except error.SDKError as err:
            self.sdk.delete_user(user_id=user.id)
            raise err

        return user.id
