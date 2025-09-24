import json
import logging
import time

from selenium.webdriver import ActionChains

from transfer_data import EMAIL, PASSWORD, CUSTOMER, RESTAURANT
from selenium import webdriver
from Devices import devices
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class DevicesTransfer:

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        """Открывает страницу и разворачивает окно браузера."""
        try:
            self.driver.get("https://backoffice.katemedia.ru/home")
            self.driver.maximize_window()
        except Exception as e:
            logging.error(f"Ошибка при открытии страницы: {e}")

    def login(self):
        """Выполняет вход на сайт с указанными данными."""
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "basic_email"))
            )
            email_input.send_keys(EMAIL)
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "basic_password"))
            )
            password_input.send_keys(PASSWORD)

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            submit_button.click()
        except Exception as e:
            logging.error(f"Ошибка входа: {e}")

    def navigate_to_devices(self):
        """Переходит на страницу с блюдами."""
        try:
            devices_list = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-test="sidebar-item-5"]'))
            )
            devices_list.click()
        except Exception as e:
            logging.error(f"Ошибка перехода на страницу с устройствами: {e}")
            time.sleep(1.5)

    def find_devices(self, list_of_devices):
        for device in list_of_devices:
            search_container = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'xjvNTwX1zs6s79c9YekTY'))
            )

            search_input = WebDriverWait(search_container, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input'))
            )
            time.sleep(1)

            search_input.click()
            search_input.send_keys(Keys.COMMAND + "A")
            search_input.send_keys(Keys.DELETE)

            search_input.send_keys(device)

            time.sleep(2)

            try:
                WebDriverWait(self.driver, 3.5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, '_379OyITUe5I3e0JWk9nOVX'))
                )
                self.edit_existing_device()
            except:
                self.add_new_device(device)

    def add_new_device(self, device):
        search_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'xjvNTwX1zs6s79c9YekTY'))
        )

        add_new_device_button = WebDriverWait(search_container, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME,
                                        '_1cs1RpCHfaSmXcY_A2NOmB.Pg5_LEyCAQYvKp0VlGc9O._2nJUiuMlI6FA29rk-RDUta._3SGMGUZsG4NsPXTwdeTsqq'))
        )
        add_new_device_button.click()

        hardware_id_container = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test="HardwareIdField"]'))
        )

        hardware_id_field = WebDriverWait(hardware_id_container, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input'))
        )

        hardware_id_field.click()
        device_id = device
        hardware_id_field.send_keys(device_id)

        customer_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="CustomerField"]'))
        )
        customer_input = WebDriverWait(customer_container, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-select-selection-search-input'))
        )
        customer_input.click()
        time.sleep(0.3)
        customer_input.send_keys(CUSTOMER)
        customer_input.send_keys(Keys.ENTER)

        restaurant_container = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test="RestaurantField"]'))
        )
        restaurant_input = WebDriverWait(restaurant_container, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-select-selection-search-input'))
        )
        restaurant_input.click()
        time.sleep(0.3)
        restaurant_input.send_keys(RESTAURANT)
        restaurant_input.send_keys(Keys.ENTER)

        time.sleep(1)

        self.save_new_device()

    def edit_existing_device(self):

        actions = ActionChains(self.driver)
        items_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, '_379OyITUe5I3e0JWk9nOVX'))
        )

        edit_device_link = WebDriverWait(items_container, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, 'a'))
        )
        edit_device_link.click()

        device_form = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'basic'))
        )

        time.sleep(2)

        customer_container = WebDriverWait(device_form, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test="CustomerField"]'))
        )

        customer_input = WebDriverWait(customer_container, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ant-select-selection-item'))
        )

        customer_input.click()
        time.sleep(1)
        actions.send_keys(CUSTOMER).perform()
        actions.send_keys(Keys.ENTER).perform()

        actions.send_keys(Keys.TAB)
        time.sleep(0.5)
        actions.send_keys(RESTAURANT).perform()
        actions.send_keys(Keys.ENTER).perform()

        time.sleep(2)

        self.save_changes()

    def go_back(self):
        self.driver.execute_script("window.history.go(-1)")

    def save_changes(self):
        """Сохраняет изменения."""
        buttons_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="BtnBlock"]'))
        )

        save_button = buttons_container.find_element(By.CLASS_NAME,
                                                     '_1cs1RpCHfaSmXcY_A2NOmB.Pg5_LEyCAQYvKp0VlGc9O._2nJUiuMlI6FA29rk-RDUta._3SGMGUZsG4NsPXTwdeTsqq.bc_9Ij0p_AuoRYvqYijJh')
        save_button.click()

        modals_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test=ModalWindows'))
        )

        confirm_modal = WebDriverWait(modals_container, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test=ModalToConfirmIsVisible'))
        )

        confirm_buttons_block = WebDriverWait(confirm_modal, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, '_1oD1cGTQOFqqikKsZ1pjFR'))
        )

        confirm_button = WebDriverWait(confirm_buttons_block, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test=yesButton'))
        )
        confirm_button.click()

        success_modal = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test=ModalSentSuccessfullyIsVisible]'))
        )

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )

        time.sleep(0.5)
        confirm_success = success_modal.find_element(By.CSS_SELECTOR, '[type="submit"]')
        confirm_success.click()

        self.driver.back()

    def save_new_device(self):
        """Сохраняет изменения."""
        buttons_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="BtnBlock"]'))
        )

        save_button = buttons_container.find_element(By.CLASS_NAME,
                                                     '_1cs1RpCHfaSmXcY_A2NOmB.Pg5_LEyCAQYvKp0VlGc9O._2nJUiuMlI6FA29rk-RDUta._3SGMGUZsG4NsPXTwdeTsqq.ALUixAobyuAr_UL0S7yBg')
        save_button.click()

        modals_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test=ModalWindows'))
        )

        confirm_modal = WebDriverWait(modals_container, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test=ModalToConfirmIsVisible'))
        )

        confirm_buttons_block = WebDriverWait(confirm_modal, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, '_1oD1cGTQOFqqikKsZ1pjFR'))
        )

        confirm_button = WebDriverWait(confirm_buttons_block, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test=yesButton'))
        )
        confirm_button.click()

        success_modal = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test=ModalSentSuccessfullyIsVisible]'))
        )

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )

        time.sleep(0.5)
        confirm_success = success_modal.find_element(By.CSS_SELECTOR, '[type="submit"]')
        confirm_success.click()

        time.sleep(1)
        self.driver.back()


def run_script():
    """Основной запуск скрипта."""
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    page = DevicesTransfer(driver)

    page.open_page()
    page.login()
    page.navigate_to_devices()
    page.find_devices(list_of_devices=devices)


logging.basicConfig(level=logging.INFO)
run_script()
