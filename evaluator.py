from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# 1. Define your custom enterprise tools here
@tool
def process_refund(customer_id: str, amount: float) -> str:
    """Useful for processing refunds in customer support use-cases."""
    # Mock logic - replace with actual hackathon API/logic
    return f"Successfully initiated refund of ${amount} for customer {customer_id}."

@tool
def query_database(query: str) -> str:
    """Useful for looking up user records or financial data."""
    # Mock logic - you will map this to the actual dataset
    return f"Database results for {query}: Active subscriber, tier 1."

class EnterpriseAgent:
    def __init__(self, llm=None, tools=None):
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-4o")
        # Base tools + whatever specific tools you add on the day
        self.tools = tools or [process_refund, query_database]
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            handle_parsing_errors=True
        )

    def execute_task(self, prompt: str):
        """Run the agent on a specific problem statement."""
        print(f"Executing: {prompt}")
        return self.agent.run(prompt)