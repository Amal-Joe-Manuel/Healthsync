"""Simple PatientAgent using LangChain for sharing medical records."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic


class PatientAgent:
    """Agent that can share medical records via LangChain."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.llm = ChatAnthropic(model=model)
        self._system_prompt = (
            "You are a patient agent that helps share medical records. "
            "Answer questions about the patient's medical history, conditions, "
            "medications, and relevant health information based on the context provided. "
            "Be concise and only share information that is appropriate to disclose."
        )

    def share_records(self, query: str, context: str | None = None) -> str:
        """
        Share medical record information based on the user query and optional context.

        Args:
            query: The question or request about medical records.
            context: Optional medical record context to ground the response.

        Returns:
            The agent's response about the medical records.
        """
        messages = [
            SystemMessage(content=self._system_prompt),
            HumanMessage(
                content=f"Context (medical records):\n{context or 'No context provided.'}\n\nQuery: {query}"
            ),
        ]
        response = self.llm.invoke(messages)
        return response.content if hasattr(response, "content") else str(response)
