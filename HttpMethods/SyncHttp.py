from requests import Response
from loguru import Logger
import requests, time, json

class SyncHttp:
    """ 同步Http请求 """

    def __init__(self, logger: Logger) -> None:
        # 初始化日志记录
        self.logger: Logger = logger

    def post(self, url: str, data: dict, headers: dict = {}) -> dict:
        """ 发送Post请求 """
        # 更新报文Headers
        headers.update({"connection": "keep-alive", "Content-Type": "application/json;charset=UTF-8"})
        # 请求返回
        for _ in range(5):
            try:
                response: Response = requests.post(
                    url, headers=headers,
                    data = json.dumps(data)
                )
                if response.status_code == 200: break
                time.sleep(0.1)
            except Exception as identifier:
                self.logger.error(identifier)
        return json.loads(response._content.decode("UTF-8"))
    
    def post_form_data(self, url: str, data: dict, headers: dict = {}) -> dict:
        """ 发送Post请求_form-data数据格式 """
        # 请求返回
        for _ in range(5):
            try:
                response: Response = requests.post(url, files=data, headers=headers)
                if response.status_code == 200: break
                time.sleep(0.1)
            except Exception as identifier:
                self.logger.error(identifier)
        return json.loads(response._content.decode("UTF-8"))