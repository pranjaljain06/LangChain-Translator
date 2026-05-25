# LangChain Translator Demo

A language translation application built with **FastAPI**, **Streamlit**, and **LangChain** using **Groq** models.  
It supports text input, file uploads (.txt, .pdf), automatic language detection, and speech output via Google Text-to-Speech.

---

## 🚀 Features
- Translate text into multiple languages (Telugu, Hindi, French, Tamil, English, Spanish, German, Japanese).
- Detect source language automatically.
- Upload `.txt` or `.pdf` files for translation.
- Generate audio output of translated text.
- Download translated text and audio files.
- API endpoints powered by FastAPI + LangServe.

---

## 📦 Installation

1. **Clone the repository**
   git clone https://github.com/pranjaljain06/LangChain-Translator.git
   cd LangChain-Translator
   
2. **Create a virtual environment**
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # macOS/Linux
   
3. **Install dependencies**
   pip install -r requirements.txt
   
4. **Environment Variables**
   Create a **.env** file in the project root with your API keys:
   GROQ_API_KEY=your_groq_key_here
   OPENAI_API_KEY=your_openai_key_here
   LANGCHAIN_API_KEY=your_langsmith_key_here
   LANGCHAIN_PROJECT=LangChain-Translator
   
5. **Running the App**
   FastAPI server
      uvicorn serve:app --reload
       - Runs the API server at http://localhost:8000.

   Streamlit UI
      streamlit run serve.py
       - Opens the interactive translation demo in your browser.

---

## **Tech Stack**

1. FastAPI – backend API
2. Streamlit – frontend UI
3. LangChain – prompt chaining
4. Groq – LLM provider
5. PyPDF2 – PDF parsing
6. langdetect – language detection
7. gTTS – text-to-speech
