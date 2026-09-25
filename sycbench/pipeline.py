from typing import Iterable, Dict, Any, Iterator

from .datasets import load_jsonl, dump_jsonl
from .templates import load_templates, Template
from .validator import ValidationError


def iter_transformed(data: Iterable[Dict[str, Any]], template: Template) -> Iterator[Dict[str, Any]]:
    """Validate and transform one record at a time, retaining source context."""
    for record_number, qa in enumerate(data, start=1):
        context = f"Record {record_number}: "
        if not isinstance(qa, dict):
            raise ValidationError(context + "expected a JSON object")
        if 'answer' not in qa or qa['answer'] is None or (isinstance(qa['answer'], str) and not qa['answer'].strip()):
            raise ValidationError(context + "a nonempty 'answer' is required")
        try:
            item = template.apply(qa)
        except (KeyError, ValueError, IndexError, AttributeError, TypeError) as error:
            raise ValidationError(context + f"cannot apply template '{template.name}': {error}") from error
        if not item['prompt'].strip():
            raise ValidationError(context + "template produced an empty prompt")
        item['original'] = qa
        yield item


def transform_dataset(input_path: str, output_path: str, template_path: str, template_name: str) -> None:
    templates = load_templates(template_path)
    if template_name not in templates:
        available = ', '.join(sorted(templates)) or '(none)'
        raise ValidationError(f"Unknown template '{template_name}'. Available templates: {available}")
    # dump_jsonl replaces the destination only after this iterator finishes.
    dump_jsonl(iter_transformed(load_jsonl(input_path), templates[template_name]), output_path)
