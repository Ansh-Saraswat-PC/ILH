from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Define the structured schema for the evaluation report
class EvalResult(BaseModel):
    score: int = Field(description="Score from 1 to 5 based on accuracy and helpfulness.")
    reasoning: str = Field(description="Why this score was given.")

class AgentEvaluator:
    def __init__(self, llm=None):
        # Swap out OpenAI for Gemini
        base_llm = llm or ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")
        
        self.eval_chain = base_llm.with_structured_output(EvalResult)
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert enterprise AI evaluator. Grade the agent's actual response based on the given task and expected outcome. Be critical of hallucinations or skipped tool usage."),
            ("human", "Task Given to Agent: {task}\nExpected Outcome/Knowledge: {expected_outcome}\nAgent's Actual Response: {agent_response}")
        ])

    def evaluate(self, task: str, expected_outcome: str, agent_response: str):
        """Executes the automated evaluation loop."""
        formatted_messages = self.prompt_template.format_messages(
            task=task,
            expected_outcome=expected_outcome,
            agent_response=agent_response
        )
        
        result = self.eval_chain.invoke(formatted_messages)
        
        print(f"\n--- Evaluation Score: {result.score}/5 ---")
        print(f"Reasoning: {result.reasoning}\n")
        return result.score