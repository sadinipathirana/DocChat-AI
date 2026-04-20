from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import uuid

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import GPT4All
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# === Setup ===
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Global Vars ===
db = None
qa_chain = None
chat_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# === Routes ===

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global db, qa_chain, chat_memory

    file = request.files.get('pdf')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = str(uuid.uuid4()) + '.pdf'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # === Load and Chunk PDF ===
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    # === Embeddings (HuggingFace) ===
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)

    # === Load GPT4All Local Model ===
    llm = GPT4All(model="./models/ggml-gpt4all-j-v1.3-groovy.bin")

    # === Patch generate() to avoid unsupported 'max_tokens' ===
    original_generate = llm.client.generate
    def safe_generate(prompt, **kwargs):
        kwargs.pop("max_tokens", None)
        return original_generate(prompt, **kwargs)
    llm.client.generate = safe_generate

    # === Create Conversational QA Chain ===
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(),
        memory=chat_memory
    )

    return jsonify({"message": "PDF processed and chat is ready!", "filename": filename})

@app.route('/chat', methods=['POST'])
def chat():
    global qa_chain
    if not qa_chain:
        return jsonify({'response': 'Please upload a PDF first.'}), 400

    query = request.json.get('message', '').strip()
    if not query:
        return jsonify({'response': 'Empty question'}), 400

    try:
        print("[QUERY RECEIVED]", query)
        result = qa_chain.run(query)
        print("[GPT RESPONSE]", result)
        return jsonify({'response': result})
    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({'response': f'[Error] {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
