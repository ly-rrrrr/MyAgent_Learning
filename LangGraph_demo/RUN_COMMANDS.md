# LangGraph Demo 启动和调试命令

## 普通运行

在项目根目录运行：

```powershell
python LangGraph_demo/simple_agent.py "请计算 12 * 7"
```

也可以运行一个不需要工具的问题：

```powershell
python LangGraph_demo/simple_agent.py "你好，介绍一下 StateGraph"
```

## 断点调试运行

Python 版的 `node --inspect-brk` 可以用 `debugpy`：

```powershell
python -m debugpy --listen 5678 --wait-for-client LangGraph_demo/simple_agent.py "请计算 12 * 7"
```

如果要调试不走工具的路径：

```powershell
python -m debugpy --listen 5678 --wait-for-client LangGraph_demo/simple_agent.py "你好，介绍一下 StateGraph"
```

`--wait-for-client` 会让程序等待 VS Code 调试器连接，所以命令执行后终端暂时没有输出是正常的。

## VS Code 连接方式

如果 `.vscode/launch.json` 里没有配置，可以添加：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to debugpy 5678",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      }
    }
  ]
}
```

注意：VS Code 选择的 Python 解释器要安装了 `langgraph`。如果命令行能运行，但 VS Code 调试报 `No module named 'langgraph'`，通常是 VS Code 选错了解释器。

## 推荐断点

建议第一轮一次性加完这些断点：

- `run`：看 `initial_state` 如何创建。
- `route_question`：看路由节点如何写入 `route`。
- `choose_next_node`：看条件边如何根据 `route` 选择下一个节点。
- `calculate`：看工具节点如何写入 `tool_result`。
- `write_answer`：看最终回答节点如何写入 `answer`。

## 重点观察字段

调试时主要观察 `state` 里的四个字段：

- `question`：用户原始输入，一般从开始到结束不变。
- `route`：路由节点写入，用来控制条件边。
- `tool_result`：工具节点写入，表示工具执行结果。
- `answer`：最终回答节点写入。

还要重点观察两个返回值：

- `route_question` 返回的局部更新，例如 `{"route": "calculate"}`。
- `choose_next_node` 返回的下一个节点名，例如 `"calculate"` 或 `"write_answer"`。

## 总体流程

计算问题的流程：

```text
initial_state
  -> route_question
  -> choose_next_node
  -> calculate
  -> write_answer
  -> END
```

普通问题的流程：

```text
initial_state
  -> route_question
  -> choose_next_node
  -> write_answer
  -> END
```

核心理解：

```text
State 记录当前上下文
Node 接收完整 state，返回局部更新
Edge 根据 state 决定下一个 Node
app.invoke(initial_state) 让初始数据沿着图开始流动
```

`app = build_graph()` 得到的是编译好的图结构，不是某一次运行的数据。`initial_state` 才是本次运行的输入，`app.invoke(initial_state)` 才是真正开始执行图。
