from pydantic import BaseModel, Field
import time, os, psutil

class CountInfo(BaseModel):
    """ 测试程序运行耗时及内存占用 """

    # 运行时间
    time_result: float = Field(None)
    # 占用内存
    memory_result: float = Field(None)

    def count_time(self, func) -> callable:
        """ 装饰器：记录运行时间(单位：秒) """
        def int_time():
            time_start = time.time()
            func()
            time_end = time.time()
            self.time_result = time_end - time_start
        return int_time
    
    def count_memory(self, func) -> callable:
        """ 装饰器：记录占用内存(单位: MB) """
        def float_memory():
            pid = os.getpid()
            p = psutil.Process(pid)
            memory_start = p.memory_full_info().uss / 1024
            func()
            memory_end = p.memory_full_info().uss / 1024
            self.memory_result = memory_end - memory_start
        return float_memory