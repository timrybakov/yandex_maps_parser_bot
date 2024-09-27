from typing import Dict, List, Optional

from databases.interfaces import Record

from .sources.user_system.user_system_postgres import UserSystemPostgres


class UserSystem:

    def __init__(
        self,
        source: UserSystemPostgres
    ) -> None:
        self._source = source

    async def bulk_create(
        self,
        data: List[Dict[str, str]]
    ) -> None:
        await self._source.bulk_create(
            data=data
        )

    async def select_all_by_task_id(
        self,
        task_id: str
    ) -> Optional[List[Record]]:
        return await self._source.select_all(
            values={
                'task_id': task_id
            }
        )
