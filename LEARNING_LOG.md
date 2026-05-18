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
- 已完成 `debugpy` 断点调试，理解 `app.invoke(initial_state)` 如何驱动 state 沿图流动。
- 已整理 LangGraph 调试命令、断点位置、重点观察字段和总体流程到 `LangGraph_demo/RUN_COMMANDS.md`。

调试时重点观察：

- `question`：用户原始输入。
- `route`：路由节点写入，条件边读取。
- `tool_result`：工具节点写入。
- `answer`：最终回答节点写入。

核心理解：

```text
build_graph() 定义图结构
initial_state 提供本次运行的数据
app.invoke(initial_state) 启动图执行
Node 返回局部更新
Edge 根据 state 决定下一步
```
