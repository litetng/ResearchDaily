import os
from dotenv import load_dotenv

# 1. 加载 .env 文件中的所有变量
load_dotenv()

# 2. 安全地获取 API Key
api_key = os.getenv("GEMINI_API_KEY")

# 3. 检查是否获取成功（可选的防御性编程）
if not api_key:
    raise ValueError("⚠️ 找不到 API Key，请检查根目录下的 .env 文件是否配置正确！")

# 接下来就可以把 api_key 传给你的大模型调用函数了
print("API Key 加载成功！")