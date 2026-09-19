from smolagents import Tool

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate arithmetic expressions accurately. Use this for calculations."
    inputs = {"expression": {"type": "string", "description": "A mathematical expression."}}
    output_type = "string"

    def forward(self, expression: str) -> str:
        allowed = {"abs": abs, "round": round, "min": min, "max": max, "sum": sum}
        return str(eval(expression, {"__builtins__": {}}, allowed))

def build_calculator_tool():
    return CalculatorTool()
