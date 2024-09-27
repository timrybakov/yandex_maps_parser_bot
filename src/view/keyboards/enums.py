from enum import Enum


class BeforeParsingEnum(str, Enum):
    start = 'start'
    before_rules = 'before_rules'
    after_rules = 'after_rules'
    info = 'info'


class StatusCheckEnum(str, Enum):
    status = 'status'
    download = 'download'


class Buttons(Enum):
    start_parsing = 'Начать 🏃'
    rules = 'Правила 📖'
    info = 'Информация по запросу 📊'
    after_rules = 'Продолжить ⏩'
    status_check = 'Статус задачи 🔍'
    download_file = 'Скачать файл 📄'
