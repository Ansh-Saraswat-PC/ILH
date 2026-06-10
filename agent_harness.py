import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import tool

# 1. Define your custom enterprise tools
@tool
def process_refund(customer_id: str, amount: float) -> str:
    """Useful for processing refunds in customer support use-cases."""
    return f"Successfully initiated refund of ${amount} for customer {customer_id}."

@tool
def query_database(query: str) -> str:
    """Useful for looking up user records or financial data."""
    return f"Database results for {query}: Active subscriber, tier 1, customer_id 992 found."

class EnterpriseAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")
        
        self.tools_map = {
            "process_refund": process_refund,
            "query_database": query_database
        }
        
        self.model_with_tools = self.llm.bind_tools(list(self.tools_map.values()))

    def execute_task(self, task_input: str):
        """Runs an explicit, visible reasoning loop."""
        print(f"\n[Agent] Starting task: {task_input}")
        messages = [HumanMessage(content=task_input)]
        
        # NEW: Keep a log of actions for the judge to see
        execution_trace = [] 
        
        for turn in range(5):
            print(f"[Agent] Turn {turn + 1}: Thinking...")
            response = self.model_with_tools.invoke(messages)
            messages.append(response)
            
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_id = tool_call["id"]
                    
                    print(f"  -> CALLING TOOL: {tool_name} with arguments {tool_args}")
                    actual_tool = self.tools_map[tool_name]
                    tool_output = actual_tool.invoke(tool_args)
                    print(f"  -> TOOL OUTPUT: {tool_output}")
                    
                    # Log the exact action and result
                    execution_trace.append(f"Tool Used: {tool_name} | Args: {tool_args} | Result: {tool_output}")
                    
                    messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_id))
            else:
                print("[Agent] Task complete.")
                # Pass both the answer AND the evidence back to the evaluator
                trace_log = "\n".join(execution_trace)
                return f"{response.content}\n\n[SYSTEM LOG - EVIDENCE OF EXECUTION]\n{trace_log}"
                
        return "Loop limit reached without a final answer."