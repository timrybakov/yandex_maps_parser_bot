from typing import Any, Dict, Optional

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType


class FSMSystem:
    def __init__(
        self,
        state: FSMContext
    ) -> None:
        self._state = state

    async def clear_state(self) -> None:
        await self._state.clear()

    async def get(self) -> Dict[str, Any]:
        return await self._state.storage.get_data(
            key=self._state.key
        )

    async def set(
        self,
        data: Optional[Dict[str, Any]]
    ) -> None:
        await self._state.storage.set_data(
            key=self._state.key,
            data=data
        )

    async def update(
        self,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        if data:
            kwargs.update(data)
        return await self._state.storage.update_data(
            key=self._state.key,
            data=kwargs
        )

    async def set_state(
        self,
        new_state: Optional[StateType] = None
    ) -> None:
        await self._state.storage.set_state(
            key=self._state.key,
            state=new_state
        )

    async def clear(self) -> None:
        await self.set_state(
            new_state=None
        )
        await self.set({})
