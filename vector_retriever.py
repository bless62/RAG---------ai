from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import config_data as config

class vectorRetriever(object):
    def __init__(self,retriever_top_k=1):
        self.chroma = Chroma(
            collection_name="ecommerce_customer_service_kb",
            persist_directory=config.persist_directory,
            embedding_function=GoogleGenerativeAIEmbeddings(model=config.embedding_model)
        )
        self.retriever = self.chroma.as_retriever(search_kwargs={"k": retriever_top_k})