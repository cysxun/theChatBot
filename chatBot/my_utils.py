import configparser
import os
import ollama
from langchain_core.messages import HumanMessage, AIMessage

# 读取 Ollama 配置：优先 config.ini（本机实际配置，不入库），缺失则回退 config.example.ini（模板）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg_path = os.path.join(BASE_DIR, "config.ini")
if not os.path.exists(cfg_path):
    cfg_path = os.path.join(BASE_DIR, "config.example.ini")

config = configparser.ConfigParser()
config.read(cfg_path, encoding="utf-8")
host = config.get("ollama", "host", fallback="127.0.0.1")
port = config.get("ollama", "port", fallback="11434")

client = ollama.Client(host=f"http://{host}:{port}")

def get_response(lc_messages):
    # langchain消息对象 → ollama要求的dict数组
    ollama_msgs = []
    for m in lc_messages[-50:]:
        if isinstance(m, HumanMessage):
            ollama_msgs.append({"role":"user", "content":m.content})
        elif isinstance(m, AIMessage):
            ollama_msgs.append({"role":"assistant", "content":m.content})

    resp = client.chat(
        model="qwen2:1.5b",
        messages=ollama_msgs
    )
    return resp["message"]["content"]
