# Custom Chatbot using LangChain

## 🚀 Project Overview
This project is a **custom chatbot** built using **LangChain** and **Hugging Face models**. It scrapes course details from Brainlox website, stores embeddings in a **FAISS vector database**, and provides intelligent responses to user queries. The chatbot can categorize courses, fetch prices, and handle natural language queries effectively.

## 🛠️ Tech Stack
- **Python** 🐍
- **Flask** 🌐 (for API)
- **LangChain** 🔗 (for LLM-based retrieval)
- **FAISS** 📂 (for vector search)
- **Hugging Face Transformers** 🤗 (for embeddings & LLM)
- **BeautifulSoup** 🏗️ (for web scraping)

## ✨ Features
- 🔍 **Real-time Course Retrieval**: Scrapes course data from Brainlox.
- 📂 **Vector-based Storage**: Uses FAISS for efficient search.
- 🤖 **AI-Powered Query Handling**: Leverages LangChain for intelligent responses.
- 💰 **Price Lookup**: Fetches and displays course prices.
- 🏷 **Category-based Filtering**: Lists courses based on their category (Java, Python, Web Dev, etc.).
- ⚡ **Fast & Lightweight API**: Built using Flask.

## 📌 Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/custom-chatbot-langchain.git
   cd custom-chatbot-langchain
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Mac/Linux
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application
Start the Flask server:
```bash
python app.py
```
The API will be available at `http://127.0.0.1:5000/`

## 🛠 API Endpoints
### Query Courses
- **Endpoint:** `POST /query`
- **Request Body:**
  ```json
  {
    "query": "List all Java courses"
  }
  ```
- **Response:**
  ```json
  {
    "response": ["Java Basics", "Advanced Java", "Java Spring Boot"]
  }
  ```

## 📂 Project Structure
```
📦 custom-chatbot-langchain
├── 📂 faiss_index            # FAISS vector store
├── 📄 app.py                 # Main application logic
├── 📄 requirements.txt        # Dependencies
├── 📄 README.md              # Project documentation
└── 📄 .gitignore             # Ignored files
```

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit PRs.

## 📜 License
This project is licensed under the **MIT License**.

---
Made with ❤️ using LangChain & Python 🚀

