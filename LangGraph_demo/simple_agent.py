from __future__ import annotations

import re
import sys
from typing import TextIO, Literal, TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    """State is the shared data object passed between all nodes.

    question: the original user input.
    route: the next branch chosen by the router node.
    tool_result: result produced by the tool node, if any.
    answer: final text returned to the user.
    """

    question: str
    route: Literal["calculate", "answer"]
    tool_result: str
    answer: str


def extract_expression(question: str) -> str:
    """Pick the first arithmetic expression from the user question."""

    match = re.search(r"\d[\d+\-*/().\s]*", question)
    return match.group(0).strip() if match else ""


def evaluate_expression(expression: str) -> str:
    """Evaluate a small arithmetic expression for this teaching demo."""

    if not expression or not re.fullmatch(r"[\d+\-*/().\s]+", expression):
        return "没有找到合法的四则运算表达式。"

    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as exc:
        return f"计算失败：{exc}"

    return f"{expression} = {result}"


def route_question(state: AgentState) -> dict[str, str]:
    """Node: inspect the question and decide whether a tool is needed."""

    question = state["question"]
    has_math = bool(re.search(r"\d+\s*[+\-*/]\s*\d+", question))
    return {"route": "calculate" if has_math else "answer"}


def calculate(state: AgentState) -> dict[str, str]:
    """Node: run a tiny arithmetic tool and write its result into state."""

    expression = extract_expression(state["question"])
    return {"tool_result": evaluate_expression(expression)}


def write_answer(state: AgentState) -> dict[str, str]:
    """Node: produce the final answer from the current state."""

    if state.get("tool_result"):
        return {"answer": f"我调用了计算工具，结果是：{state['tool_result']}"}

    return {"answer": f"这是一个不需要工具的问题：{state['question']}"}


def choose_next_node(state: AgentState) -> Literal["calculate", "write_answer"]:
    """Conditional edge: choose where the graph should go next."""

    return "calculate" if state["route"] == "calculate" else "write_answer"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("route_question", route_question)
    graph.add_node("calculate", calculate)
    graph.add_node("write_answer", write_answer)

    graph.set_entry_point("route_question")

    graph.add_conditional_edges(
        "route_question",
        choose_next_node,
        {
            "calculate": "calculate",
            "write_answer": "write_answer",
        },
    )
    graph.add_edge("calculate", "write_answer")
    graph.add_edge("write_answer", END)

    return graph.compile()


def run(question: str) -> AgentState:
    app = build_graph()
    initial_state: AgentState = {
        "question": question,
        "route": "answer",
        "tool_result": "",
        "answer": "",
    }
    return app.invoke(initial_state)


def configure_output(output: TextIO) -> None:
    """Use UTF-8 for CLI output when the runtime allows it."""

    if hasattr(output, "reconfigure"):
        output.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    configure_output(sys.stdout)
    user_question = " ".join(sys.argv[1:]) or "请计算 12 * 7"
    final_state = run(user_question)

    print("\nFinal state:")
    for key, value in final_state.items():
        print(f"{key}: {value}")

    print("\nAnswer:")
    print(final_state["answer"])


