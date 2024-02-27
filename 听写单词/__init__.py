import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import random
import requests
from playsound import playsound
import tempfile
import threading
import time

def get_word_definitions(word):
    url = f"https://dict.youdao.com/suggest?num=5&ver=3.0&doctype=json&cache=false&le=en&q={word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            entries = data["data"]["entries"]
            definitions = [entry["explain"] for entry in entries]
            return definitions
    return None


def play_word_audio(word):
    url = f"https://dict.youdao.com/dictvoice?audio={word}&type=1"

    try:
        # 发送HTTP请求获取音频文件
        response = requests.get(url)
        if response.status_code == 200:
            # 将音频文件保存到临时文件中
            with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                temp_audio.write(response.content)
                temp_audio_path = temp_audio.name

            # 初始化pygame
            pygame.init()
            # 加载音频文件
            pygame.mixer.music.load(temp_audio_path)
            # 播放音频文件
            pygame.mixer.music.play()
            # 等待音频播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # 关闭pygame
            pygame.mixer.music.stop()
            pygame.quit()

            # 删除临时文件
            os.remove(temp_audio_path)
        else:
            print("Failed to fetch audio file from the server")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    wordlist_path = 'word.txt'

    with open(wordlist_path, 'r', encoding='utf-8') as file:
        words = file.readlines()

    while True:
        random_word = random.choice(words).strip()
        definitions = get_word_definitions(random_word)

        if definitions:
            # print("随机单词:", random_word)
            print("中文解释:")
            for definition in definitions:
                print("-", definition)

            # play_word_audio(random_word)

            thread = threading.Thread(target=play_word_audio, args=(random_word,))
            thread.start()

            user_input = input("请输入该单词的拼写（按回车提交）：")

            if user_input.strip() == random_word:
                print("拼写正确！\n")
            else:
                print("拼写错误，正确拼写为:", random_word, "\n")


if __name__ == "__main__":
    main()
