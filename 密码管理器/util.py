import json


def add_json_value(file_name, key, value):
    # 读取现有的 JSON 数据
    try:
        with open(file_name, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    # 更新现有数据或创建新的数据
    existing_data[key] = value

    # 将更新后的数据写入文件
    with open(file_name, "w") as f:
        json.dump(existing_data, f)


def add_json_array(file_name, key, json_data):
    # 读取现有的 JSON 数据
    try:
        with open(file_name, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    # 更新现有数据或创建新的数据
    if key not in existing_data:
        existing_data[key] = []
    existing_data[key].append(json_data)

    # 将更新后的数据写入文件
    with open(file_name, "w") as f:
        json.dump(existing_data, f)
