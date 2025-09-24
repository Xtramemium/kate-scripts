import pandas as pd
import json


def xlsx_to_json(xlsx_file, sheet_name, json_file):
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name)

    data = df.to_dict(orient='records')

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

xlsx_to_json("general_wordings.xlsx", "New wordings", '../survey_wordings.json')
