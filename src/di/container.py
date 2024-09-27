from functools import cached_property

from .. import config, parser
from .repository_container import RepositoryContainer


class Container:
    @cached_property
    def settings(self) -> config.Settings:
        return config.Settings()

    @cached_property
    def repository_container(self) -> RepositoryContainer:
        return RepositoryContainer(
            settings=self.settings
        )

    @property
    def parser_app(self) -> parser.YandexMapsParserApp:
        return parser.YandexMapsParserApp(
            settings=self.settings,
            record_repository=self.repository_container.user_system
        )
