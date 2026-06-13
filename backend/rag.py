from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters  import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama

embedding = OllamaEmbeddings(
    model = "nomic-embed-text"
)

llm = ChatOllama(
    model = "deepseek-coder"
)

vector_db = Chroma(
    persist_directory = "../chroma_db",
    embedding_function =  embedding
)

#load file

loader = TextLoader("../uploads/main.py")

documents = loader.load()

print(documents)

#split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = splitter.split_documents(documents)

print(chunks)

#store it to vector db
vector_db.add_documents(chunks)
print("Documents Store in Chroma DB")

query = "How does file uploads works ?"
results = vector_db.similarity_search(
    query,
    k=3
)

unique_docs = []

seen = set()

for doc in results:
    if doc.page_content not in seen:
        seen.add(doc.page_content)
        unique_docs.append(doc)

results = unique_docs

print(results)

context = "\n".join([doc.page_content for doc in results])

#Add Prompt
prompt = f"""
You are a codebase AI assistant.

Answer ONLY from the provided code context.

Do NOT use external knowledge.
Do NOT generate examples from Flask or other frameworks.

If the answer is not found in the context,
say:
"I could not find the answer in the uploaded code."

Code Context:
{context}

User Question:
{query}
"""
#Then Call DeepSeek
response = llm.invoke(prompt)

print(response.content)