from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k)
        if not results:
            return "No relevant information was found in the knowledge base."

        context = "\n\n".join(
            f"[{index}] Source: "
            f"{result['metadata'].get('source') or result['metadata'].get('doc_id') or result.get('id', 'unknown')}\n"
            f"{result['content']}"
            for index, result in enumerate(results, start=1)
        )
        prompt = (
            "Answer the question using only the context below. "
            "Cite supporting chunks by number, such as [1]. "
            "If the context does not contain the answer, say so.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        return self.llm_fn(prompt)
