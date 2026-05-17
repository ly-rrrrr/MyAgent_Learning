# Agent 学习日志

## 阶段 1：Function Calling

状态：完成

目录：`Function_Calling_demo`

重点：

- `messages`：完整对话历史。
- `tool_calls`：模型请求调用的工具列表。
- `role: tool`：把本地工具执行结果放回对话。
- 多轮循环：模型请求工具，本地执行工具，再把结果交回模型继续回答。

## 阶段 2：LangGraph StateGraph

状态：进行中

目录：`LangGraph_demo`

重点：

- `State`：用 `TypedDict` 定义图中流动的数据字段和用途。
- `Node`：普通函数，输入完整 state，输出局部更新。
- `Edge`：用普通边和条件边控制流程。

当前进展：

- 已实现最小 `StateGraph` Agent。
- 先不接真实 LLM，用规则模拟路由、工具调用和回答生成。
- 已覆盖基础测试：普通回答路线、计算路线、异常计算兜底。
