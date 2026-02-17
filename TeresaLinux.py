import _thread as thread
import base64
import datetime
import hashlib
import hmac
import io
import json
import sys
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket  # 使用websocket_client
import os
import sys
import configparser
'''

在运行根目录下创建一个secret.ini格式如下：

[Credentials]
appid = *****
api_secret = *****
api_key = ****

'''

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    
    # 读取配置文件中的账号密码
    appid = config.get('Credentials', 'appid')
    api_secret = config.get('Credentials', 'api_secret')
    api_key = config.get('Credentials', 'api_key')
    
    return appid, api_secret, api_key
base_path = getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
configs = os.path.join(base_path, 'secret.ini')
logo = os.path.join(base_path, 'logo.ico')
appid, api_secret, api_key = read_config(configs)
SPARKAI_APP_ID = appid
SPARKAI_API_SECRET = api_secret
SPARKAI_API_KEY = api_key
answer =" "

def spark(input):
    from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
    from sparkai.core.messages import ChatMessage
    import re
    # 星火认知大模型Spark Max的URL值（https://www.xfyun.cn/doc/spark/Web.html）
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    # 星火认知大模型Spark Max的domain值（https://www.xfyun.cn/doc/spark/Web.html）
    SPARKAI_DOMAIN = 'generalv3.5'

    if __name__ == '__main__':
        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )
        messages = [ChatMessage(
            role="user",
            content=input
        )]
        handler = ChunkPrintHandler()
        result = spark.generate([messages], callbacks=[handler])
        a = str(result)
        pattern = r"text='(.*?)'"
        match = re.search(pattern, a)

        if match:
            extracted_text = match.group(1)
            extracted_text = extracted_text.replace('\\n', '\n')

            rresult = extracted_text
            return rresult
            print(extracted_text)
        else:
            print("Error 1")

if __name__ == "__main__":
    # 获取用户输入
    user_input = input()
    # 处理用户输入并输出结果
    result = spark(user_input)
    # 将结果输出，用于Bash脚本获取
    print(result)