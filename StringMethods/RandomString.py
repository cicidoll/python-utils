import random, string

def random_unicode(long: int) -> str:
    """ 随机生成指定长度的中文字符串 """
    long = 0 if long <= 0 else long
    def create_chr(sub_long: int) -> str:
        return "".join([chr(random.randint(0x4e00, 0x9fbf)) for _ in range(sub_long)])
    return create_chr(long)

