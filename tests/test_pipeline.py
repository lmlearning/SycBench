from sycbench.datasets import load_jsonl, dump_jsonl
from sycbench.templates import load_templates
from sycbench.pipeline import transform_dataset


def test_transform(tmp_path):
    inp = tmp_path / 'in.jsonl'
    inp.write_text('{"question": "Q", "answer": "A", "belief": "B", "history": ""}\n')
    tpl = tmp_path / 'tpl.yaml'
    tpl.write_text('belief_influence:\n  pattern: "{question} - {belief}"\n')
    out = tmp_path / 'out.jsonl'
    transform_dataset(str(inp), str(out), str(tpl), 'belief_influence')
    data = out.read_text().strip()
    assert 'Q - B' in data
