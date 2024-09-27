import asyncio

from celery import Task, current_app
from celery.exceptions import Ignore
from src.di import di_container

from ..exceptions import parser_exceptions
from .celery import app


@app.task(bind=True)
def parse_task(
    self: Task,
    city: str,
    org_type: str
) -> None:
    try:
        self.update_state(
            state='PROCESS'
        )
        asyncio.get_event_loop().run_until_complete(
            di_container.parser_app.grab_data(
                city=city,
                org_type=org_type,
                task_id=self.request.id
            )
        )

    except parser_exceptions.CaptchaException:
        current_app.control.revoke(
            self.request.id,
            terminate=True
        )
        self.update_state(
            state='CAPTCHA'
        )
        raise Ignore()

    except parser_exceptions.GlobalParserException:
        current_app.control.revoke(
            self.request.id,
            terminate=True
        )
        self.update_state(
            state='CANCELED'
        )
        raise Ignore()
