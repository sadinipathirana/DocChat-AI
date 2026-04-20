# DocChat AI

DocChat AI is a web application that allows users to upload PDF documents and chat with an AI assistant about their content. Built with Flask and powered by AI models, it provides an interactive way to query and understand document information.

## Features

- Upload PDF documents
- AI-powered chat interface for document queries
- User-friendly web interface

## Tech Stack

- Python 3.10+
- Flask
- LangChain
- GPT4All (local model)
- FAISS (vector similarity search)
- HuggingFace Sentence Transformers
- HTML, CSS, JavaScript

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/docchat-ai.git
   cd docchat-ai
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Upload a PDF document using the web interface
2. Ask questions about the document content in the chat interface
3. Receive AI-generated responses based on the document

## Project Structure

- `app.py`: Main Flask application
- `requirements.txt`: Python dependencies
- `runtime.txt`: Runtime specification
- `models/`: AI model files
- `static/`: CSS and static assets
- `templates/`: HTML templates
- `uploads/`: Uploaded document storage
- `pdf sample/`: Sample PDF files
