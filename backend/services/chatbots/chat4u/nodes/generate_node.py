from langchain_core.messages import AIMessage

from ..chains.generate_chain import generate_chain


def generate(state):
    print("---GENERATE---")
    question = state["messages"][-1].content
    documents = state["documents"]

    docs_content = "\n\n".join(doc.page_content for doc in documents)

    generation = generate_chain.invoke(
        {
            "context": docs_content,
            "question": question,
            "chat_history": state["messages"],
        }
    )
    message = state["messages"] + [AIMessage(content=generation)]

    return {"documents": documents, "messages": messages}
