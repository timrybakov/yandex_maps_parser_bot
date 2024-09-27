from typing import Dict, List

import tablib
from aiogram.fsm.context import FSMContext
from databases.interfaces import Record

from celery.result import AsyncResult

from .. import celery
from ..di import di_container
from ..exceptions import presenter_exceptions
from ..view import fsm


class Presenter:
    def __init__(
        self,
        state: FSMContext = None
    ) -> None:
        self._state = state

    @property
    def get_fsm_storage(self) -> fsm.FSMSystem:
        return fsm.FSMSystem(
            state=self._state
        )

    def _save_csv_file(
        self,
        task_id: str,
        data: List[Record]
    ) -> None:
        data_dicts = [dict(item) for item in data]

        data = tablib.Dataset()

        for record_dict in data_dicts:
            row = [None] + list(record_dict.values())
            data.append(row)

        with open(f'src/media/records/{task_id}.csv', 'w') as file:
            file.write(data.export('csv'))

    def start_parse_process(
        self,
        data: Dict[str, str]
    ) -> str:
        task = celery.parse_task.delay(**data)
        return task.id

    def get_status_from_queue(
        self,
        task_id: str
    ) -> str:
        task = AsyncResult(task_id)
        return task.state

    async def fetch_and_save_records_by_task_id(
        self,
        task_id: str
    ) -> None:
        data = await di_container.repository_container.user_system.select_all_by_task_id(
            task_id=task_id
        )
        if not data:
            raise presenter_exceptions.NoRecordsException

        self._save_csv_file(
            task_id=task_id,
            data=data
        )
