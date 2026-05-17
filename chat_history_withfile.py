from langchain_core.chat_history import BaseChatMessageHistory
import os,json
from langchain_core.messages import message_to_dict,messages_from_dict

class FileChatHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id # 每个会话对应一个唯一的session_id
        self.storage_path = storage_path # 存储消息的文件夹路径
        self.file_path = os.path.join(self.storage_path,self.session_id+".json") # 每个会话的消息存储在一个以session_id命名的JSON文件中
        os.makedirs(self.storage_path,exist_ok=True) # 确保存储路径存在
        if not os.path.exists(self.file_path): #文件不存在时，创建聊天记录文件
            with open(self.file_path,"w",encoding="utf-8") as f:
                json.dump([],f,ensure_ascii=False)

    def add_messages(self,new_messages):
        existed_messages = list(self.messages)
        existed_messages.extend(new_messages)
        all_messages = [message_to_dict(message) for message in existed_messages]
        with open(self.file_path,"w",encoding="utf-8") as f: 
            json.dump(all_messages,f,ensure_ascii=False)
    
    @property
    def messages(self):
        # 检查文件是否存在且大小大于 0
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError:
                    # 如果文件损坏或格式不对，返回空列表
                    messages = []
        else:
            # 如果文件不存在或为空，返回空列表
            messages = []
        return messages_from_dict(messages)

    def clear(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False)