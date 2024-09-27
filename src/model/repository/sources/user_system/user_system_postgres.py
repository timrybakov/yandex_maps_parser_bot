from typing import Any, Dict, List, Optional

from databases.interfaces import Record

from src.clients import postgres_client

from . import queries


class UserSystemPostgres:

    def __init__(
        self,
        connector: postgres_client.PostgresConnector
    ) -> None:
        self._conn = connector

    async def bulk_create(
        self,
        data: List[Dict[str, Any]]
    ) -> None:
        await self._conn.execute_many(
            queries.CREATE_RECORDS,
            values_list=data
        )

    async def select_all(
        self,
        values: Optional[Dict[str, Any]] = None
    ) -> Optional[List[Record]]:
        return await self._conn.fetch_all(
            query=queries.SELECT_BY_TASK,
            values=values
        )
