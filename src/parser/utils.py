from selenium.webdriver.remote.webelement import WebElement


class ParserUtils:

    @staticmethod
    def unify_phone_number(
        phone_number_element: WebElement
    ) -> str:
        chars_to_remove = [' (', ') ', '-']
        phone_number = phone_number_element.text
        if phone_number.startswith('8'):
            phone_number = '+7' + phone_number[1:]
        for char in chars_to_remove:
            phone_number = phone_number.replace(char, '')

        return phone_number[:12]
