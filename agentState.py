from typing import TypedDict, List
class AgentState(TypedDict, total=False):
    input: str
    
    tasks:List[str]
    intermediate_steps: List[str]  
    History_value: List[int]
    final_output: str

