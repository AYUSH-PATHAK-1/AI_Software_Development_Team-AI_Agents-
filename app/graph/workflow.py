from langgraph.graph import END, START, StateGraph

from graph.nodes import manager_node, planner_node, coder_node, file_writer_node, tester_node, debugger_node,  reviewer_node, architect_node, researcher_node
from state.state import AgentState


def route_after_testing(state: AgentState) -> str:
    if state["status"] == "tests_passed":
        return "passed"
    
    if state["debug_attempts"] >= 3:
        return "max_attempts"

    return "failed"

def route_after_review(state: AgentState) -> str:
    review = state["review"]

    if review is None:
        raise ValueError("Review result is missing.")

    if review.approved:
        return "approved"

    if state["review_attempts"] >= 3:
        return "max_review_attempts"

    return "rejected"


builder = StateGraph(AgentState)


# builder.add_node("planner", planner_node)
builder.add_node("manager", manager_node)
builder.add_node("researcher", researcher_node)
builder.add_node("architect", architect_node)
builder.add_node("coder", coder_node)
builder.add_node("file_writer", file_writer_node)
builder.add_node("tester", tester_node)
builder.add_node("debugger", debugger_node)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "manager")
builder.add_edge("manager", "researcher")
# builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "architect")
builder.add_edge("architect", "coder")
builder.add_edge("coder", "file_writer")
builder.add_edge("file_writer", "tester")
builder.add_conditional_edges("tester", route_after_testing,
    {
    "passed": "reviewer",
    "failed": "debugger",
    "max_attempts": END,
})
builder.add_edge("debugger", "file_writer")
builder.add_conditional_edges(
    "reviewer",
    route_after_review,
    {
        "approved": END,
        "rejected": "coder",
        "max_review_attempts": END,
    },
)


graph = builder.compile()