import json
import logging
import os
import time
import re


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data import EMAIL, PASSWORD, CUSTOMER, RESTAURANT

def add_dish_to_not_found(file_path, dish_name):
    """
    Добавляет блюдо, которое не найдено, в файл JSON.

    Если файл уже существует, загружаем существующие данные
    """
    data = ['Авторский кофе и матча', 'Алкоголь', 'Блинчики', 'Горячие напитки', 'Десерты', 'Детское меню', 'Добавки', 'Добавки, сиропы', 'Завтраки весь день', 'игра', 'Какао и горячий шоколад']

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            logging.warning(f"Файл {file_path} повреждён.")

    """Проверяем что бы не было дубликатов"""
    if not any(dish.get("name") == dish_name for dish in data):
        data.append({"name": dish_name})
        logging.info(f"Добавлено новое блюдо: {dish_name}")
    else:
        logging.info(f"Блюдо уже существует в файле: {dish_name}")

    """Сохраняем обновлённые данные обратно в файл"""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Ошибка при записи в файл {file_path}: {e}")



class MenuReplacement:

    array_of_done_categories = []

    def __init__(self, driver):
        self.driver = driver
        self.not_found_file = "dish_not_found.json"
        self.menu = self.read_json_file('Moskvarium_new.json')

    def read_json_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

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

    def navigate_to_dishes(self):
        """Переходит на страницу с блюдами."""
        try:
            devices_expand_menu = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-test="sidebar-item-1"]'))
            )
            devices_expand_menu.click()

            dishes = WebDriverWait(devices_expand_menu, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Dishes'))
            )
            dishes.click()
        except Exception as e:
            logging.error(f"Ошибка перехода на страницу с блюдами: {e}")

    def find_location(self):
        """Ищет локацию"""
        try:
            input_zone = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "_33efVvY_gbJV_j0BCMV_t_"))
            )

            customer_input_field = WebDriverWait(input_zone, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ant-select-selection-search-input"))
            )
            customer_input_field.send_keys(CUSTOMER)
            customer_input_field.send_keys(Keys.RETURN)

            customer_name = WebDriverWait(input_zone, 10).until(
                EC.element_to_be_clickable((By.ID, 'rc_select_1'))
            )
            customer_name.send_keys(RESTAURANT)
            customer_name.send_keys(Keys.RETURN)

            category_select = WebDriverWait(input_zone, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="CategorySelect"]'))
            )

            category_name = WebDriverWait(category_select, 10).until(
                EC.element_to_be_clickable((By.ID, 'rc_select_2'))
            )

            category_name.click()
            category_name.send_keys('холодный')
            category_name.send_keys(Keys.RETURN)

        except Exception as e:
            logging.error(f"Ошибка при выборе локации и ресторана: {e}")

    def edit_all_dishes_on_location(self):
        """Редактирует все блюда на локации."""

        time.sleep(1)
        for i in range(0, 12):
            page_with_dishes = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, '_2nI6s17vktU6utdDQbVnBh'))
            )
            try:
                dish = WebDriverWait(page_with_dishes, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'div[data-test^="Item-{i}"]'))
                )
            except:
                break

            edit_dish_link = WebDriverWait(dish, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, 'a'))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(edit_dish_link).perform()
            edit_dish_link.click()

            time.sleep(2)

            input_fields = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test="InputFields"]'))
            )

            time.sleep(1)
            input_pos_name = WebDriverWait(input_fields, 10).until(
                EC.visibility_of_element_located((By.ID, 'basic_posName'))
            )
            dish_pos_name = input_pos_name.get_attribute('value')
            id_input_field = WebDriverWait(input_fields, 10).until(
                EC.element_to_be_clickable((By.ID, 'basic_externalId'))
            )

            input_dish_ams_name = WebDriverWait(input_fields, 10).until(
                EC.visibility_of_element_located((By.ID, 'basic_name'))
            )
            dish_ams_name = input_dish_ams_name.get_attribute('value')


            dish_id_in_system = id_input_field.get_attribute('value')

            dish_id = self.find_dish_id(dish_pos_name)
            if dish_id is None:
                self.save_not_found_dish(dish_ams_name)
                self.go_back()
            elif dish_id == dish_id_in_system:
                self.go_back()
            else:
                actions.scroll_to_element(id_input_field).perform()
                id_input_field.click()
                id_input_field.send_keys(Keys.COMMAND + 'a')
                id_input_field.send_keys(Keys.BACKSPACE)
                id_input_field.send_keys(dish_id)

                time.sleep(0.5)

                self.save_changes()

    def save_not_found_dish(self, dish_name):
        """Сохраняет ненайденное блюдо в файл."""
        try:
            add_dish_to_not_found(self.not_found_file, dish_name)
        except Exception as e:
            logging.error(f"Ошибка при добавлении блюда в файл: {e}")

    def find_dish_id(self, dish_pos_name):

        def find_ids_by_name(data, target_names):
            result = {}

            # Приводим все имена из POS к чистому виду
            normalized_targets = [name.strip().lower() for name in target_names]

            for entry in data:
                dish_name = entry.get("name")
                if dish_name is None:
                    continue

                normalized_name = dish_name.strip().lower()

                if normalized_name in normalized_targets:
                    result[dish_name] = entry.get("id")
                    return result

            return result

        normalized_dish_name = dish_pos_name.strip().lower()
        target_names = [normalized_dish_name]

        found_ids = find_ids_by_name(self.menu, target_names)
        
        if not found_ids:
            if dish_pos_name != normalized_dish_name:
                found_ids = find_ids_by_name(self.menu, [dish_pos_name])
            
            if not found_ids:
                return None

        return next(iter(found_ids.values()))


    def go_back(self):
        self.driver.back()

    def save_changes(self):
        """Сохраняет изменения."""
        buttons_container = self.driver.find_element(By.CSS_SELECTOR, 'div[data-test="BtnBlock"]')

        save_button = buttons_container.find_element(By.CLASS_NAME, 'Pg5_LEyCAQYvKp0VlGc9O')
        save_button.click()

        time.sleep(1)


    def move_next_category(self):
        actions = ActionChains(self.driver)

        input_zone = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_33efVvY_gbJV_j0BCMV_t_"))
        )

        category_select = WebDriverWait(input_zone, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="CategorySelect"]'))
        )
        span_category_name = WebDriverWait(category_select, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ant-select-selection-item'))
        )
        category_name = span_category_name.get_attribute('title')
        categories_area = category_select.find_element(By.CLASS_NAME, '_3CqNloW2J85icWeUqpaYe7')

        self.array_of_done_categories.append(category_name)

        actions.click(categories_area).perform()
        time.sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        actions.send_keys(Keys.RETURN).perform()

        new_category_name = span_category_name.get_attribute('title')
        print('Имя новой категории = ',new_category_name)

        return new_category_name not in self.array_of_done_categories


    def move_to_next_page(self):
        time.sleep(1)
        pagination_container = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="PaginationComponent"]'))
        )
        next_page_button = pagination_container.find_element(By.XPATH, '//ul//li[@title="Next Page"]')
        if next_page_button.get_attribute('aria-disabled') == 'false':
            print('внутри if next_page_button.get_attribute("aria-disabled") == "false"')
            next_page_button.click()
            return True
        else:
            print('внутри else next_page_button.get_attribute("aria-disabled") == "false"')
            return False


def run_script():
    """Основной запуск скрипта."""
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    page = MenuReplacement(driver)

    page.open_page()
    page.login()
    page.navigate_to_dishes()
    page.find_location()
    while True:
        page.edit_all_dishes_on_location()
        if not page.move_to_next_page():
            if not page.move_next_category():
                print(page.array_of_done_categories)
                break



logging.basicConfig(level=logging.INFO)
run_script()

