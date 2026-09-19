import logging
from smolagents import CodeAgent
from model_config import build_model
from tools import build_all_tools

logger = logging.getLogger("gaia_agent")

INSTRUCTIONS = """
You solve GAIA benchmark questions.

Use web_search for factual verification. It returns several compact results.
Use webpage_fetch only when a result URL is useful and its snippet is insufficient.
Use calculator for arithmetic.
Use inspect_file whenever an attachment is provided.

Work efficiently and avoid repeating searches.
After obtaining enough evidence, call final_answer immediately.

Exact-match grading:
- Return ONLY the requested answer.
- Number: digits only unless the question explicitly requests units.
- List: comma-separated values only.
- String: the shortest exact answer.
- Do not write explanations, labels, reasoning, markdown, or "FINAL ANSWER".
""".strip()

def build_agent():
    agent = CodeAgent(
        model=build_model(),
        tools=build_all_tools(),
        max_steps=1,
        verbosity_level=0,
    )
    agent.prompt_templates["system_prompt"] += "\n\n" + INSTRUCTIONS
    return agent

def clean_answer(value):
    text = str(value).strip()
    for prefix in ("FINAL ANSWER:", "Final Answer:", "Answer:"):
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        text = text[1:-1].strip()
    return text
