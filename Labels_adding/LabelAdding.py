import json
import logging
import time

from data import EMAIL, PASSWORD, URL, URL_STAGING, EMAIL_STAGING, PASSWORD_STAGING
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class LabelsAdding:
    def __init__(self, driver):
        self.driver = driver
        self.labels = self.read_json_file('survey_wordings.json')

    def read_json_file(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def write_json(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def open_page(self):
        """Открывает страницу и разворачивает окно браузера."""
        try:
            self.driver.get(URL)
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

    def navigate_to_admin_settings(self):
        """Переходит на страницу с блюдами."""
        try:
            admin_settings = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-test="sidebar-item-8"]'))
            )
            admin_settings.click()
            logging.info("Переход на страницу с устройствами выполнен успешно")
        except Exception as e:
            logging.error(f"Ошибка перехода на страницу с устройствами: {e}")
            time.sleep(1.5)

    def navigate_to_add_new_label(self):
        """Переходит на страницу с вордингами."""
        add_new_label_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME,
                                        '_1cs1RpCHfaSmXcY_A2NOmB.Pg5_LEyCAQYvKp0VlGc9O._2nJUiuMlI6FA29rk-RDUta._3SGMGUZsG4NsPXTwdeTsqq'))
        )
        add_new_label_button.click()

    def print_object(self):

        for label in self.labels:
            label_type = label.get('Wording group')
            label_key = label.get('Key')
            label_rus = label.get('Label_rus')
            label_eng = label.get('Label_eng')

            form = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'basic'))
            )

            category_input = WebDriverWait(form, 10).until(
                EC.element_to_be_clickable((By.ID, 'basic_IDSelectedCategory'))
            )

            category_input.click()
            category_input.send_keys(label_type)
            category_input.send_keys(Keys.RETURN)
            key_input = WebDriverWait(form, 10).until(
                EC.element_to_be_clickable((By.ID, 'basic_key'))
            )
            key_input.click()
            key_input.send_keys(label_key)

            languages = {
                "Russian": label.get("Russian"),
                "English": label.get("English"),
                "Chinese": label.get("Chinese"),
                "French": label.get("French"),
                "German": label.get("German"),
                "Spanish": label.get("Spanish"),
                "Italian": label.get("Italian"),
                "Polish": label.get("Polish"),
                "Slovak": label.get("Slovak"),
                "Danish": label.get("Danish"),
                "Ukrainian": label.get("Ukrainian")
            }

            for lang, text in languages.items():
                if text:
                    label_field_container = WebDriverWait(form, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'div[data-test="LabelField-{lang}"]'))
                    )
                    label_input = WebDriverWait(label_field_container, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input'))
                    )
                    label_input.click()
                    label_input.send_keys(label_rus if lang in ["Russian", "Ukrainian"] else label_eng)

                    text_field_container = WebDriverWait(form, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'div[data-test="ValueField-{lang}"]'))
                    )
                    field_input = WebDriverWait(text_field_container, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'ant-input'))
                    )
                    field_input.click()
                    field_input.send_keys(text)

            self.save_changes()

    def save_changes(self):
        """Сохраняет изменения."""
        buttons_container = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="BtnBlock"]'))
        )

        save_button = buttons_container.find_element(By.CLASS_NAME,
                                                     '_1cs1RpCHfaSmXcY_A2NOmB.Pg5_LEyCAQYvKp0VlGc9O._2nJUiuMlI6FA29rk-RDUta._3SGMGUZsG4NsPXTwdeTsqq._2988Xi6PWy-xCSbGhwBR-W')
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

        time.sleep(0.5)
        success_modal_container = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="ModalSentSuccessfullyIsVisible"]'))
        )

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )
        confirm_success = WebDriverWait(success_modal_container, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )
        confirm_success.click()


def run_script():
    """Основной запуск скрипта."""
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    page = LabelsAdding(driver)

    page.open_page()
    page.login()
    page.navigate_to_admin_settings()
    page.navigate_to_add_new_label()
    page.print_object()


logging.basicConfig(level=logging.INFO)
run_script()

# 657
