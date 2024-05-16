from setuptools import find_packages, setup

setup(
    name="medical_chatbot",
    version="0.0.1",
    author="Naveen alla",
    author_email="naveenalla3000@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "pinecone",
        "langchain-google-genai",
        "pillow",
        "langchain-pinecone",
        "python-dotenv",
        "pypdf",
        "sentence-transformers",
        "chainlit",
    ]
)