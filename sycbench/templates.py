from dataclasses import dataclass
from typing import Dict


@dataclass
class Template:
    name: str
    pattern: str

    def apply(self, qa: Dict[str, str]) -> Dict[str, str]:
        prompt = self.pattern.format(**qa)
        return {"prompt": prompt, "expected_answer": qa.get("answer", "")}


def load_templates(path: str) -> Dict[str, Template]:
    """Load simple template file without external dependencies."""
    templates: Dict[str, Template] = {}
    current_name = None
    pattern_lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            if not line.startswith(' '):
                if current_name:
                    templates[current_name] = Template(name=current_name, pattern=''.join(pattern_lines).strip())
                    pattern_lines = []
                current_name = line.rstrip(':\n')
            else:
                # assume "  pattern: ..." format
                parts = line.strip().split(':', 1)
                if len(parts) == 2 and parts[0] == 'pattern':
                    pattern_lines.append(parts[1].strip().strip('"'))
    if current_name:
        templates[current_name] = Template(name=current_name, pattern=''.join(pattern_lines).strip())
    return templates
