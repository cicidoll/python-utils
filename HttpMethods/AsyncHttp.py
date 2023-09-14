from loguru import Logger
from asyncio import AbstractEventLoop, Task
from typing import List
import asyncio, aiohttp, json

# HTTP请求超时设置
TIME_OUT_SETTING: int = 60

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
        self._tasks: List[Task] = []
        # http请求列表
        self._request_list: list = []
        # 新建线程池
        self.loop: AbstractEventLoop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)

    def add_request_async(self, url: str, data: dict, headers={}) -> None:
        """ 配置loop: 新增请求 """
        # 保存请求
        self._request_list.append({"headers": headers, "data": data, "url": url})
        # 新增请求
        sub_request = self.send_post(url, data, headers)
        # 添加进队列
        self._tasks.append(asyncio.ensure_future(sub_request))

    def start_async_loop(self) -> None:
        """ 配置loop管理: 启动线程池 """
        try:
            if len(self._tasks) == 0:
                self.logger.error("事件队列为空，请检查")
                return
            # 支持多线程的async
            self.loop.run_until_complete(asyncio.wait(self._tasks))
            # 检查异步请求发送情况 若有异常 则重新发起
            self._tasks = self.__process_tasks(self._tasks, self._request_list)
        except Exception as identifier:
            self.logger.error("启动事件线程池失败，请检查")
            self.logger.error(identifier)

    def __process_tasks(self, old_task_list: List[Task], request_list: list) -> List[Task]:
        """ 检查异步请求发送情况 若有网络异常 则重新发起 """
        new_task_list: List[Task] = old_task_list
        times: int = 0
        while [i for i in new_task_list if i.result() == None or i == None] != []:
            temp_task_list: List[Task] = []
            index_list: list = []
            # 创建新的请求
            for i in range(len(new_task_list)):
                if new_task_list[i].result() != None and new_task_list[i] != None: continue
                times += 1
                sub_request = self.send_post(**request_list[i])
                sub_task: Task = asyncio.ensure_future(sub_request)
                temp_task_list.append(sub_task)
                index_list.append(
                    {
                        "index": i,
                        "sub_task": sub_task
                    }
                )
            self.loop.run_until_complete(asyncio.wait(temp_task_list))
            # 替换旧请求
            for i in range(len(temp_task_list)):
                if temp_task_list[i].result() == None or temp_task_list[i] == None: continue
                new_task_list[index_list[i]["index"]] = index_list[i]["sub_task"]
        if times != 0:
            self.logger.warning("网络不稳定，已重发%d个异常网络请求" % times)
        return new_task_list

    def close_loop(self) -> None:
        """ 关闭线程池 """
        try:
            self.loop.close()
        except Exception as identifier:
            self.logger.error("关闭事件线程池失败，请检查")
            self.logger.error(identifier)

    def get_result(self, index: int) -> dict:
        try:
            return self._tasks[index].result()
        except Exception as identifier:
            self.logger.error(identifier)

    def clear_async_tasks(self) -> None:
        """ 清空任务列表 """
        self._tasks = []
        self._request_list = []

    async def send_post(self, url: str, data: dict, headers: dict) -> dict:
        """ 发起Post请求-返回的结果中附带请求参数 """
        try:
            async with self._sem:
                async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as sess:
                    async with sess.post(url, data=json.dumps(data)) as response:
                        return await response.json()
        except Exception as identifier:
            self.logger.error(identifier)
            return None