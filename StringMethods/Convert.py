import base64, re

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
    
    @staticmethod
    def is_base64(input_str):
        """ 检测字符串是否为Base64编码 """
        base64_code = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$"
        return bool(re.match(base64_code, input_str))