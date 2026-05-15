# import streamlit as st
# import PyPDF2
# from api_client import APIClient

# st.set_page_config(page_title="Document Q&A Engine", layout="wide")

# api_client = APIClient()

# # Initialize from DB on load
# if "messages" not in st.session_state:
#     st.session_state.messages = api_client.get_history()
# if "document_text" not in st.session_state:
#     st.session_state.document_text = ""
# if "summary" not in st.session_state:
#     st.session_state.summary = ""

# with st.sidebar:
#     st.header("⚙️ Configuration")
#     if st.button("🗑️ Clear Document", use_container_width=True):
#         st.session_state.document_text = ""
#         st.session_state.summary = ""
#         st.success("Document cleared!")
        
#     if st.button("🚨 Deep Clean (Wipe Database & Vectors)", use_container_width=True):
#         with st.spinner("Purging databases..."):
#             api_client.clear_all()
#             st.session_state.messages = []
#             st.session_state.document_text = ""
#             st.session_state.summary = ""
#             st.success("System completely reset!")

# st.title("📄 Document Q&A & Summarization Engine")
# col1, col2 = st.columns(2)

# with col1:
#     st.header("📤 Upload Document")
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
#     if uploaded_file is not None:
#         try:
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             extracted_text = ""
#             for page in pdf_reader.pages:
#                 extracted_text += page.extract_text() + "\n"
#             st.session_state.document_text = extracted_text
#             st.success(f"✅ Loaded: {uploaded_file.name}")
#         except Exception as e:
#             st.error(f"Error loading document: {str(e)}")

# with col2:
#     st.header("✨ Generate Summary")
#     if st.session_state.document_text:
#         if st.button("📝 Generate Summary", use_container_width=True):
#             with st.spinner("Generating summary..."):
#                 try:
#                     st.session_state.summary = api_client.summarize(st.session_state.document_text)
#                     st.info(st.session_state.summary)
#                 except Exception as e:
#                     st.error(f"Error generating summary: {str(e)}")

# st.header("💬 Ask Questions")
# if st.session_state.document_text:
#     # Display historical messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])
            
#     # Input for new question
#     if prompt := st.chat_input("Ask a question about the document..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)
            
#         with st.spinner("Finding answer..."):
#             try:
#                 answer = api_client.ask_question(st.session_state.document_text, prompt)
#                 st.session_state.messages.append({"role": "assistant", "content": answer})
#                 with st.chat_message("assistant"):
#                     st.write(answer)
#             except Exception as e:
#                 st.error(f"Error getting answer: {str(e)}")
# else:
#     st.info("📌 Upload a document first to start asking questions")

import streamlit as st
import PyPDF2
from api_client import APIClient

# 1. Page Config
st.set_page_config(
    page_title="Document Q&A Engine",
    page_icon="📄",
    layout="wide"
)

# 2. Cache the API Client so it doesn't re-initialize on every rerun
@st.cache_resource
def get_api_client():
    return APIClient()

api_client = get_api_client()

# 3. Initialize Session State
if "messages" not in st.session_state:
    try:
        # Fetch existing history from the backend on first load
        st.session_state.messages = api_client.get_history()
    except Exception:
        st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if st.button("🗑️ Clear Local UI", use_container_width=True):
        st.session_state.document_text = ""
        st.session_state.summary = ""
        st.success("UI cleared! (Backend data remains)")
        st.rerun() # Refresh the page to reflect changes
        
    st.divider()
    
    if st.button("🚨 Deep Clean (Wipe All)", use_container_width=True, type="primary"):
        with st.spinner("Purging databases..."):
            try:
                api_client.clear_all()
                st.session_state.messages = []
                st.session_state.document_text = ""
                st.session_state.summary = ""
                st.success("System completely reset!")
                st.rerun()
            except Exception as e:
                st.error(f"Reset failed: {e}")

# --- Main UI ---
st.title("📄 Document Q&A & Summarization Engine")

col1, col2 = st.columns(2)

with col1:
    st.header("📤 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        try:
            # We only extract text if it's different from what we already have
            # to save processing time on reruns
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            extracted_text = ""
            for page in pdf_reader.pages:
                extracted_text += page.extract_text() + "\n"
            
            st.session_state.document_text = extracted_text
            st.success(f"✅ Loaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error loading document: {str(e)}")

with col2:
    st.header("✨ Generate Summary")
    if st.session_state.document_text:
        if st.button("📝 Generate Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                try:
                    # Logic is moved to API Client
                    summary = api_client.summarize(st.session_state.document_text)
                    st.session_state.summary = summary
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")
        
        if st.session_state.summary:
            st.info(st.session_state.summary)
    else:
        st.write("Upload a document to enable summarization.")

st.divider()

# --- Chat Interface ---
st.header("💬 Ask Questions")

if st.session_state.document_text:
    # Display chat history using Streamlit's native chat elements
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Input for new question
    if prompt := st.chat_input("Ask a question about the document..."):
        # Add user message to UI immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Get AI Answer
        with st.chat_message("assistant"):
            with st.spinner("Finding answer..."):
                try:
                    answer = api_client.ask_question(st.session_state.document_text, prompt)
                    st.write(answer)
                    # Add assistant message to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error getting answer: {str(e)}")
else:
    st.info("📌 Upload a document first to start asking questions")