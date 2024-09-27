class CaptchaException(Exception):

    def __init__(
        self,
        details: str = '',
        message: str = 'CAPTCHA detected. '
    ):
        if details:
            message += details
        super().__init__(message)


class GlobalParserException(Exception):

    def __init__(self, message: str = 'Parser Error'):
        super().__init__(message)
