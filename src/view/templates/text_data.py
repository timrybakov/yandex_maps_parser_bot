import json
from typing import Dict


def get_text_data_from_json() -> Dict[str, str]:
    with open('src/view/templates/text_data.json', 'r') as f:
        return json.load(f)


text_data = get_text_data_from_json()
