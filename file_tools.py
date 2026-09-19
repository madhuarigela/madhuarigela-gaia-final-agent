from pathlib import Path
import json
import pandas as pd
from smolagents import Tool

class FileReaderTool(Tool):
    name = "inspect_file"
    description = "Read an attached local file. Supports PDF, XLSX, CSV, DOCX, JSON, TXT, and similar text files."
    inputs = {"path": {"type": "string", "description": "Path to the file."}}
    output_type = "string"

    def forward(self, path: str) -> str:
        p = Path(path)
        if not p.exists():
            return f"File not found: {p}"
        suffix = p.suffix.lower()
        if suffix in {".txt",".md",".csv",".tsv",".json",".xml",".html"}:
            return p.read_text(errors="ignore")[:12000]
        if suffix in {".xlsx",".xls"}:
            sheets = pd.read_excel(p, sheet_name=None)
            return "\n".join(f"--- {k} ---\n{v.to_string(index=False)}" for k,v in sheets.items())[:12000]
        if suffix == ".pdf":
            from pypdf import PdfReader
            return "\n".join((page.extract_text() or "") for page in PdfReader(str(p)).pages)[:12000]
        if suffix == ".docx":
            from docx import Document
            return "\n".join(x.text for x in Document(str(p)).paragraphs)[:12000]
        try:
            return p.read_text(errors="ignore")[:12000]
        except Exception:
            return f"Unsupported file type: {suffix}"

def build_file_reader_tool():
    return FileReaderTool()
