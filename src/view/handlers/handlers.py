from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from ... import presenter
from ...exceptions import presenter_exceptions
from .. import keyboards, templates

router = Router()


@router.message(Command('start'))
async def on_start(
    message: Message,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    await user_presenter.get_fsm_storage.clear()
    await message.answer(
        text=f'{templates.text_data['handlers']['on_start']}',
        reply_markup=keyboards.get_on_start_keyboard()
    )


@router.callback_query(
    keyboards.BeforeParsingCallback.filter(
        F.before_parsing == keyboards.BeforeParsingEnum.info
    )
)
async def status_context(
    query: CallbackQuery,
    state: FSMContext
) -> None:
    await query.message.edit_text(
        text=f'{templates.text_data['handlers']['status']}',
        inline_message_id=str(query.from_user.id),
        reply_markup=keyboards.get_statuscheck_keyboard()
    )


@router.callback_query(
    keyboards.BeforeParsingCallback.filter(
        F.before_parsing == keyboards.BeforeParsingEnum.before_rules
    )
)
async def rules_context(
    query: CallbackQuery,
    state: FSMContext
) -> None:
    await query.message.edit_text(
        text=f'{templates.text_data['handlers']['rules']}',
        inline_message_id=str(query.from_user.id),
        reply_markup=keyboards.get_rules_keyboard()
    )


@router.callback_query(
    keyboards.BeforeParsingCallback.filter(
        (F.before_parsing == keyboards.BeforeParsingEnum.start) |
        (F.before_parsing == keyboards.BeforeParsingEnum.after_rules)
    )
)
async def parse_context(
    query: CallbackQuery,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    await user_presenter.get_fsm_storage.set_state(
        new_state=keyboards.States.city
    )
    await query.message.edit_text(
        text=f'{templates.text_data['handlers']['enter_city']}',
        inline_message_id=str(query.from_user.id)
    )


@router.message(
    F.text,
    StateFilter(keyboards.States.city)
)
async def receive_city(
    message: Message,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    await user_presenter.get_fsm_storage.update(
        city=message.text
    )
    await user_presenter.get_fsm_storage.set_state(
        new_state=keyboards.States.org_type
    )
    await message.answer(
        text=f'{templates.text_data['handlers']['enter_org_type']}'
    )


@router.message(
    F.text,
    StateFilter(keyboards.States.org_type)
)
async def receive_org_type(
    message: Message,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    await user_presenter.get_fsm_storage.update(
        org_type=message.text
    )
    data = await user_presenter.get_fsm_storage.get()
    task_id = user_presenter.start_parse_process(
        data=data
    )
    await message.answer(
        text=(
            f'*Параметры поиска:*\n\n'
            f'*ID*: `{task_id}`\n'
            f'*Город поиска*: {data["city"]}\n'
            f'*Организация*: {data["org_type"]}\n\n'
            f'{templates.text_data["handlers"]["parse_process"]}'
        ),
        parse_mode='Markdown'
    )


@router.callback_query(
    keyboards.StatusCheckCallback.filter(
        F.status_check == keyboards.StatusCheckEnum.download
    )
)
async def download_file_context(
    query: CallbackQuery,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    await user_presenter.get_fsm_storage.set_state(
        new_state=keyboards.States.download
    )
    await query.message.edit_text(
        text=f'{templates.text_data['handlers']['download_file']}',
        inline_message_id=str(query.from_user.id)
    )


@router.callback_query(
    keyboards.StatusCheckCallback.filter(
        F.status_check == keyboards.StatusCheckEnum.status
    )
)
async def check_status_context(
    query: CallbackQuery,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    await user_presenter.get_fsm_storage.set_state(
        new_state=keyboards.States.status_check
    )
    await query.message.edit_text(
        text=f'{templates.text_data['handlers']['status_check']}',
        inline_message_id=str(query.from_user.id)
    )


@router.message(
    F.text,
    StateFilter(keyboards.States.status_check)
)
async def check_status(
    message: Message,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    status = user_presenter.get_status_from_queue(
        task_id=message.text
    )

    match status:
        case 'PROCESS':
            await message.answer(
                text=f'{templates.text_data['celery']['process']}'
            )
        case 'SUCCESS':
            await message.answer(
                text=f'{templates.text_data['celery']['success']}'
            )
        case 'FAILURE':
            await message.answer(
                text=f'{templates.text_data['celery']['failure']}'
            )
        case 'CAPTCHA':
            await message.answer(
                text=f'{templates.text_data['celery']['captcha']}'
            )
        case 'CANCELED':
            await message.answer(
                text=f'{templates.text_data['celery']['canceled']}'
            )
        case _:
            await message.answer(
                text=f'{templates.text_data['celery']['unknown']}'
            )


@router.message(
    F.text,
    StateFilter(keyboards.States.download)
)
async def fetch_records_to_file(
    message: Message,
    state: FSMContext
) -> None:
    user_presenter = presenter.Presenter(
        state=state
    )
    try:
        await user_presenter.fetch_and_save_records_by_task_id(
            task_id=message.text
        )
        document = FSInputFile(
            path=f'src/media/records/{message.text}.csv'
        )
        await message.answer_document(
            document=document,
            caption=f'{templates.text_data['handlers']['file_caption']}'
        )
        await message.answer(
            text=f'{templates.text_data['handlers']['after_download_file']}'
        )

    except presenter_exceptions.NoRecordsException:
        await message.answer(
            text=f'{templates.text_data['handlers']['file_caption_error']}'
        )

