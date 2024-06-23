import requests
import json

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class CommonOcr(object):
    def __init__(self, img_path):
        # 请登录后前往 “工作台-账号设置-开发者信息” 查看 x-ti-app-id
        # 示例代码中 x-ti-app-id 非真实数据
        self._app_id = '4b6b60863e01c7a44acb87187efdc148'
        # 请登录后前往 “工作台-账号设置-开发者信息” 查看 x-ti-secret-code
        # 示例代码中 x-ti-secret-code 非真实数据
        self._secret_code = 'ca8ed65855c0f35bb03580bae20b0fe2'
        self._img_path = img_path

    def recognize(self):
        # 通用表格识别
        url = 'https://api.textin.com/ai/service/v2/recognize/table'
        head = {}
        try:
            image = get_file_content(self._img_path)
            head['x-ti-app-id'] = self._app_id
            head['x-ti-secret-code'] = self._secret_code
            result = requests.post(url, data=image, headers=head)
            return result.text
        except Exception as e:
            return e

if __name__ == "__main__":
    response = CommonOcr(r'./example/报告6.jpg')
    text = response.recognize()
    print(text)
    with open('6.json', 'w', encoding='utf-8') as f:
        f.write(text)
    