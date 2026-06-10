import os
from dotenv import load_dotenv

# Load the file
load_dotenv()

# Check both variations
print("Is GEMINI_API_KEY active?:", "GEMINI_API_KEY" in os.environ)

from rag_core import EnterpriseRAG
from agent_harness import EnterpriseAgent
from evaluator import AgentEvaluator

# ... rest of your main.py code remains exactly the same ...

def main():
    # 11:30 AM: Ingestion & Setup
    # TODO: Replace with the actual file they give you at the event
    dataset_file = "dummy_enterprise_data.csv" 
    
    print("=== STEP 1: INITIALIZING RAG ===")
    rag = EnterpriseRAG()
    # rag.ingest_data(dataset_file) # Uncomment when file is present
    
    print("\n=== STEP 2: SPINNING UP AGENT ===")
    agent_system = EnterpriseAgent()
    
    # 12:30 PM: Problem Statement Testing
    test_task = "Look up the records for customer ID 992 and process a refund of $45.00."
    expected_result = "Agent should use query_database tool, then use process_refund tool."
    
    actual_response = agent_system.execute_task(test_task)
    
    print("\n=== STEP 3: RUNNING EVALUATIONS ===")
    # 03:00 PM: Optimization & Benchmarking
    evaluator = AgentEvaluator()
    evaluator.evaluate(test_task, expected_result, actual_response)

if __name__ == "__main__":
    main()