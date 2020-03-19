import attr
from looker_sdk import (
    api_settings,
    auth_session,
    methods,
    requests_transport,
    serialize,
)
from looker_sdk.rtl import transport as tp


@attr.s(auto_attribs=True, kw_only=True)
class CustomConfigReader(tp.TransportSettings):
    """
    A custom configuration reader that implements the PApiSettings protocol and allows
    passing of config details as parameters. The get_client_id and get_cient_secret
    methods can be modified to fetch credentials from anywhere.
    """

    @classmethod
    def configure(cls, base_url: str, api_version: str) -> api_settings.PApiSettings:
        settings = cls(base_url=base_url, api_version=api_version)
        return settings

    def get_client_id(self) -> str:
        return "client_id"

    def get_client_secret(self) -> str:
        return "client_id"


def main():
    settings = CustomConfigReader.configure(
        base_url="https://<your-looker-server>:19999", api_version="3.1"
    )
    transport = requests_transport.RequestsTransport.configure(settings)
    sdk = methods.Looker31SDK(
        auth_session.AuthSession(settings, transport, serialize.deserialize31),
        serialize.deserialize31,
        serialize.serialize,
        transport,
    )

    me = sdk.me()
    print(me)


main()
