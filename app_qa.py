#用户与大模型交互的APP界面  
import streamlit as st
from llm_chat import ChatService

st.title("智能电商客服问答")
st.divider()

# 初始化 session_state，用于存储对话历史
if "all_messages" not in st.session_state:
    st.session_state["all_messages"] = [{"role":"assistant","content":"您好,有什么可以帮您？"}]

# 遍历session_state中的消息列表
for message in st.session_state["all_messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 初始化chatService对象
@st.cache_resource
def get_chat_service():
    chat_service = ChatService()
    return chat_service

# 获取用户输入
prompt = st.chat_input("请输入您的问题吧。")

if prompt:
    st.chat_message("user").write(prompt)  # 页面写出用户的问题
    st.session_state["all_messages"].append({"role":"user","content":prompt}) #会话历史记录添加用户的问题
    
    # 获取chatService对象
    chat_service = get_chat_service()
    # 获取会话配置
    session_config = {"configurable": {"session_id": "user_02"}}
    
    # 将 AI 的回答流式写出在网页上
    with st.chat_message("assistant"):
        # 使用 stream 方法获取流式响应
        stream_resp = chat_service.withHistory_chain.stream({"user_question": prompt}, session_config)
        # 使用 st.write_stream 实时渲染并获取最终完整文本
        res = st.write_stream(stream_resp)
    
    # 会话历史记录添加 AI 的回答
    st.session_state["all_messages"].append({"role":"assistant","content":res})