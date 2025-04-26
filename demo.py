# Agents_LanGraph/graph.py

from langgraph.graph import StateGraph, END
from Ollama import llm
from prompt import prompt
from utils import TOOLS
from agentState import AgentState

import json

def agent_node(state: AgentState) -> AgentState:
    """
    Agent node function: decides which tool to use or finish the task.
    """
    input_value = state["input"]
    tasks = state.get("tasks", ["finish"])
    task = tasks.pop(0)

    history = state.get("History_value", [])
    intermediate_steps = state.get("intermediate_steps", [])

    formatted_steps = "\n".join(intermediate_steps) if intermediate_steps else "None"

    # Generate a response from the LLM based on task, input, and previous steps
    response = llm.invoke(
        prompt.format_messages(Task=task, input=input_value, intermediate_steps=formatted_steps)
    )

    json_response = json.loads(response)

    if json_response['action'] != "finish":
        # Perform the selected tool action
        tool_name = json_response['action']
        tool_args = json_response['action_input']

        intermediate_steps.append(f"Task: {tool_name} | Args: {tool_args['arg']}")
        result = TOOLS[tool_name].invoke(tool_args)

        history.append(str(input_value))
        input_value = result  # Update input with tool's result

    final_output = ""
    if json_response['action'] == "finish":
        final_output = f"Here is the result: {input_value}"
        history.append(str(input_value))

    # Updated agent state
    updated_state = {
        "input": input_value,
        "tasks": tasks,
        "intermediate_steps": intermediate_steps,
        "History_value": history,
        "final_output": final_output
    }

    print(updated_state)
    print("\n\n")

    return updated_state

def final_node(state: AgentState) -> AgentState:
    """
    Final node: simply returns the final state.
    """
    return state

def build_graph() -> StateGraph:
    """
    Builds and compiles the agent workflow graph.
    """
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        lambda state: "final" if state.get("final_output") else "agent"
    )
    graph.add_edge("final", END)

    return graph.compile()

if __name__ == "__main__":
    # Example Run
    runnable = build_graph()

    initial_state = {
        "input": "5",
        "tasks": [
            "add value to this number :",
            "multiply this number :",
            "finish"
        ],
        "intermediate_steps": [],
        "History_value": []
    }

    result = runnable.invoke(initial_state)
    print("\nFinal Result:", result)
