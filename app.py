import os

# Import the Pinecone modules
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory

# Import the dotenv module
from dotenv import load_dotenv

# Import the chainlit modules
import chainlit as cl

# Import asyncio module for async operations
import asyncio

# Import the local modules
from src.prompt import prompt_template
from src.helper import download_hugging_face_embedding
from src.helper import get_llm

# Load the environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_HOST = os.getenv("PINECONE_API_HOST")
PINECONE_API_INDEX = os.getenv("PINECONE_API_INDEX")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Load the embeddings
embeddings = download_hugging_face_embedding() 

# initialize Pinecone client
pc = PineconeClient(api_key=PINECONE_API_KEY)
index_name = PINECONE_API_INDEX

# Load the Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Initialize the PromptTemplate
PROMPT=PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question","history"]
)

# Configure the ConversationBufferMemory
conversationBufferMemory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
    input_key="question"
)

# Configure the chain type kwargs
chain_type_kwargs={
    "prompt": PROMPT,
    "memory": conversationBufferMemory
}

# set up the llm 
llm = get_llm()

# Initialize the RetrievalQA chain
rqa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs,
)


# Define the on_chat_start event
@cl.on_chat_start
async def on_chat_start():
    print("on_chat_start")
    # Set the app name
    cl.user_session.set("app", "HanaAI-medical-chatbot")

# Define the on_chat_message event
@cl.on_message
async def on_message(message: cl.Message):
    print("on_message", message.content)
    # Get the response from the RetrievalQA chain
    response =  rqa.invoke({"query": message.content})
    # Get the result from the response
    result = response["result"]
    # Send the result
    await cl.Message(content=result).send()

