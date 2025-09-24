import json

# Пример: читаем JSON из файла или строки
with open("Moskvarium.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Проходимся по каждому объекту и модифицируем поле 'name'
for item in data:
    if 'name' in item and isinstance(item['name'], str):
        item['name'] = item['name'].strip().lower()

# Сохраняем результат обратно в файл
with open("Moskvarium_new.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
