"""
@Description :  用Python实现人脸表情检测

效果：
运行程序后，选择一张图片，程序标注出人脸的位置和表情

原理：
可调用百度云的api，如https://ai.baidu.com/tech/face/detect 人脸属性分析，具体参数见文档。
程序读取文件后，根据api的要求进行操作后，解析api的返回值，在图片上标注框体和表情，并保存标注后的图片

在线调试：https://console.bce.baidu.com/tools/?_=1668482508529#/api?product=AI&project=%E4%BA%BA%E8%84%B8%E8%AF%86%E5%88%AB&parent=%E4%BA%BA%E8%84%B8%E5%9F%BA%E7%A1%80API&api=rest/2.0/face/v3/detect&method=post
文档：https://ai.baidu.com/ai-doc/FACE/yk37c1u4t#%E5%9C%A8%E7%BA%BF%E8%B0%83%E8%AF%95
@Author      :   Evan
@Time        :   2024/02/27 11:09:22
@Version     :   1.0
"""
import requests
import cv2
import json
import numpy as np
import base64
import urllib
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def detect_face_emotion(image_path, access_token):
    # 读取图片文件  image 可以通过 get_file_content_as_base64("C:\fakepath\2.jpeg",False) 方法获取
    image = cv2.imread(image_path)
    _, image_data = cv2.imencode('.jpg', image)
    image_data_str = base64.b64encode(image_data).decode('utf-8')

    # 设置请求URL和body
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    request_url = request_url + "?access_token=" + access_token
    body = {
        "image": image_data_str,
        "image_type": "BASE64",
        "face_field": "emotion"   
    }
    headers = {
        "Content-Type": "application/json"
    }

    # 发送POST请求到百度云API
    response = requests.post(request_url, headers=headers, data=json.dumps(body))
    # 解析API返回的JSON数据
    result = response.json()

    print(result)


    # 在图片上标注人脸位置和表情
    for face in result["result"]["face_list"]:
        location = face["location"]
        left_top = (int(location["left"]), int(location["top"]))
        right_bottom = (int(location["left"] + location["width"]), int(location["top"] + location["height"]))
        emotion = face["emotion"]["type"]
        cv2.rectangle(image, left_top, right_bottom, (255, 0, 0), 2)
        # 调整文本位置
        text_offset_x = 10
        text_offset_y = -10
        text_position = (left_top[0] + text_offset_x, left_top[1] + text_offset_y)
        
        # 标注表情文本
        cv2.putText(image, emotion, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 保存标注后的图片
    output_path = "annotated_image.jpg"
    cv2.imwrite(output_path, image)


    return output_path

if __name__ == "__main__":
    image_path = "face/2.jpg"
    access_token="24.7823add1b9bd275279138713786864ea.2592000.1711609417.282335-53715462"
    annotated_image_path = detect_face_emotion(image_path, access_token)