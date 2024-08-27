# DocAI
A Document Understanding AI system that gleans insights from PDF documents.

# Features
* CLI Frontend: Provides an easy-to-use command-line interface for user interactions.
* Web Frontend: Provides a very simple interactive UI.
* Content Processing: Capable of accepting and processing information from PDF files.
* Natural Language Processing: Receives, understands, and provides feedback in natural language.
* Context-Aware: Understands conversation context and answers questions accordingly.
* Retrieval and Generation: Delivers answers grounded in facts, minimizing the chances of hallucination.
* Vector Storage: Stores and retrieves text vector representations.
* Feedback Mechanism: Allows users to provide additional context (e.g., more PDFs).

# Tech Stack
* Python
* LangChain
* ChromaDB
* Groq Language Models
* Streamlit

# Installation
* Clone this repository: git clone [https://github.com/Adlai-1/DocAI](https://github.com/Adlai-1/DocAI).
* Install the needed packages: pip install -r requirements.txt (must be executed in the project directory)
* Add your API key to config.ini You can obtain an API key from GroqCloud (https://console.groq.com/keys)
* Execute "python -m streamlit run web/home.py" to run the WebUI.
* Execute "python ui/server.py" to start the server before running the User client using "python ui/client.py"


# DocAI snapshots
![Screenshot (33)](https://github.com/user-attachments/assets/1cf25d1c-4aaa-4a4e-b1b4-64a3a199edec)
![Screenshot (34)](https://github.com/user-attachments/assets/fd6f83b1-6b31-468c-b6ad-d9561e753760)
![Screenshot (35)](https://github.com/user-attachments/assets/0564902b-c716-412b-a837-4dee1390fb23)
![Screenshot (36)](https://github.com/user-attachments/assets/f8180618-27a1-4f00-97bc-bcc10f1aa6ca)
![Screenshot (44)](https://github.com/user-attachments/assets/1d92fa46-3c3f-46a1-876d-aab4ef81747b)
![Screenshot (43)](https://github.com/user-attachments/assets/49e9175a-2b59-4d44-a7ca-fe644d5b61cb)
