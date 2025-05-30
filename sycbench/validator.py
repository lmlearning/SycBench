from typing import Iterable, Dict, List


class ValidationError(Exception):
    pass


def validate_prompts(prompts: Iterable[Dict[str, str]]) -> List[str]:
    """Return list of error messages."""
    errors = []
    for i, item in enumerate(prompts):
        if 'prompt' not in item:
            errors.append(f"Item {i} missing 'prompt'")
        if 'expected_answer' not in item:
            errors.append(f"Item {i} missing 'expected_answer'")
    return errors
