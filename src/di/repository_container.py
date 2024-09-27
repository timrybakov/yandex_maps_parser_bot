from functools import cached_property

from pydantic_settings import BaseSettings

from ..clients import postgres_client
from ..model import repository


class RepositoryContainer:
    def __init__(
        self,
        settings: BaseSettings
    ) -> None:
        self._settings = settings

    @cached_property
    def postgres_connector(self) -> postgres_client.PostgresConnector:
        return postgres_client.PostgresConnector(
            database_url=self._settings.database_url
        )

    @cached_property
    def user_system(self) -> repository.UserSystem:
        return repository.UserSystem(
            source=self._user_system_postgres
        )

    @cached_property
    def _user_system_postgres(self) -> repository.UserSystemPostgres:
        return repository.UserSystemPostgres(
            connector=self.postgres_connector
        )
