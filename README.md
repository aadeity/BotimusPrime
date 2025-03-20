# BotimusPrime
<div align="center">
  
  <h1>📄Interactive Document Chatbot</h1>
  <p>
    <strong>Chat with your documents using open-source LLMs</strong>
  </p>
  <p>
    <a href="#demo">View Demo</a>
    ·
    <a href="#features">Features</a>
    ·
    <a href="#installation">Installation</a>
    ·
    <a href="#usage">Usage</a>
  </p>
  
  ![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
  ![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
  ![LangChain](https://img.shields.io/badge/langchain-0.1.0+-orange.svg)
  ![License](https://img.shields.io/badge/license-MIT-blue)
</div>

## 🌟 Overview

Document Chatbot is an intelligent application that allows you to upload documents (PDF, DOCX, XLSX, CSV) and ask questions about their content. The application uses open-source LLMs through Ollama to provide accurate, context-aware responses based on the document's content.

<div id="demo"></div>

## ✨ Demo

![WhatsApp Image 2025-03-20 at 21 30 43_14bb25b3](https://github.com/user-attachments/assets/278b6976-f2d1-4bdb-9ab0-cba2a18c7278)
![WhatsApp Image 2025-03-20 at 21 31 01_4ec0d314](https://github.com/user-attachments/assets/d509509d-eb41-4bb4-a3a2-43d4a35e1c0f)


<div id="features"></div>

## 🚀 Features

- **Document Upload**: Support for PDF, Word, Excel, and CSV files
- **Multiple LLM Support**: Choose from various Ollama models (Gemma, Llama3, Mistral)
- **Interactive Chat Interface**: User-friendly conversation UI
- **Semantic Search**: Finds relevant information even when exact keywords aren't used
- **Local Processing**: All data stays on your machine for privacy
- **Responsive Design**: Works on desktop and mobile devices

<div id="installation"></div>

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- At least one LLM model pulled in Ollama (e.g., `ollama pull gemma:2b`)

## 🔧 Installation

1. **Clone the repository**


2. **Create a virtual environment**


3. **Install dependencies**


4. **Create necessary directories**


<div id="usage"></div>

## 🖥️ Usage

1. **Start the application**


2. **Access the web interface**

Open your browser and go to: `http://localhost:5000`

3. **Upload a document**

Click "Choose a file" and select a document (PDF, DOCX, XLSX, CSV)

4. **Select an LLM model**

Choose from the available models in the dropdown

5. **Ask questions about your document**

Type your query in the chat input and press Enter

## 🧩 How It Works

1. **Document Processing**: When you upload a document, the application extracts its text content
2. **Text Chunking**: The text is divided into manageable chunks
3. **Vector Embedding**: Each chunk is converted into a vector embedding using Ollama
4. **Semantic Search**: When you ask a question, the application finds the most relevant chunks
5. **Response Generation**: The LLM generates a response based on the retrieved chunks


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the document processing framework
- [Ollama](https://ollama.ai/) for providing local LLM capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
