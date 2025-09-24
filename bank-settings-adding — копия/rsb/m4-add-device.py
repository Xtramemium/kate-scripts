import logging
import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EMAIL, PASSWORD, RESTAURANT, RSB_M4_URL


class BackOfficeKateMedia:

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        """Открывает страницу и разворачивает окно браузера."""
        try:
            self.driver.get(RSB_M4_URL)
            self.driver.maximize_window()
        except Exception as e:
            logging.error(f"Ошибка при открытии страницы: {e}")

    def login(self):
        """Выполняет вход на сайт с указанными данными."""
        try:
            auth_form = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'auth-form'))
            )

            email_input = WebDriverWait(auth_form, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[testid="input__login"]'))
            )
            email_input.send_keys(EMAIL)

            password_input = WebDriverWait(auth_form, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[testid="input__password"]'))
            )
            password_input.send_keys(PASSWORD)

            submit_button = WebDriverWait(auth_form, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[testid="button__login"]'))
            )
            submit_button.click()
        except Exception as e:
            logging.error(f"Ошибка входа: {e}")

    def navigate_to_devises(self):
        """Переходит на страницу с устройствами."""
        try:
            devices_menu = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-test="sidebar-item-5"]'))
            )
            devices_menu.click()
        except Exception as e:
            logging.error(f"Ошибка перехода на страницу с устройствами: {e}")

    def find_location(self):
        """Ищет локацию"""
        try:
            customer_input_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-activedescendant='rc_select_0_list_0']"))
            )
            customer_input_field.send_keys(CUSTOMER)
            customer_input_field.send_keys(Keys.RETURN)

            customer_name = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "rc_select_1"))
            )

            time.sleep(0.5)
            customer_name.send_keys(RESTAURANT)
            time.sleep(0.5)
            customer_name.send_keys(Keys.RETURN)
        except Exception as e:
            logging.error(f"Ошибка при выборе локации и ресторана: {e}")



    def edit_all_devices_on_location(self):
        """Редактирует все устройства на локации."""
        actions = ActionChains(self.driver)
        time.sleep(1)

        def check_if_devise_is_tablet(device_name_param):
            """Проверяет, является ли устройство планшетом."""
            if device_name_param.startswith('UBI') or device_name_param.startswith('NUC') or device_name_param.startswith('КС-4') or device_name_param.startswith('КС-4'):
                return False
            return True

        for i in range(0, 12):
            page_with_devices = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, '_379OyITUe5I3e0JWk9nOVX'))
            )
            try:
                device = page_with_devices.find_element(By.CSS_SELECTOR, f'div[data-test^="Item{i}"]')
            except:
                break

            device_name = device.find_element(By.CLASS_NAME, '_14JEb8M6MGYOa4D3Lq3_NR').text
            def edit_device():

                edit_device_link = WebDriverWait(device, 10).until(
                    EC.element_to_be_clickable((By.TAG_NAME, 'a'))
                )
                edit_device_link.click()
                time.sleep(2)

                form = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'ant-form.ant-form-vertical'))
                )

                hardware_id_block = form.find_element(By.CLASS_NAME, '_3EBtcSnm8brdYemfkkWAWw')
                hardware_id = hardware_id_block.find_element(By.CSS_SELECTOR, 'input[data-test="HardwareIdFieldInput"]').get_attribute('value')

                add_new_bank_block_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME,
                                                '_1cs1RpCHfaSmXcY_A2NOmB._2XB0_GxDA8jkk3srdHproI._2nJUiuMlI6FA29rk-RDUta._3SGMGUZsG4NsPXTwdeTsqq._333-B_GTirWA5PZ5PeVZS'))
                )

                actions.move_to_element(add_new_bank_block_button).perform()
                add_new_bank_block_button.click()
                time.sleep(0.5)

                single_bank_settings_block = form.find_element(By.CLASS_NAME, 'U05rEvagThTt83mk8RuDu')

                empty_settings_input = single_bank_settings_block.find_element(By.CLASS_NAME, 'ant-select-selection-search-input')
                empty_settings_input.click()
                time.sleep(0.5)
                empty_settings_input.send_keys(M4)
                empty_settings_input.send_keys(Keys.RETURN)
                terminal_id = hardware_id[4:]


                actions.send_keys(Keys.TAB).perform()
                actions.send_keys(terminal_id).perform()

                actions.send_keys(Keys.TAB).perform()
                actions.send_keys(f'{hardware_id}@katemedia.ru').perform()

                time.sleep(0.5)

                actions.send_keys(Keys.TAB).perform()
                actions.send_keys(API_PROXY_PASSWORD)
                bank_settings_block = self.driver.find_element(By.CLASS_NAME, '_1ef2dzG9HBY_IwJw34hsb5')
                proxy_password_block = bank_settings_block.find_element(By.CSS_SELECTOR,
                                                                         'div[data-test="M4PasswordField"]')
                proxy_password_input = proxy_password_block.find_element(By.CLASS_NAME, 'ant-input')

                add_new_bank_block_button.click()

                proxy_password_input.click()
                actions.send_keys(Keys.TAB).perform()
                actions.send_keys(Keys.TAB).perform()

                actions.send_keys('QR').perform()
                time.sleep(0.5)
                actions.send_keys(Keys.RETURN).perform()
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.5)
                actions.send_keys(f'SBP{terminal_id}').perform()

                self.save_changes()


            if not check_if_devise_is_tablet(device_name):
                continue
            else:
                edit_device()

    def save_changes(self):
        """Сохраняет изменения."""
        buttons_container = self.driver.find_element(By.CLASS_NAME, '_3E62ZhF-kVYesOtcK1_MwT')

        save_button = buttons_container.find_element(By.CLASS_NAME, 'Pg5_LEyCAQYvKp0VlGc9O')
        save_button.click()

        time.sleep(1)

        modals_container = self.driver.find_elements(By.CLASS_NAME, '_3r-gagQJ_2fUbOJp1OIef-')

        confirm_save_modal = next(modal for modal in modals_container if modal.find_element(By.CLASS_NAME,
                                                                                            'ev_m0xQbx9aqzGISlDMC0').text == 'Are you sure you want to save the information?')

        save_button_confirm = confirm_save_modal.find_element(By.CSS_SELECTOR, '[type="submit"]')
        save_button_confirm.click()

        success_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, '_3LCI7MHAd0fXzr-8mD0hG9'))
        )

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )

        confirm_success = success_modal.find_element(By.CSS_SELECTOR, '[type="submit"]')
        confirm_success.click()
        time.sleep(0.5)

        self.driver.back()

    def move_to_next_page(self):
        time.sleep(1)
        pagination_container = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="PaginationComponent"]'))
        )
        next_page_button = pagination_container.find_element(By.XPATH, '//ul//li[@title="Next Page"]')
        if next_page_button.get_attribute('aria-disabled') == 'false':
            next_page_button.click()
            return True
        else:
            return False


def run_script():
    """Основной запуск скрипта."""
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    page = BackOfficeKateMedia(driver)

    page.open_page()
    page.login()
    page.navigate_to_devises()
    page.find_location()
    while True:
        page.edit_all_devices_on_location()
        if not page.move_to_next_page():
            break


logging.basicConfig(level=logging.INFO)
run_script()
