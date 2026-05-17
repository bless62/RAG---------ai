from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
import config_data as config
import os
from operator import itemgetter
from vector_retriever import vectorRetriever
from langchain_core.output_parsers import StrOutputParser
from chat_history_withfile import FileChatHistory
from langchain_core.documents import Document
from langchain_core.runnables import RunnableWithMessageHistory,RunnableLambda

#创建全局变量：用户会话历史存储字典
users_chat_store ={}

class ChatService(object):
    def __init__(self):
        self.model = ChatOpenAI(
            model = config.llm_model,
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            extra_body={"enable_thinking": False}
        )
        #创建检索器实例，链式调用时使用的组件
        self.retriever = vectorRetriever().retriever
        #提示词模板生成
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system","你是一个电商客服，回答用户的问题，需要严格参考资料{retrieved_docs}"),
            MessagesPlaceholder("chat_history"),
            ("human","{user_question}")
        ])
        #retriever：输入->"查询语句的字符串"，
        # 输出->List[Document] (检索出来的最相关的文档片段)

        #prompt_template:输入->字典
        #输出->List[BaseMessage] (消息对象列表).模型能够直接理解的格式。它将你定义的角色（system, human）和变量填充后的内容组合成了一串标准的消息流。

        #普通链式调用：不带记忆功能
        self.normal_chain = ({"user_question": itemgetter("user_question") | RunnableLambda(self.show_input),"retrieved_docs" : itemgetter("user_question") | self.retriever | self.doc_format_str, "chat_history": itemgetter("chat_history")}
        | RunnableLambda(self.show_input) | self.prompt_template | self.model | StrOutputParser())

        #带记忆的链式调用
        self.withHistory_chain = RunnableWithMessageHistory(
                self.normal_chain,
                self.get_chatHistory,#记忆存储
                input_messages_key="user_question",
                history_messages_key="chat_history"
        )

    #定义一个函数用于打印完整的提示词信息，方便调试和查看生成的提示内容
    def print_prompt(self,full_prompt):
        print("="*20,full_prompt,"="*20)
        return full_prompt

    #实现会话管理：返回或创建会话历史
    def get_chatHistory(self,session_id):
        if session_id not in users_chat_store:
            users_chat_store[session_id] = FileChatHistory(session_id,config.storage_path)
        return users_chat_store[session_id]

    #把检索出来的Document格式化为字符串，便于模型理解
    def doc_format_str(self,docs:list[Document]):
        str = '['
        for doc in docs:
            str += doc.page_content
            str += ']'
        return str

    #用于打印链式调用过程中，某个节点的中间输出，用于调试
    def show_input(self,value):
        print('=='*20)
        print(value)
        return value

if __name__ == "__main__":
    chat_service = ChatService()
    session_config = {"configurable": {"session_id": "user_01"}}
    res1 =chat_service.withHistory_chain.invoke({"user_question": "我妈妈前天买了8个桃子"},session_config)
    print(res1)

    res2 = chat_service.withHistory_chain.invoke({"user_question": "我刚刚买了29个芒果"},session_config)
    print(res2)

    res3 = chat_service.withHistory_chain.invoke({"user_question": "我家一共买了多少种水果？有我妈妈喜欢吃的水果吗？"},session_config)
    print(res3)
