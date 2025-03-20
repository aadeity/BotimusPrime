import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import langchain
from langchain.llms import Ollama
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders.excel import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS



app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'xls', 'csv', 'txt'}
MODELS = ['gemma:2b', 'gemma:7b', 'llama3:8b', 'mistral:7b']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Creating uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template('index.html', models=MODELS)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        #  creating a vector store
        try:
            documents = load_document(filepath)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            texts = text_splitter.split_documents(documents)

            #  embeddings using Ollama
            embeddings = OllamaEmbeddings(model="gemma:2b")


            vectorstore = FAISS.from_documents(documents=texts, embedding=embeddings)

            return jsonify({'success': True, 'filename': filename})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File type not allowed'}), 400


def load_document(filepath):

    ext = filepath.split('.')[-1].lower()

    if ext == 'pdf':
        loader = PyPDFLoader(filepath)
    elif ext == 'docx':
        loader = Docx2txtLoader(filepath)
    elif ext in ['xlsx', 'xls']:
        loader = UnstructuredExcelLoader(filepath)
    elif ext == 'csv':
        loader = CSVLoader(filepath)
    elif ext == 'txt':
        with open(filepath, 'r') as f:
            text = f.read()
        return [Document(page_content=text)]
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()


@app.route('/query', methods=['POST'])
def query_document():
    data = request.json
    if not data or 'query' not in data or 'filename' not in data or 'model' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    query = data['query']
    filename = data['filename']
    model_name = data['model']

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        # Loading the document
        documents = load_document(filepath)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)

        # embeddings and vector store
        embeddings = OllamaEmbeddings(model="gemma:2b")
        vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)

        # Creating retriever
        retriever = vectorstore.as_retriever()

        # Initializing LLM
        llm = Ollama(model=model_name)

        # Creating QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

        # Getting the responsee
        response = qa_chain.run(query)

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
