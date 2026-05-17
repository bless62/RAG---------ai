# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

这是一个基于 LangChain 和 Streamlit 的电商客服问答系统，实现了 RAG（检索增强生成）架构。系统通过向量数据库存储产品知识，使用大语言模型回答用户问题，并支持会话历史持久化。

## 运行方式

### 启动 Streamlit 应用

```bash
streamlit run app_qa.py          # 主问答界面
streamlit run app_file_uploader.py  # 知识库管理界面
```

### 环境变量要求

- `DASHSCOPE_API_KEY`: 阿里云通义千问 API Key（用于 LLM）
- 代码中已配置：`GOOGLE_API_KEY`（用于 Embedding 模型）

## 核心代码架构

### 主要模块

| 文件 | 说明 |
|------|------|
| [`app_qa.py`](app_qa.py) | Streamlit 主界面：用户问答交互入口 |
| [`llm_chat.py`](llm_chat.py) | ChatService 类：核心对话服务，包含链式调用和会话管理 |
| [`vector_retriever.py`](vector_retriever.py) | vectorRetriever 类：向量检索器初始化 |
| [`knowledge_base.py`](knowledge_base.py) | knowledgeBase 类：知识库上传/删除操作 |
| [`chat_history_withfile.py`](chat_history_withfile.py) | FileChatHistory 类：基于 JSON 的文件式会话历史存储 |
| [`config_data.py`](config_data.py) | 全局配置：数据库路径、模型名称等 |

### 数据流图

```
用户提问 → app_qa.py → ChatService.withHistory_chain
                          ├─→ vectorRetriever (RAG 检索)
                          ├─→ FileChatHistory (会话历史)
                          └─→ Qwen LLM → 返回答案
```

### 关键技术栈

- **LLM**: 阿里云通义千问 (`qwen3.5-plus`) via DashScope API
- **Embedding**: Google Gemini Embedding (`models/gemini-embedding-001`)
- **Vector DB**: ChromaDB (持久化目录：`chroma_db`)
- **Framework**: LangChain + Streamlit
- **Session Storage**: 每个会话对应一个 JSON 文件 (`chatMessageHistory/`)

## 关键函数和类

- [`ChatService.__init__`](llm_chat.py:14) - 初始化 LLM、检索器和提示词模板
- [`ChatService.normal_chain`](llm_chat.py:38) - 不带记忆的链式调用
- [`ChatService.withHistory_chain`](llm_chat.py:44) - 带记忆的消息历史链
- [`FileChatHistory`](chat_history_withfile.py:4) - 自定义 BaseChatMessageHistory 实现
- [`knowledgeBase.upload_by_str`](knowledge_base.py:32) - 文本上传并分块向量化

## 配置项 (config_data.py)

- `persist_directory`: Chroma 数据库持久化路径
- `embedding_model`: Embedding 模型名称
- `llm_model`: LLM 模型名称
- `storage_path`: 会话历史 JSON 文件存储路径
