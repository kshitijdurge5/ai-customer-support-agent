import pytest
from safe_tools import call_tool

def test_count_words():
    assert call_tool("count_words", {"text": "hello world"}) == 2

def test_unknown_tool_blocked():
    with pytest.raises(ValueError):
        call_tool("run_shell", {"command": "whoami"})
