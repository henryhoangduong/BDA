from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from core.factories.llm_factory import get_llm
from langchain.schema import Document
import json
import logging
import re
logger = logging.getLogger(__name__)

llm = get_llm()


async def generate_qa_from_chunks(
    chunks: List[Document],
) -> List[Dict[str, str]]:
    try:
        prompt = PromptTemplate(
            input_variables=["chunk"],
            template=(
                "Here is a passage from a document:\n\n"
                "{chunk}\n\n"
                "Please generate **one** question about the content above, "
                "and provide its answer. "
                "Respond in JSON format exactly like:\n"
                '{{\"question\": \"<your question>\", \"answer\": \"<your answer>\"}}'
            )
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        qas: List[Dict[str, str]] = []
        for chunk in chunks:
            print("chunk: ", chunk)
            result: dict = chain.invoke({"chunk": chunk.page_content})
            raw_text: str = result.get("text", "")

            m = re.search(r"```json\n(.*)```", raw_text, flags=re.DOTALL)
            json_str = m.group(1) if m else raw_text

            try:
                qa = json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.warning(
                    "Could not parse JSON from LLM output: %s\nError: %s", json_str, e)
                continue

            qas.append({**(chunk.model_dump()), **qa})

        return qas
    except Exception as e:
        logger.error("Error creating qa dataset: ", e)
        raise e


if __name__ == "__main__":
    import json

    chunks = [
        "Alice was beginning to get very tired of sitting by her sister on the bank...",
        "The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly..."
    ]

    qa_pairs = generate_qa_from_chunks(chunks)
    for idx, qa in enumerate(qa_pairs, 1):
        print(f"{idx}. Q: {qa['question']}\n   A: {qa['answer']}\n")
