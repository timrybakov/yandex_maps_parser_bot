class NoRecordsException(Exception):

    def __init__(self, message='No records for current task_id.'):
        super().__init__(message)
