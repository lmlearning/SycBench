import json
import os
from pathlib import Path
import tempfile
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
    """Replace a JSONL file only after the complete iterable is written.

    Serialization, iteration, or write failures leave an existing destination
    untouched. The temporary file lives beside the destination so replacement
    stays on the same filesystem. This does not guarantee power-loss durability.
    """
    destination = Path(path)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', dir=destination.parent,
            prefix=f'.{destination.name}.', suffix='.tmp', delete=False,
        ) as f:
            temporary_path = Path(f.name)
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
