import os
from langchain_chroma import Chroma
import config_data as config
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 知识库 
class knowledgeBase(object):
        
    def __init__(self, file_name:str, init_embedding:bool=False):
        self.file_name = file_name
        self.embedding_model_name = config.embedding_model
        
        # 只有在需要时（比如上传）才加载 Embedding 模型
        self.embedding_function = None
        if init_embedding:
            self.embedding_function = GoogleGenerativeAIEmbeddings(model=self.embedding_model_name)
            
        self.chroma = Chroma(
            collection_name="ecommerce_customer_service_kb",
            persist_directory=config.persist_directory,
            embedding_function=self.embedding_function,
        )
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 200,
            chunk_overlap = 20,
            separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
            length_function = len,
        )



    def upload_by_str(self, data, md5):
        knowledge_chunks = self.splitter.split_text(data)
        meta_data = {
            "source": self.file_name,
            "file_md5": md5,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operaor": "chensisi"
        }
        #
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[meta_data for _ in knowledge_chunks]
        )

    def check_md5(self, md5):
        # 检查是否存在该MD5的文件记录
        results = self.chroma.get(where={"file_md5": md5})
        if results and results['ids']:
            return True
        return False

    def get_all_filenames(self):
        # 获取数据库中所有的元数据
        results = self.chroma.get(include=['metadatas'])
        if results and results['metadatas']:
            # 提取所有唯一的 source 字段 (即文件名)
            filenames = set([m['source'] for m in results['metadatas'] if 'source' in m])
            return list(filenames)
        return []

    def delete_by_filename(self, filename):
        # 根据文件名删除对应的记录
        self.chroma.delete(where={"source": filename})
        return True

        
if __name__ == "__main__":
    pass
    # # print(os.getcwd())
    # kb = knowledgeBase(file_name = "文件名2")
    # # kb.upload_by_str(data = "明天会更好", md5="test_md5")


