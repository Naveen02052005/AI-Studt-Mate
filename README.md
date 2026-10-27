# 📚 AI Study Mate

**AI Study Mate** is an AI-powered study assistant that helps students understand, summarize, and revise their study materials. Students can upload PDF documents, ask questions based on their documents, generate summaries, and practice with AI-generated quizzes.

The project uses Generative AI and Retrieval-Augmented Generation (RAG) to provide answers grounded in uploaded study materials.

## ✨ Features

- **📄 PDF Document Management:** Upload and manage multiple study PDFs.
- **💬 Ask AI:** Ask questions about uploaded documents and receive context-based answers.
- **🔎 Hybrid Retrieval:** Combines semantic search and keyword-based retrieval to find relevant information.
- **📌 Source References:** View source documents and page references supporting answers.
- **📝 Smart Summarization:** Generate study summaries and key points from selected documents.
- **🧠 Practice Quiz:** Generate multiple-choice questions with four options, correct answers, and explanations.
- **🔤 OCR Support:** Extract text from scanned PDF pages when required.
- **💬 Chat History:** Keep track of conversations with the study assistant.
- **👍 User Feedback:** Provide feedback on AI-generated answers.
- **🛡️ Error Handling:** Handle missing documents, invalid uploads, and other expected input errors.
- **📊 AI Monitoring:** Use LangSmith tracing to inspect and monitor supported LLM operations.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Frontend:** Streamlit
- **LLM / Generative AI:** Google Gemini
- **AI Framework:** LangChain
- **Retrieval-Augmented Generation:** RAG
- **Vector Database:** Chroma
- **Embeddings:** Hugging Face Sentence Transformers
- **Keyword Retrieval:** BM25
- **PDF Processing:** PyPDF and LangChain document loaders
- **OCR:** Tesseract OCR and `pytesseract`
- **PDF Image Conversion:** `pdf2image`
- **AI Tracing and Monitoring:** LangSmith
- **Environment Configuration:** Python dotenv

## 🏗️ Project Architecture

The application follows the **Model-View-Controller (MVC)** architecture to organize its code into separate responsibilities.

```text
AI-Study-Mate/
│
├── app.py
├── controllers/
│   ├── chat_controller.py
│   └── quiz_controller.py
│
├── models/
│
├── services/
│   ├── chat_service.py
│   ├── document_service.py
│   ├── llm_service.py
│   ├── prompts.py
│   ├── quiz_service.py
│   └── summary_service.py
│
├── views/
│   ├── chat_view.py
│   ├── documents_view.py
│   ├── home_view.py
│   ├── quiz_view.py
│   └── summary_view.py
│
├── src/
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
```

- **Views:** Display the user interface and collect user input.
- **Controllers:** Coordinate application workflows and user actions.
- **Services:** Handle document processing, retrieval, LLM interactions, summarization, and quiz generation.
- **Models:** Provide a dedicated place for model-related components as the project evolves.
- **App entry point:** `app.py` launches the Streamlit application.

## ⚙️ Installation and Setup

### Prerequisites

- Python version compatible with the project configuration
- Git
- A Google Gemini API key
- Tesseract OCR and Poppler if using the OCR functionality on scanned PDFs

### 1. Clone the repository

```bash
git clone https://github.com/Naveen02052005/AI-Studt-Mate.git
cd AI-Studt-Mate
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory and add your Gemini API key using the environment variable name expected by the project.

For example, if the application uses `GOOGLE_API_KEY`:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

If LangSmith tracing is enabled in your configuration, add the relevant LangSmith settings as required by your code.

**Important:** Replace the example value with your own API key. Never commit `.env` or expose API keys in source code or public repositories.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser to use AI Study Mate.

## 🚀 How to Use

1. Launch the application.
2. Open **My Documents** and upload your study PDFs.
3. Open **Ask AI** to ask questions about the uploaded materials.
4. Review answers and their supporting source references.
5. Open the summary section to generate summaries and key points.
6. Open **Practice Quiz**, select a document and the number of questions, and test your understanding.
7. Review the correct answers and explanations.
8. Provide feedback on AI-generated responses when needed.

## 🛡️ Responsible AI and Security

- Answers are designed to use retrieved content from uploaded documents.
- Source references help users verify information against the original PDFs.
- AI-generated answers and quiz questions should be checked against the source material.
- API keys and credentials must be stored in environment variables, not committed to Git.
- Uploaded documents should be treated as private study materials.

## 🎯 Project Objective

The objective of AI Study Mate is to make studying more interactive and efficient by combining document understanding, Generative AI, information retrieval, and personalized practice in one application.

## 👨‍💻 Author

**Naveen Merugu**

GitHub: [Naveen02052005](https://github.com/Naveen02052005)

## 📄 License

No license has been added yet. All rights are reserved unless a license is added to this repository.
