import os
import gradio as gr
from agent import build_agent, clean_answer
from gaia_client import get_questions, download_attachment, submit

AGENT = None

def get_agent():
    global AGENT
    if AGENT is None:
        AGENT = build_agent()
    return AGENT

def solve_one(item):
    question = item.get("question", item.get("text", ""))
    task_id = item.get("task_id") or item.get("id")
    filename = item.get("file_name") or item.get("filename")
    attachment = download_attachment(task_id, filename) if task_id else None
    if attachment:
        question += f"\n\nAttachment available at: {attachment}. Inspect it before answering."
    try:
        answer = clean_answer(get_agent().run(question))
    except Exception as e:
        answer = f"AGENT_ERROR: {type(e).__name__}: {e}"
    return task_id, answer

def run_all(username, space_id, progress=gr.Progress()):
    questions = get_questions()
    answers = []
    rows = []
    for i, item in enumerate(questions, 1):
        progress(i/len(questions), desc=f"Solving {i}/{len(questions)}")
        task_id, answer = solve_one(item)
        answers.append({"task_id": task_id, "submitted_answer": answer})
        rows.append([i, task_id, answer])
    result = submit(username.strip(), space_id.strip(), answers)
    return rows, result

with gr.Blocks(title="GAIA Final Agent") as demo:
    gr.Markdown("# GAIA Final Agent\nHugging Face Agents Course Unit 4 evaluation agent.")
    with gr.Row():
        username = gr.Textbox(label="Hugging Face username", value=os.getenv("HF_USERNAME", "madhuarigela"))
        space_id = gr.Textbox(label="Public Space ID", value=os.getenv("SPACE_ID", "madhuarigela/gaia-final-agent"))
    run = gr.Button("Run 20-question evaluation", variant="primary")
    table = gr.Dataframe(headers=["#", "Task ID", "Answer"], datatype=["number","str","str"])
    result = gr.JSON(label="Scoring result")
    run.click(run_all, inputs=[username, space_id], outputs=[table, result])

demo.launch()
