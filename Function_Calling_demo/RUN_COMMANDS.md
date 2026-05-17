# Function Calling Demo 启动命令

## 普通运行

```powershell
node function_calling_agent.js "北京现在几点？顺便计算 12*7"
```

## 断点调试运行

```powershell
node --inspect-brk function_calling_agent.js "北京现在几点？顺便计算 12*7"
```

然后在 Chrome 打开：

```text
chrome://inspect
```

找到 Node.js 进程后点击 `inspect`。

## 调试时重点观察

- `messages`：完整对话历史，每一轮都会发给模型。
- `data`：模型接口返回的完整 JSON。
- `data.choices[0].message`：模型这一轮返回的 assistant 消息。
- `msg.tool_calls`：模型请求调用的工具列表。
- `args`：模型传给本地函数的参数。
- `result`：本地函数执行后的结果。

