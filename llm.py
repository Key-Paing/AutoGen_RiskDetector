from langchain_google_vertexai import VertexAI
from google.oauth2.service_account import Credentials
from google.auth import default
import json
import streamlit as st


try:
    raw = st.secrets["google"]["credentials"]
    key_path = json.loads(raw)

    credentials = Credentials.from_service_account_info(
        key_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    llm = VertexAI(
        project='machine-translation-001',
        location='us-central1',
        model = "gemini-2.5-pro-preview-05-06",
        credentials=credentials
    )
except Exception as e:
    st.error("LLM setup failed")
    st.text(repr(e))