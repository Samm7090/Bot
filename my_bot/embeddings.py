# from langchain_community.embeddings import SentenceTransformerEmbeddings

# def sentence_transformer_embedding(model_name: str = 'all-MiniLM-L6-v2'):
#     sentence_transformer = SentenceTransformerEmbeddings(model_name=model_name)
#     return sentence_transformer


#------------------------------------
"Updated code because of deprecation of langchain_community.embeddings.SentenceTransformerEmbeddings"
"the above code was giving warning during runtime HuggingFaceEmbeddings will soon be moved out of "
"langchain_community into a new package called langchain-huggingface."
#------------------------------------
from langchain_huggingface import HuggingFaceEmbeddings

def sentence_transformer_embedding(model_name: str = 'all-MiniLM-L6-v2'):
 
    return HuggingFaceEmbeddings(model_name=model_name)
