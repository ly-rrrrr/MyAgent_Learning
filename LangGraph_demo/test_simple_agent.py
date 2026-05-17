import unittest

from LangGraph_demo.simple_agent import calculate, configure_output, run


class FakeOutput:
    def __init__(self):
        self.encoding = "cp1252"
        self.configured_encoding = None

    def reconfigure(self, *, encoding):
        self.configured_encoding = encoding


class SimpleAgentTest(unittest.TestCase):
    def test_routes_plain_question_directly_to_answer(self):
        final_state = run("你好，介绍一下 StateGraph")

        self.assertEqual(final_state["route"], "answer")
        self.assertEqual(final_state["tool_result"], "")
        self.assertIn("不需要工具", final_state["answer"])

    def test_routes_math_question_through_calculate_node(self):
        final_state = run("请计算 12 * 7")

        self.assertEqual(final_state["route"], "calculate")
        self.assertEqual(final_state["tool_result"], "12 * 7 = 84")
        self.assertIn("计算工具", final_state["answer"])

    def test_calculate_reports_invalid_expression_without_raising(self):
        result = calculate(
            {
                "question": "请计算 12 / 0",
                "route": "calculate",
                "tool_result": "",
                "answer": "",
            }
        )

        self.assertIn("计算失败", result["tool_result"])

    def test_configure_output_switches_stdout_to_utf8(self):
        output = FakeOutput()

        configure_output(output)

        self.assertEqual(output.configured_encoding, "utf-8")


if __name__ == "__main__":
    unittest.main()
