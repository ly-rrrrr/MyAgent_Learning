# LangGraph Demo：最小 StateGraph Agent

这个阶段先不接真实 LLM。目标是只理解 LangGraph 的三个核心：

1. `State`：图里流动的数据。
2. `Node`：接收 state，返回 state 的局部更新。
3. `Edge`：控制节点之间怎么流动，包括普通边和条件边。



## 代码学习顺序

### 1. State 定义

在 `simple_agent.py` 里：

```python
class AgentState(TypedDict):
```

字段含义：

- `question`：用户原始输入。
- `route`：路由节点决定下一步走哪里。
- `tool_result`：工具节点执行后的结果。
- `answer`：最终返回给用户的答案。

### 2. Node 节点

每个 Node 都是一个普通 Python 函数：

```python
def route_question(state: AgentState) -> dict[str, str]:
```

规则是：

- 输入：完整 state。
- 输出：只返回要更新的字段。
- 保持逻辑简单，方便复用和测试。

当前 demo 有三个节点：

- `route_question`：判断问题是否需要计算工具。
- `calculate`：执行一个极简计算工具。
- `write_answer`：根据 state 生成最终回答。

辅助函数：

- `extract_expression`：从用户问题里提取四则运算表达式。
- `evaluate_expression`：执行规则模拟的计算工具，并把异常转成可读结果。

### 3. Edge 边

普通边：

```python
graph.add_edge("calculate", "write_answer")
```

意思是 `calculate` 执行完以后固定去 `write_answer`。

条件边：

```python
graph.add_conditional_edges("route_question", choose_next_node, ...)
```

意思是 `route_question` 执行完以后，调用 `choose_next_node(state)` 判断下一步去哪。

条件边本身不直接改 state，它只读取 `route_question` 写入的 `route` 字段，然后选择下一个节点。

## 当前图流程

```text
route_question
  ├─ 如果需要计算 -> calculate -> write_answer -> END
  └─ 如果不需要计算 -> write_answer -> END
```

## 调试建议

完整的运行和断点调试命令见：

```text
LangGraph_demo/RUN_COMMANDS.md
```

第一遍重点看 `final_state`：

```text
question: 用户输入
route: 条件边选择的路线
tool_result: 工具执行结果
answer: 最终回答
```

等你熟悉这个流程后，下一阶段再把 `route_question` 和 `write_answer` 换成真实 LLM 调用。
