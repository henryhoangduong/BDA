from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.factories.llm_factory import get_llm

prompt_template = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant
    Your name is BDA assistant
    You are able to answer questions about the documents in the context.
    You are also able to reason and provide general answers
    You always respond in English
    Question: {question}
    Context: {context}  
    Chat History: {chat_history}
    Answer:                                                                                                                                           
"""
)
llm = get_llm()
generate_chain = prompt_template | llm | StrOutputParser()
