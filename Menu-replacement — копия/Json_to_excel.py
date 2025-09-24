import json
import pandas as pd

# Загружаем JSON-файл
with open('dish_not_found.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Извлекаем названия
names = [item["name"] for item in data]

# Создаем DataFrame
df = pd.DataFrame(names, columns=["Название блюда"])

# Сохраняем в Excel
df.to_excel('dish_names.xlsx', index=False, engine='openpyxl')
