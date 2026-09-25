import json
import subprocess
import sys

import pytest

from sycbench.pipeline import iter_transformed, transform_dataset
from sycbench.templates import Template
from sycbench.validator import ValidationError


@pytest.mark.parametrize("record,message", [
    ([], "JSON object"), ({"question": "Q"}, "answer"),
    ({"question": "Q", "answer": None}, "answer"),
    ({"question": "Q", "answer": "  "}, "answer"),
    ({"answer": "A"}, "question"),
])
def test_invalid_records_have_context(record, message):
    with pytest.raises(ValidationError, match="Record 1:.*" + message):
        list(iter_transformed([record], Template("question", "{question}")))


def test_empty_prompt_is_rejected():
    with pytest.raises(ValidationError, match="empty prompt"):
        list(iter_transformed([{"answer": "A"}], Template("empty", " ")))


def test_transformation_is_lazy_and_preserves_zero_answer():
    consumed = []
    def records():
        for i in range(3):
            consumed.append(i)
            yield {"question": f"Q{i}", "answer": i}
    transformed = iter_transformed(records(), Template("question", "{question}"))
    assert consumed == []
    first = next(transformed)
    assert consumed == [0]
    assert first == {"prompt": "Q0", "expected_answer": 0, "original": {"question": "Q0", "answer": 0}}


def test_late_validation_error_preserves_existing_output(tmp_path):
    source = tmp_path / "input.jsonl"
    source.write_text(json.dumps({"question": "Q", "answer": "A"}) + '\n{}\n')
    template = tmp_path / "templates.yaml"
    template.write_text('test:\n  pattern: "{question}"\n')
    destination = tmp_path / "output.jsonl"
    destination.write_bytes(b"original\n")
    with pytest.raises(ValidationError, match="Record 2"):
        transform_dataset(source, destination, template, "test")
    assert destination.read_bytes() == b"original\n"
    assert not list(tmp_path.glob(".*.tmp"))


def test_unknown_template_cli_error_is_actionable(tmp_path):
    template = tmp_path / "templates.yaml"
    template.write_text('known:\n  pattern: "{question}"\n')
    result = subprocess.run([
        sys.executable, "-m", "sycbench", "transform", "--input", str(tmp_path / "input.jsonl"),
        "--output", str(tmp_path / "output.jsonl"), "--templates", str(template), "--experiment", "missing",
    ], capture_output=True, text=True)
    assert result.returncode == 2
    assert "Available templates: known" in result.stderr
    assert "Traceback" not in result.stderr
