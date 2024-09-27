from sqlalchemy.orm import DeclarativeBase, Mapped

from . import constants


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = 'parser_records'

    id: Mapped[constants.int_pk]
    name: Mapped[constants.base_str]
    phone_number: Mapped[constants.base_str]
    web_link: Mapped[constants.link_str]
    city: Mapped[constants.base_str]
    org_type: Mapped[constants.base_str]
    task_id: Mapped[constants.task_id_str]
    created_at: Mapped[constants.auto_datetime]
