import configparser
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever

config = configparser.ConfigParser()
config.read("config.ini")

# initialize
llm_model = ChatGroq(model=config['AI']['model'], api_key=config['AI']['key'])
embedding_model = HuggingFaceEmbeddings(model_name=config['AI']['embedding'])
vector = Chroma(embedding_function=embedding_model ,persist_directory="./vectorstore").as_retriever()

# prompts
context = """
Given a chat history and the latest user question \
which might reference context in the chat history, \
formulate a standalone question which can be understood \
without the chat history. Do NOT answer the question, \
just reformulate it if needed, otherwise return it as it is.
"""
context_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", context),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

llm = """
You are a Document-Understanding AI assistant designed to answer questions \
from documents provided to you. Use the retrieved context below to answer question \
If you don't know the answer to a question, make it known. \
Lastly, make the interaction friendly and lively as possible.\n\n
{context}
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", llm),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

# rag chain setup
history_chain = create_history_aware_retriever(
    llm_model, vector, context_prompt
)
qa_chain = create_stuff_documents_chain(llm_model, prompt)
main_chain = create_retrieval_chain(history_chain, qa_chain)

def store_chat(memory: list, query: str, resp: str):
    memory.extend(
        [
            HumanMessage(content=query),
            AIMessage(content=resp)
        ]
    )

def call_rag(input: str, chat_memory: dict) -> str:
    resp = main_chain.invoke({'input': input, 'history': chat_memory})
    store_chat(chat_memory, input, resp['answer'])
    return resp['answer']