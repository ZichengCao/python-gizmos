import json
import os
import pyDes
import base64
import hashlib
import random
import string

PASSWORD_FILE = "passwords.json"
CONFIG_FILE = "config.json"

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


# 加载密钥
def load_key():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        if "key" in data:
            return data["key"].encode()
    # 生成加密密钥
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    add_json_value(CONFIG_FILE, "key", key)
    return key.encode()


# 加密数据
def encrypt(data, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return base64.b64encode(des.encrypt(data.encode())).decode()


# 解密数据
def decrypt(data, key):
    des = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    return des.decrypt(base64.b64decode(data)).decode()


# 加载密码数据
def load_passwords(input_website):
    try:
        with open(PASSWORD_FILE, "r") as f:
            passwords_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    passwords = []
    if input_website in passwords_data:
        accounts = passwords_data[input_website]
        for account in accounts:
            for username, encrypted_password in account.items():
                passwords.append((username, decrypt(encrypted_password, load_key())))

    return passwords

# 存储密码
def store_password():
    website = input("请输入网站名：")
    username = input("请输入账号：")
    password = input("请输入密码：")
    encrypted_password = encrypt(password, load_key())
    add_json_array(PASSWORD_FILE, website, {username: encrypted_password})
    print("密码已保存")


# 查询密码
def retrieve_password():
    input_key = input("请输入授权码：")
    if not check_master_key(input_key):
        print("授权码不正确")
        return

    website = input("请输入网站名：")

    passwords = load_passwords(website)
    if len(passwords) == 0:
        print("找不到对应的密码")
        return
    for username, password in passwords:
        print(f"账号：{username}, 密码: {password}")


# 设置授权码
def save_master_key():
    master_password = input("请设置授权码：")
    add_json_value(CONFIG_FILE, "master_password", hashlib.md5(master_password.encode()).hexdigest())
    print("授权码已设置")


def check_master_key(input_key):
    # 加载 config.json 中的授权码
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
    stored_password_hash = config_data.get("master_password")
    # 对输入密码进行加密
    input_password_hash = hashlib.md5(input_key.encode()).hexdigest()
    # 检查是否匹配
    return input_password_hash == stored_password_hash


def main():
    while True:
        print(" ------------------密码管理器菜单------------------")
        menu_options = ["0. 设置授权码", "1. 存储密码", "2. 查询密码", "3. 退出"]
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                json.dump({}, f)

        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if "master_password" in data:
                print(menu_options[1])
                print(menu_options[2])
                print(menu_options[3])
                print(" -----------------------------------------------")
                choice = input("请选择操作：")
                if choice == "1":
                    store_password()
                elif choice == "2":
                    retrieve_password()
                elif choice == "3":
                    break
                else:
                    print("无效的选择，请重新输入")
            else:
                print(menu_options[0])
                print(" -----------------------------------------------")
                choice = input("请选择操作：")
                if choice == "0":
                    save_master_key()
                else:
                    print("无效的选择，请重新输入")

        input("按任意键继续...")


if __name__ == "__main__":
    main()
