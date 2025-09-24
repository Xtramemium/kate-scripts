import json
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data import EMAIL, PASSWORD, CUSTOMER, RESTAURANT
from kt2 import kt2_array
from kc4 import kc4_array


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


class DevicesReplacement:
    array_of_deactivated_devices = []
    def __init__(self, driver):
        self.driver = driver
        self.last_checked_device = read_json_file('last_checked_device.json')

    def open_page(self):
        """Открывает страницу и разворачивает окно браузера."""
        try:
            self.driver.get("https://backoffice.katemedia.ru/home")
            self.driver.maximize_window()
            logging.info("Страница успешно открыта")
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
            logging.info("Вход выполнен успешно")
        except Exception as e:
            logging.error(f"Ошибка входа: {e}")

    def navigate_to_devices(self):
        """Переходит на страницу с блюдами."""
        try:
            devices_list = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-test="sidebar-item-5"]'))
            )
            devices_list.click()
            logging.info("Переход на страницу с устройствами выполнен успешно")
        except Exception as e:
            logging.error(f"Ошибка перехода на страницу с устройствами: {e}")
            time.sleep(1.5)

    def check_if_devices_exist(self, devices, prefix, type):

        for device in devices:
            search_container = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'xjvNTwX1zs6s79c9YekTY'))
            )

            search_input = WebDriverWait(search_container, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input'))
            )
            time.sleep(0.7)
            search_input.click()
            search_input.send_keys(Keys.COMMAND + 'a')
            search_input.send_keys(Keys.DELETE)

            time.sleep(2)
            search_input.send_keys(device)
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME,
                                                'cAl1UiAP3Gk19fMjL4Fw0._2D30JRSvX56zKnroC-47vE.ev_m0xQbx9aqzGISlDMC0._27XNBQMo6GBXsJg6-VYKMZ._2hkRzeJdGgRVd2ze1QztW0._39t6R-jr-yFWACGU_eUrpH'))
                )
                self.add_new_device(device, prefix)
            except:
                self.last_checked_device[type] = device
                write_json('last_checked_device.json', self.last_checked_device)

    def add_new_device(self, device, prefix):
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
        device_id = ' '.join(filter(None, [prefix, str(device)]))
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


        self.save_changes()

    def save_changes(self):
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
            EC.visibility_of_element_located((By.CLASS_NAME, '_3LCI7MHAd0fXzr-8mD0hG9'))
        )

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )
        
        time.sleep(0.5)
        confirm_success = success_modal.find_element(By.CSS_SELECTOR, '[type="submit"]')
        confirm_success.click()

        self.driver.back()


def run_script():
    """Основной запуск скрипта."""
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    page = DevicesReplacement(driver)

    page.open_page()
    page.login()
    page.navigate_to_devices()
    unchecked_kc4_devices = filter(lambda x: x > page.last_checked_device['kc4'], kc4_array)
    # unchecked_kt2_devices = filter(lambda x: x > page.last_checked_device['kt2'], kt2_array)
    page.check_if_devices_exist(devices=unchecked_kc4_devices, prefix='KC-4', type='kc4')
    # page.check_if_devices_exist(devices=unchecked_kt2_devices, prefix='', type='kt2')


logging.basicConfig(level=logging.INFO)
run_script()
