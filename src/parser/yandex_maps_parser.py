import logging
from time import sleep
from typing import Dict, List

from pydantic_settings import BaseSettings
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..exceptions import parser_exceptions
from ..model import repository
from .utils import ParserUtils

logger = logging.getLogger(__name__)


class YandexMapsParserApp:

    def __init__(
        self,
        settings: BaseSettings,
        record_repository: repository.UserSystem
    ) -> None:
        self._settings = settings
        self._repository = record_repository
        self._driver = webdriver.Remote(
            command_executor=self._settings.firefox_url,
            options=self._firefox_options_init
        )
        self._wait = WebDriverWait(
            self._driver,
            timeout=5
        )

    @property
    def _firefox_options_init(self) -> webdriver.FirefoxOptions:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-cache')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        return options

    def _check_for_smart_captcha(
        self
    ) -> bool:
        try:
            self._wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'CheckboxCaptcha')
                )
            )
            return True

        except exceptions.TimeoutException:
            return False

    def fetch_data_from_url_path(
        self,
        request_path: str
    ) -> None:
        self._driver.get(request_path)

        if self._check_for_smart_captcha():
            raise parser_exceptions.CaptchaException

    def search_organizations_by_city_and_type(
        self,
        city: str,
        org_type: str
    ) -> None:
        self._check_for_smart_captcha()
        input_element = self._wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'input__control')
            )
        )
        input_element.send_keys(
            f'{city} {org_type}'
        )
        search_button = self._wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'button')
            )
        )
        search_button.click()

    def scroll_through_organizations(self) -> List[WebElement]:
        for i in range(100):
            try:
                sleep(1)
                scroll_container = self._wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'scroll__container')
                    )
                )
                self._driver.execute_script(
                    'arguments[0].scrollTop += 300;',
                    scroll_container
                )
                if i % 5 == 0:
                    self._wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, 'link-overlay')
                        )
                    )

            except exceptions.StaleElementReferenceException:
                pass

        link_element = self._driver.find_elements(
            By.CLASS_NAME,
            'link-overlay'
        )
        return link_element

    def fetch_organization_details(
        self,
        city: str,
        org_type: str,
        task_id: str,
        link_el_list: List[WebElement]
    ) -> List[Dict[str, str]]:

        org_details_list = []
        seen_orgs = set()

        for link_element in link_el_list:
            try:
                try:
                    href = link_element.get_attribute('href')
                    self._driver.execute_script(
                        f'window.open("","org_tab");'
                    )
                    self._driver.switch_to.window(
                        self._driver.window_handles[-1]
                    )
                    self.fetch_data_from_url_path(
                        request_path=href
                    )

                except parser_exceptions.CaptchaException as error:
                    logger.error(error)
                    break

                except exceptions.NoSuchElementException:
                    pass

                name_element = self._wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'orgpage-header-view__header')
                    )
                )
                phone_number_element = self._wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span[itemprop="telephone"]')
                    )
                )
                phone_number = ParserUtils.unify_phone_number(
                    phone_number_element=phone_number_element
                )
                try:
                    web_link = self._wait.until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, 'business-urls-view__link')
                        )
                    ).get_attribute('href')

                except exceptions.TimeoutException:
                    web_link = None

                org_key = (name_element.text, phone_number, web_link)

                if org_key not in seen_orgs:
                    org_info = {
                        'name': name_element.text,
                        'phone_number': phone_number,
                        'web_link': web_link,
                        'city': city,
                        'org_type': org_type,
                        'task_id': task_id
                    }

                    org_details_list.append(org_info)
                    seen_orgs.add(org_key)

                self._driver.close()
                self._driver.switch_to.window(
                    self._driver.window_handles[0]
                )

            except exceptions.TimeoutException as error:
                logger.error(error)

            finally:
                if len(self._driver.window_handles) > 1:
                    self._driver.close()
                    self._driver.switch_to.window(
                        self._driver.window_handles[0]
                    )

        return org_details_list

    async def grab_data(
        self,
        city: str,
        org_type: str,
        task_id: str
    ) -> None:
        try:
            self.fetch_data_from_url_path(
                request_path='https://www.yandex.ru/maps'
            )
            self.search_organizations_by_city_and_type(
                city=city,
                org_type=org_type
            )
            organization_data = self.scroll_through_organizations()
            data = self.fetch_organization_details(
                city=city,
                org_type=org_type,
                task_id=task_id,
                link_el_list=organization_data
            )
            await self._repository.bulk_create(
                data=data
            )

        except parser_exceptions.CaptchaException as error:
            logger.error(f'Captcha {error}')
            raise parser_exceptions.CaptchaException

        except Exception as error:
            logger.error(f'Global {error}')
            raise parser_exceptions.GlobalParserException

        finally:
            self._driver.quit()
