from typing import Iterable, Dict, Any, List

from .datasets import load_jsonl, dump_jsonl
from .templates import load_templates, Template
from .validator import validate_prompts, ValidationError


def transform_dataset(input_path: str, output_path: str, template_path: str, template_name: str) -> None:
    templates = load_templates(template_path)
    template = templates[template_name]

    data = load_jsonl(input_path)
    transformed: List[Dict[str, Any]] = []
    for qa in data:
        item = template.apply(qa)
        item['original'] = qa
        transformed.append(item)

    errors = validate_prompts(transformed)
    if errors:
        raise ValidationError('\n'.join(errors))

    dump_jsonl(transformed, output_path)
