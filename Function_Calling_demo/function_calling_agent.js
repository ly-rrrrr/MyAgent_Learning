// Minimal Function Calling agent: no SDK, no framework, just fetch + messages.
// Run: node function_calling_agent.js "time in Beijing and 12*7"
// Debug: node --inspect-brk function_calling_agent.js "time in Beijing and 12*7"

const BASE_URL = process.env.OPENAI_BASE_URL || "https://aihubmix.com/v1";
const API_URL = `${BASE_URL}/chat/completions`;
const MODEL = process.env.OPENAI_MODEL || "gpt-5.4-nano";
const API_KEY = process.env.OPENAI_API_KEY || "your key";

const objectSchema = (properties, required) => ({
  type: "object",
  properties,
  required,
  additionalProperties: false,
});
const tools = [
  { type: "function", function: {
    name: "get_current_time",
    description: "Get current local time for a city.",
    parameters: objectSchema({ city: { type: "string", description: "City name" } }, ["city"]),
  } },
  { type: "function", function: {
    name: "calculate",
    description: "Evaluate a simple arithmetic expression.",
    parameters: objectSchema({
      expression: { type: "string", description: "Example: 12 * 7" },
    }, ["expression"]),
  } },
];

function getCurrentTime({ city }) {
  const zones = {
    beijing: "Asia/Shanghai",
    shanghai: "Asia/Shanghai",
    tokyo: "Asia/Tokyo",
    london: "Europe/London",
    newyork: "America/New_York",
    "new york": "America/New_York",
  };
  const timeZone = zones[String(city).toLowerCase()] || "UTC";
  const time = new Intl.DateTimeFormat("zh-CN", {
    dateStyle: "full",
    timeStyle: "long",
    timeZone,
  }).format(new Date());
  return { city, timeZone, time };
}

function calculate({ expression }) {
  if (!/^[\d+\-*/().\s]+$/.test(expression)) {
    throw new Error("Only simple arithmetic is allowed.");
  }
  return { expression, result: Function(`"use strict"; return (${expression})`)() };
}

const functions = { get_current_time: getCurrentTime, calculate };

async function chat(messages) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model: MODEL, messages, tools, tool_choice: "auto" }),
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
  return res.json();
}

async function runAgent(input) {
  const messages = [
    { role: "system", content: "You are concise. Use tools for live data or calculations." },
    { role: "user", content: input },
  ];

  for (let step = 0; step < 5; step += 1) {
    debugger; // Use: node --inspect-brk function_calling_agent.js "..."
    const data = await chat(messages);
    const msg = data.choices[0].message;
    messages.push(msg);
    console.log(`\n--- assistant turn ${step + 1} ---`);
    console.dir(msg, { depth: null });

    const calls = msg.tool_calls || [];
    if (calls.length === 0) return msg.content;

    for (const call of calls) {
      const name = call.function.name;
      const args = JSON.parse(call.function.arguments || "{}");
      const result = functions[name] ? functions[name](args) : { error: `Unknown function: ${name}` };
      messages.push({ role: "tool", tool_call_id: call.id, content: JSON.stringify(result) });
    }
  }
  throw new Error("Too many tool-calling rounds.");
}

const input = process.argv.slice(2).join(" ") || "What time is it in Beijing? Also calculate 12 * 7.";
runAgent(input)
  .then((answer) => console.log(`\nFinal answer:\n${answer}`))
  .catch((err) => { console.error(err); process.exitCode = 1; });
