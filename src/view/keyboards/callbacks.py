from aiogram.filters.callback_data import CallbackData

from .enums import BeforeParsingEnum, StatusCheckEnum


class BeforeParsingCallback(
    CallbackData,
    prefix='on_start_callback'
):
    before_parsing: BeforeParsingEnum


class StatusCheckCallback(
    CallbackData,
    prefix='status_callback'
):
    status_check: StatusCheckEnum
