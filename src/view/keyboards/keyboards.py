from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import BeforeParsingCallback, StatusCheckCallback
from .enums import BeforeParsingEnum, Buttons, StatusCheckEnum


def get_on_start_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=Buttons.start_parsing.value,
                    callback_data=BeforeParsingCallback(
                        before_parsing=BeforeParsingEnum.start
                    ).pack()
                ),
                InlineKeyboardButton(
                    text=Buttons.rules.value,
                    callback_data=BeforeParsingCallback(
                        before_parsing=BeforeParsingEnum.before_rules
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.info.value,
                    callback_data=BeforeParsingCallback(
                        before_parsing=BeforeParsingEnum.info
                    ).pack()
                )
            ]
        ]
    )
    return inline_keyboard


def get_rules_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=Buttons.after_rules.value,
                    callback_data=BeforeParsingCallback(
                        before_parsing=BeforeParsingEnum.after_rules
                    ).pack()
                )
            ]
        ]
    )
    return inline_keyboard


def get_statuscheck_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=Buttons.status_check.value,
                    callback_data=StatusCheckCallback(
                        status_check=StatusCheckEnum.status
                    ).pack()
                ),
                InlineKeyboardButton(
                    text=Buttons.download_file.value,
                    callback_data=StatusCheckCallback(
                        status_check=StatusCheckEnum.download
                    ).pack()
                )
            ]
        ]
    )
    return inline_keyboard

