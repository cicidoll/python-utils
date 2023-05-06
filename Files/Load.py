import json

def load_json(filepath: str):
    """ 读取json文件 """
    try:
        with open(filepath, 'r', encoding='utf8') as (json_file):
            json_data = json.load(json_file)
            return json_data
    except Exception as identifier:
        print(identifier)