import random, string

class RandomString:
    """ 随机生成指定字符串 """

    @staticmethod
    def random_unicode(long: int) -> str:
        """ 随机生成指定长度的中文字符串 """
        long = 0 if long <= 0 else long
        return "".join([chr(random.randint(0x4e00, 0x9fbf)) for _ in range(long)])

    @staticmethod
    def random_numbers(long: int) -> int:
        """ 随机生成指定位数的数字 """
        return random.randint(0, int('9'*long))

    @staticmethod
    def random_ascii_letters(long: int) -> str:
        """ 随机生成指定位数的大小写字母 """
        long = 0 if long <= 0 else long
        return "".join([random.choice(string.ascii_letters) for _ in range(long)])

    @staticmethod
    def random_punctuation(long: int) -> str:
        """ 随机生成指定位数的特殊字符 """
        long = 0 if long <= 0 else long
        return "".join([random.choice(string.punctuation) for _ in range(long)])

    @staticmethod
    def random_long_string(long: int) -> int:
        """ 随机生成指定位数的字符串(包含大小写字母、特殊字符、数字与中文) """
        long = 0 if long <= 0 else long
        template: str = string.ascii_letters + string.digits + string.punctuation + "".join([str(i) for i in range(10)]) + "".join([chr(random.randint(0x4e00, 0x9fbf)) for _ in range(96)])
        return "".join([random.choice(template) for _ in range(long)])
