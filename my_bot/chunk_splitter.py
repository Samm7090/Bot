from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_load_data(doc: list, chunk_size=1000, chunk_overlap=200):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(doc)

    return chunks
