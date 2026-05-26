from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "deepseek-coder"
)

response = llm.invoke("Write Python API Example")

print(response.content)
