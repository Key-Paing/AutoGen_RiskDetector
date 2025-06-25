from langchain_google_vertexai import VertexAI
from google.oauth2.service_account import Credentials
import json
import streamlit as st


# key_path = 'botexpert-459607-26d1eb471087.json'

raw = st.secrets["google"]["credentials"]
service_account_info = json.loads(raw)
credentials = Credentials.from_service_account_info(service_account_info, scopes=['https://www.googleapis.com/auth/cloud-platform'])


# Create credentials
# credentials = Credentials.from_service_account_file(
#     key_path,
#     scopes=['https://www.googleapis.com/auth/cloud-platform']
# )


llm = VertexAI(
    project='machine-translation-001',
    location='us-central1',
    credentials=credentials,
    model = "gemini-2.5-pro-preview-05-06"
)