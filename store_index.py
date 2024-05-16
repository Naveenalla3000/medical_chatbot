import os
from src.helper import load_pdf
from src.helper import text_split
from src.helper import download_hugging_face_embedding
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient
from dotenv import load_dotenv
load_dotenv()

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_HOST = os.getenv("PINECONE_API_HOST")
PINECONE_API_INDEX = os.getenv("PINECONE_API_INDEX")

# Load PDFs
extracted_data = load_pdf("data/")

# Split text into chunks
text_chunks = text_split(extracted_data)

# Download Hugging Face Embeddings
embeddings = download_hugging_face_embedding()

# initialize Pinecone client
pc = PineconeClient(api_key=PINECONE_API_KEY)
index_name = PINECONE_API_INDEX

# Store embeddings in Pinecone
dosearch = PineconeVectorStore.from_texts(
    [
        tc.page_content for tc in text_chunks
    ],
    embeddings,
    index_name=index_name,
)
