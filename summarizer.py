import os
import google.generativeai as genai
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 读取 Gemini API 密钥
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    # 针对 google-generativeai 包进行配置
    genai.configure(api_key=GEMINI_API_KEY)

def summarize_abstract(abstract: str) -> str:
    """
    接收论文的 Abstract，调用 Gemini API 生成一段 150 字以内的“核心创新点”中文总结。
    """
    if not GEMINI_API_KEY:
        return "⚠️ 未能从 .env 找到 GEMINI_API_KEY，无法调用大模型。"

    prompt = f"""
请作为资深的领域研究人员，对以下学术论文摘要进行高度凝练的总结。
要求：
1. 必须用**中文**回答。
2. 直接指出其“**核心创新点**”或“**主要贡献**”。
3. 字数严格控制在 **150字** 以内。
4. 语言要求专业、准确且精炼，无需寒暄废话。

待总结的论文摘要如下：
{abstract}
"""
    try:
        # 使用当前 API 列表内存在的最新版模型 gemini-2.5-flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        # 移除多余的换行符，使界面展示更整洁
        cleaned_text = response.text.replace('\n', ' ').strip()
        return cleaned_text
    except Exception as e:
        return f"❌ 总结生成失败，API 错误详情: {str(e)}"

if __name__ == "__main__":
    # 简单的本地测试逻辑
    print("===== 开始本地大模型测试 =====")
    test_abstract = "This paper proposes a novel transformer-based architecture for super-resolution of noisy images. We introduce a diffusion prior to stabilize training. Experiments show a 2.5dB PSNR improvement over state-of-the-art methods."
    print("输入 Abstract:\n", test_abstract)
    print("\n⏳ 正在请求 Gemini API 总结...")
    summary = summarize_abstract(test_abstract)
    print("\n✅ 生成总结结果:\n", summary)
    print("================================")
