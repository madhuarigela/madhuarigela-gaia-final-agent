from calculator_tool import build_calculator_tool
from file_tools import build_file_reader_tool
from web_fetch_tool import build_webpage_fetch_tool
from web_search_tool import build_web_search_tool

def build_all_tools():
    return [
        build_calculator_tool(),
        build_file_reader_tool(),
        build_web_search_tool(),
        build_webpage_fetch_tool(),
    ]
