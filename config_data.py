import os
#向量知识库配置
# 必须在这里配置你的 Google API Key，否则网页运行时会直接崩溃
os.environ["GOOGLE_API_KEY"] = "AIzaSyCDdxngJ1vUHypfyOdC2qajIrUM-qHRh2g"
#向量知识库路径
persist_directory = "D:/VscodeProjects/ai_project01/RAG与Agent开发入门/RAG项目案例-电商客服ai/chroma_db"
#向量知识库模型名称
embedding_model = "models/gemini-embedding-001"
llm_model="qwen3.5-plus"

#历史对话存储
storage_path = "D:/VscodeProjects/ai_project01/RAG与Agent开发入门/RAG项目案例-电商客服ai/chatMessageHistory"