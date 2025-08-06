from langchain_ollama import ChatOllama

def get_llm(module_name="qwen2.5:3b"):
    return ChatOllama(model=module_name)