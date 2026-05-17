print("程序开始运行...")
import streamlit as st
import time
print("Streamlit 导入成功...")

#添加网页标题
st.title("知识库更新服务")

# 使用 session_state 来控制上传控件的重置
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

#添加上传文件框
uploader_file = st.file_uploader(
    label="请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,
    key=f"uploader_{st.session_state['uploader_key']}" # 动态 Key
)

from knowledge_base import knowledgeBase
import hashlib

# 使用缓存来存储轻量级的知识库对象（不加载模型），用于快速展示文件名
@st.cache_resource
def get_kb_manager():
    return knowledgeBase(file_name="manager", init_embedding=False)

# --- 侧边栏：管理已上传文件 ---
st.sidebar.header("知识库管理")

# 快速获取已存在的文件名
kb_manager = get_kb_manager()
existing_files = kb_manager.get_all_filenames()

if existing_files:
    st.sidebar.write("已上传的文件：")
    for f in existing_files:
        st.sidebar.text(f"📄 {f}")
    
    # 删除功能
    st.sidebar.divider()
    delete_file_name = st.sidebar.selectbox("选择要删除的文件", ["-- 请选择 --"] + existing_files)
    if st.sidebar.button("确认删除", type="primary"):
        if delete_file_name != "-- 请选择 --":
            kb_manager.delete_by_filename(delete_file_name)
            st.sidebar.success(f"文件 '{delete_file_name}' 已从知识库删除！")
            st.rerun() 
else:
    st.sidebar.info("知识库目前为空")

# --- 主界面：上传功能 ---
# 上传文件
if uploader_file is not None:
    # #提取文件的信息
    file_name = uploader_file.name
    # #获取文件内容 (二进制用于计算MD5)
    file_bytes = uploader_file.getvalue()
    # 计算MD5
    md5_hash = hashlib.md5(file_bytes).hexdigest()
    
    # 检查MD5是否存在
    if kb_manager.check_md5(md5_hash):
        st.warning(f"文件 '{file_name}' (MD5: {md5_hash}) 已存在于知识库中，请勿重复上传！")
    else:
        # 只有在真正需要上传时，才显示加载动画并初始化带模型的对象
        with st.status("正在处理文件并上传至向量数据库...", state="running", expanded=True) as status:
            # 转换为字符串用于上传
            txt_value = file_bytes.decode('utf-8')
            # 创建一个带模型初始化功能的知识库对象进行上传
            kb_upload = knowledgeBase(file_name=file_name, init_embedding=True)
            kb_upload.upload_by_str(data=txt_value, md5=md5_hash)
            status.update(label="上传成功！", state="complete", expanded=False)
            
        # 上传成功后，修改 key 以重置上传控件
        st.session_state["uploader_key"] += 1
        st.success(f"知识库已更新！文件 '{file_name}' 上传成功。")
        time.sleep(1)
        st.rerun() 


