from loguru import Logger
from asyncio import AbstractEventLoop
from typing import List
import asyncio, aiohttp, json

class AsyncPostHttpView:
    """ 使用协程实现异步Post批量请求-控制器 """

    def __init__(self, sem: int, logger: Logger) -> None:
        self.async_post_http: AsyncPostHttpModel = AsyncPostHttpModel(sem, logger)

    def run(self, posts_list: List[dict]) -> List[dict]:
        for post in posts_list:
            # 将请求参数依次添加进异步队列
            self.async_post_http.add_request_async(post["url"], post["data"], post["headers"])
        # 启动事件池
        self.async_post_http.start_async_loop()
        # 获取批量请求结果
        response_datas: list = [self.async_post_http.get_result(i) for i in range(len(posts_list))]
        # 清空任务列表
        self.async_post_http.clear_async_tasks()
        return response_datas
    
class AsyncPostHttpModel:
    """ 使用协程实现异步Post批量请求-Model """

    def __init__(self, sem: int, logger: Logger) -> None:
        # 设置日志
        self.logger: Logger = logger
        # 设置Asyncio并发数量类
        self._sem: asyncio.Semaphore = asyncio.Semaphore(sem)
        # 任务列表
        self._tasks: list = []
        # 新建线程池
        self.loop: AbstractEventLoop = asyncio.get_event_loop()

    def add_request_async(self, url: str, data: dict, headers={}) -> None:
        """ 配置loop: 新增请求 """
        # 新增请求
        sub_request = self.send_post(url, data, headers)
        # 添加进队列
        self._tasks.append(asyncio.ensure_future(sub_request))

    def start_async_loop(self) -> None:
        """ 配置loop管理: 启动线程池 """
        try:
            if len(self._tasks) == 0: return
            # 支持多线程的async
            self.loop.run_until_complete(asyncio.wait(self._tasks))
        except Exception as identifier:
            self.logger.error(identifier)

    def close_loop(self) -> None:
        """ 关闭线程池 """
        try:
            self.loop.close()
        except Exception as identifier:
            self.logger.error(identifier)

    def get_result(self, index: int) -> dict:
        try:
            return self._tasks[index].result()
        except Exception as identifier:
            self.logger.error(identifier)

    def clear_async_tasks(self) -> None:
        """ 清空任务列表 """
        self._tasks: list = []

    async def send_post(self, url: str, data: dict, headers: dict) -> dict:
        """ 发起Post请求-返回的结果中附带请求参数 """
        try:
            async with self._sem:
                async with aiohttp.ClientSession(headers=headers) as sess:
                    async with sess.post(url, data=json.dumps(data)) as response:
                        return await response.json()
        except Exception as identifier:
            self.logger.error(identifier)