import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from my_utils import get_response

st.title("cysxun的智聊机器人")

# 实例：消息自动存 st.session_state["langchain_messages"]
history = StreamlitChatMessageHistory(key="chat_messages")

# 首次打开页面，没有消息，插入欢迎语
if len(history.messages) == 0:
    history.add_ai_message("你好，我是cysxun，有什么可以帮助你的么？")

# 渲染全部历史
for msg in history.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# 用户输入
prompt = st.chat_input("请输入您要咨询的问题：")
if prompt:
    history.add_user_message(prompt)
    st.chat_message("user").markdown(prompt)

    with st.spinner("AI小助手正在思考中..."):
        # history.messages 是 langchain结构化消息对象，转成ollama标准dict格式
        content = get_response(history.messages)

    history.add_ai_message(content)
    st.chat_message("assistant").markdown(content)
