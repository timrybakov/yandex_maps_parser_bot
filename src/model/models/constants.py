import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]

base_str = Annotated[str, mapped_column(String(64))]

link_str = Annotated[str, mapped_column(String(1024), nullable=True)]

task_id_str = Annotated[str, mapped_column(String(36), nullable=False)]

auto_datetime = Annotated[
    datetime.datetime,
    mapped_column(DateTime, nullable=False, server_default=func.now())
]
