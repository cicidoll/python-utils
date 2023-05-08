import base64

class Convert:
    """ 字符串格式转换方法 """
    
    @staticmethod
    def str_convert_base64(input_str: str) -> str:
        """ 将字符串转为base64编码 """
        return str(base64.b64encode(input_str.encode('utf-8')), 'utf-8')
    
    @staticmethod
    def base64_convert_str(input_base64: str) -> str:
        """ 将base64编码转为字符串 """
        return str(base64.b64decode(input_base64), "utf-8")
    
    @staticmethod
    def base64_convert_hex(input_base64: str) -> str:
        """ 将base64转换为hex字符串 """
        return str(base64.b64decode(input_base64).hex())