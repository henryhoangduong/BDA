from langchain_core.prompts import ChatPromptTemplate

from core.factories.llm_factory import get_llm
from models.simbadoc import SimbaDoc

llm = get_llm()

prompt = ChatPromptTemplate.from_template(
    """
        # Extraction Prompt — Mode "Guideflexible"  
        *(Atlanta Sanad Documents – Insurance, Morocco)*  

        ## Role  
        Insurance/legal analyst tasked with condensing any Atlanta Sanad document (policy, endorsement, GTC, claim guide, FAQ, internal note, etc.) into a guide intended for a research LLM.

        ## Objective  
        Capture **all** key points: concepts, amounts, clauses, actors, dates, relationships, and conditions; provide the LLM with a “map” to locate any information, even from a vague question.

        ## Content Guidelines  
        - Review the entire text; no relevant information should be omitted even if it does not fit a predefined template.  
        - Summarize without personal interpretation; preserve legal terminology and quotation marks for important clauses.  
        - When necessary, create your **own sub-sections** to organize atypical information.  
        - Mention every named entity (product, coverage, exclusion, stakeholder, body, law, decree, amount, date, phone number, procedure).  
        - Briefly describe relationships or conditions (e.g., triggers, thresholds, dependencies between coverages).  
        - If information does not “fit” anywhere, place it under **“Other Key Points”**.

        ## Style & Format  
        - Flexible hierarchical Markdown: you may add, rename, or remove sections depending on the document.  
        - Each item: short sentence or bullet ending with “;” or “.”.  
        - No nested numbered lists deeper than two levels to maintain readability.  
        - No JSON, no tables.  
        - Start with the short title of the document in **bold**, followed by a “:”.

        ## Skeleton (to adapt freely)  

        text  
        **Short Title** :

        ### Overview  
        Brief summary of the document’s purpose and scope;

        ### Key Concepts & Entities  
        - …;

        ### Coverages / Insurances  
        - …;

        ### Conditions, Limits & Thresholds  
        - …;

        ### Procedures (Subscription, Claim, Termination, etc.)  
        - …;

        ### Legal Bases & References  
        - …;

        ### Other Key Points  
        - …;

        Here is the document:  
        {document}
    """
)

summary_chain = prompt | llm


def summarize_document(simbadoc: SimbaDoc) -> str:
    docs_content = "\n\n".join(doc.page_content for doc in simbadoc.documents)
    response = summary_chain.invoke({"document": docs_content})
    return response.content
