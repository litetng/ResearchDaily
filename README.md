# 📚 MyResearchDaily

**MyResearchDaily** 是一个极其轻量级且无感知的个人科研前沿论文跟踪、管理与 AI 智能辅读本地工具。

厌倦了一言不合就疯狂下载几十个冗长沉重的学术 PDF？这个应用致力于以“每天一点点”的形式，采用最轻量的文本抓取和纯本地储存手段，为您持续沉淀属于专属领域的重点核心干货。

---

## ✨ 核心特性

- **🚀 ArXiv 高级语法自动查新**
  支持强大的布尔逻辑词汇查新规则（如 `cat:cs.CV`, `ti:"deep learning" AND all:medical`）。同时内建智能排队保护机制（严格遵守官方规则，每次查询固定间歇休眠 3 秒），杜绝封 IP 或响应挂死（Time out）。
- **🤖 LLM 前沿速览 (Gemini)**
  看摘要太长？直接点击每个卡片里的“AI 总结核心创新点”，本地后台直接调起 `gemini` 极速大模型，将原本佶屈聱牙的洋文，转化为 150 字以内精准、犀利的大白话版“中文核心贡献”。
- **🗄️ SQLite 零依赖轻量本地管理**
  抛弃繁杂的远程服务部署或文档下载流，将文章、您的手写批注、是否已读的状态，只用一个几 KB 的 `my_research_daily.db` 一手打点。
- **💻 极致的 Windows“原生级”后台体验**
  通过 `run.vbs` 与 `start.bat` 并联设计，实现了双击一键完全隐藏黑框启动服务器，并自动调起浏览器，呈现纯净无打扰界面。

---

## 📂 项目结构

```text
/ (Project Root)
├── app.py                   # Streamlit 主交互层 (Tab 分区、卡片渲染、用户组件交互)
├── fetcher.py               # 网络引擎 (利用 urllib 和 xml 解析提取 ArXiv API 数据源)
├── database.py              # 数据中枢 (负责 SQLite3 的初始化和 CRUD 数据持久化)
├── summarizer.py            # AI 中介 (调用 google-generativeai 实现 150字 提炼)
├── run.vbs                  # Windows 一键静默启动快捷脚本入口
├── start.bat                # 实际承接 Anaconda 环境激活与服务调起的暗堡脚本
├── .env                     # 存放 GEMINI_API_KEY (必须)
└── my_research_daily.db     # 系统自动创建生成的单文件微型数据库
```

---

## 🛠️ 安装与配置指南

### 1. 环境依赖

在使用之前，请确保当前环境已配置 Python。如果有使用 Anaconda 等虚拟环境，需要在里面安装必备依赖包（或者在文件根目录执行命令）：

```bash
pip install streamlit python-dotenv google-generativeai
```

除了上面三个由该 App 发动的外部库以外，其余用到的包例如 `urllib`, `xml.etree`, `sqlite3` 等**皆为 Python 纯内置标准库**。

### 2. 配置环境密钥 `.env`

这是让 AI 为你解读文献“核心创新点”的钥匙。
请在根目录下新建一个 `.env` 文件，内容填写如下：

```dotenv
GEMINI_API_KEY="你的 Gemini API Key"
```

---

## 🚀 日常运行与食用指南

### 方案 A：代码狂人的传统模式
在终端环境激活下直接回车执行：
```bash
streamlit run app.py
```

### 方案 B：独立客户端的纯净摸鱼模式 (推荐)
1. 确保修改并在 `start.bat` 中填写好了对应正确的 Anaconda / 对应的环境启动路径。
2. 双击项目根目录下的 **`run.vbs`** 文件。
3. （如果你尚未设置过）：建议打开 Edge/Chrome 浏览器访问 `http://localhost:8501`，点击浏览器右上角的快捷菜单选择 **“应用 ➔ 将此站点作为应用安装”**。从此，这就是你的一个独立的跨窗无打扰程序！

---

## 📝 开发与扩展维护说明

该应用采取完全模块内聚的方式编写，无状态混用。
- 如果你需要**调整爬虫单次下载上线数量**：它已直接暴露在 Streamlit 界面的左侧边栏 Slider 组件中控制。
- 如果你需要**接入 OpenAI 其他模型或者国产模型**：直接去 `summarizer.py` 里微调基座调用，由于隔离得好，任何 AI 模型的切换都不会伤及到系统的主从逻辑。

💡 *开始你的极简学术之旅吧！*
