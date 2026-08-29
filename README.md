# cysxun 智聊机器人

基于 Streamlit + LangChain + Ollama 的 Web 聊天机器人，调用本地大模型 `qwen2:1.5b` 实现多轮对话。

## 功能

- Streamlit 网页聊天界面，自动保存对话历史
- 调用 Ollama 本地模型 `qwen2:1.5b` 生成回复
- 通过 LangChain 管理消息历史（保留最近 50 轮上下文）

## 技术栈与版本

| 组件 | 版本 |
|---|---|
| Python | 3.12.13（开发环境：conda 环境 `01python`） |
| streamlit | 1.62.0 |
| langchain-core | 1.6.1 |
| langchain-community | 0.4.2 |
| ollama | 0.6.2 |

依赖以 `requirements.txt` 为准（仅含代码实际用到的包，不含 anaconda 全量环境）。

## 项目结构

```
theChatBot/
├── chatBot/
│   ├── my_chat.py          # Streamlit 主界面（入口）
│   └── my_utils.py         # 读取配置并调用 Ollama 的核心逻辑
├── test/                   # 开发测试脚本（不入库）
├── config.example.ini      # 配置模板（入库，供各机器复制）
├── config.ini              # 本机实际配置（不入库）
├── requirements.txt        # Python 依赖清单
├── .gitignore
└── README.md
```

## 配置说明

Ollama 服务地址通过配置文件管理，不再硬编码在代码中：

```ini
[ollama]
host = 127.0.0.1   # Ollama 服务地址（不带 http://）
port = 11434       # Ollama 服务端口
```

- **config.example.ini**：模板，随仓库发布，默认 `127.0.0.1:11434`
- **config.ini**：本机/服务器实际配置，已被 `.gitignore` 排除，不入库
- 代码优先读取 `config.ini`，缺失时回退到 `config.example.ini`，再兜底默认值

首次使用：`cp config.example.ini config.ini`，再按需修改 `host` / `port`。

## 本地运行（conda）

从新建 conda 环境开始，全流程可复现：

```bash
# 1. 新建 conda 环境（Python 3.12，与开发环境一致）
conda create -n theChatBot python=3.12 -y
conda activate theChatBot

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 Ollama 服务地址（首次使用）
copy config.example.ini config.ini
# 按需编辑 config.ini 中的 host / port

# 4. 启动
streamlit run chatBot/my_chat.py
```

> 若已有现成环境（如开发用 `01python`），可直接 `conda activate 01python`，从第 2 步开始。

浏览器访问 http://localhost:8501

## 服务器部署（Linux）

前置要求：Python 3.11+、Git、可访问的 Ollama 服务（`qwen2:1.5b`）。

```bash
# 1. 拉取代码
git clone <你的仓库地址> theChatBot
cd theChatBot

# 2. 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 配置 Ollama 地址（指向服务器可通的 Ollama 服务）
cp config.example.ini config.ini
# 编辑 config.ini：若服务器本机装了 Ollama 保持 127.0.0.1:11434 即可

# 4. 启动（监听所有网卡，供外部访问）
streamlit run chatBot/my_chat.py --server.address 0.0.0.0 --server.port 8501
```

浏览器访问 `http://服务器IP:8501`。

> 服务器(Linux)若无 Ollama：`curl -fsSL https://ollama.com/install.sh | sh` 安装后 `ollama pull qwen2:1.5b`。

## Windows 部署 Ollama（本地开发）

```bash
# 1. 下载安装
#    前往 https://ollama.com/download/windows 下载 OllamaSetup.exe 并运行
#    安装完成后 Ollama 自动作为后台服务运行（任务栏托盘有图标）

# 2. 拉取模型（PowerShell / CMD 均可）
ollama pull qwen2:1.5b

# 3. 验证服务是否正常（默认监听 127.0.0.1:11434）
ollama list
```

- 本机运行 `config.ini` 保持默认 `host = 127.0.0.1`、`port = 11434` 即可直接使用
- 若需其他机器访问本机 Ollama：先设置环境变量 `OLLAMA_HOST=0.0.0.0`（`setx OLLAMA_HOST 0.0.0.0`），再重启 Ollama（托盘右键退出后重新打开）
- 校验服务：浏览器访问 `http://127.0.0.1:11434`，看到 `Ollama is running` 即正常

## 外部依赖

- Python 3.11+（推荐 3.12.x，与开发环境一致）
- Ollama（服务端，模型：qwen2:1.5b）


