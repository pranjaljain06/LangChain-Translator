from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import os
from langserve import add_routes # helps to create apis
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langdetect import detect
from gtts import gTTS
import io

load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="openai/gpt-oss-120b",groq_api_key=groq_api_key)

#1. Craete prompt templates
system_template = "Translate the following text into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser = StrOutputParser()

chain=prompt_template|model|parser

app=FastAPI(title="Langchain Server",
            version = "1.0",
            description="A simple API server using Langchain runnable interfaces"
            )

add_routes(
    app,
    chain,
    path="/chain"
)

# Streamlit UI
st.title("LangChain Translation Demo (Groq)")
#language = st.text_input("Enter target language (e.g., Telugu, Hindi, French)")
language = st.selectbox(
    "Select target language",
    ["Telugu", "Hindi", "French", "Tamil", "English", "Spanish", "German", "Japanese"]
)
text = st.text_area("Enter text to translate")
if text:
    source_lang = detect(text)
    st.write(f"Detected source language: {source_lang}")
if "history" not in st.session_state:
    st.session_state["history"] = []

# File uploader
uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf", "word"])

if st.button("Translate"):
    if language and (text or uploaded_file):
        content = ""

        # Handle text input
        if text:
            content = text

        # Handle file upload
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                content = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"

        # Run translation chain
        response = chain.invoke({"language": language, "text": content})
        st.success("Translated Text:")
        st.write(response)

        st.code(response)  # show nicely formatted text
        st.button("Copy to Clipboard", on_click=st.write, args=(response,))

        lang_map = {
            "English": "en",
            "French": "fr",
            "Hindi": "hi",
            "Telugu": "te",
            "Tamil": "ta",
            "Spanish": "es",
            "German": "de",
            "Japanese": "ja"
        }

        tts = gTTS(response, lang=lang_map[language])
        
        tts = gTTS(response, lang="en")  # or target language code
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)

        st.audio(audio_bytes.getvalue(), format="audio/mp3")
        
        # If user uploaded a file, use its name
        if uploaded_file is not None:
            original_name = uploaded_file.name
            # Split filename into (name, extension)
            base_name, _ = os.path.splitext(original_name)

            translated_name = f"Translated_{base_name}.txt"
            translated_audio = f"Translated_{base_name}.mp3"
        else:
            translated_name = "Translated_text.txt"
            translated_audio = "Translated_text.mp3"
        # Option to download translation
        st.download_button(
            label="Download Translated file",
            data=response,
            file_name=translated_name,
            mime="text/plain" #the mime argument tells the browser what type of file is being downloaded -> txt.
        )
        # Download audio file
        st.download_button(
            label="Download Audio File",
            data=audio_bytes.getvalue(),
            file_name=translated_audio,
            mime="audio/mp3"
        )
    else:
        st.error("Please enter text or upload a file, and select a language.")

# Show history
if st.session_state["history"]: #if list is not-empty
    st.subheader("Translation History")
    for item in st.session_state["history"]:
        st.write(f"{item['text']} → ({item['language']}) → {item['output']}")
        st.audio(item["audio"], format="audio/mp3")  # replay audio
        st.download_button(
            label=f"Download Audio ({item['language']})",
            data=item["audio"],
            file_name=f"Translated_{item['language']}.mp3",
            mime="audio/mp3"
        )

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 