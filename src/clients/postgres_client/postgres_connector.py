from typing import Any, Dict, List, Optional

from databases import Database
from databases.interfaces import Record


class PostgresConnector:
    def __init__(
        self,
        database_url: str
    ) -> None:
        self._db = Database(
            database_url
        )

    async def execute_many(
        self,
        query: str,
        values_list: List[Dict[str, Any]]
    ) -> None:
        async with self._db as db:
            await db.execute_many(
                query=query,
                values=values_list
            )

    async def fetch_all(
        self,
        query: str,
        values: Optional[Dict[str, Any]] = None,
    ) -> List[Record]:
        async with self._db as db:
            return await db.fetch_all(
                query=query,
                values=values
            )
