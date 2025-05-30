import json
from typing import Iterable, Dict, Any, Generator


def load_jsonl(path: str) -> Generator[Dict[str, Any], None, None]:
    """Load a JSONL file yielding dictionaries."""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def dump_jsonl(data: Iterable[Dict[str, Any]], path: str) -> None:
    """Write dictionaries to a JSONL file."""
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
