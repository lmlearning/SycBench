# SycBench

SycBench is a lightweight framework for generating sycophancy evaluation datasets
from existing question answering corpora. It provides utilities for dataset
processing, template application, and simple validation. The framework can be
invoked through the command line to transform datasets using YAML templates.

## Usage

```
python -m sycbench transform \
    --input data/input.jsonl \
    --output data/output.jsonl \
    --templates templates/standard.yaml \
    --experiment belief_influence
```

This command reads a JSONL dataset, applies the `belief_influence` template
from the provided YAML file, validates the generated prompts, and stores the
resulting evaluation dataset.

## Templates

Templates are defined in YAML files and specify a `pattern` used to generate
prompts. The template engine substitutes keys from the source data into the
pattern. An example template file:

```yaml
belief_influence:
  pattern: |
    The user believes "{belief}". Question: {question}
```

Additional templates can be added to capture different forms of sycophancy.

## Experiments

The `sycbench.experiments` module provides simple experiment drivers replicating
common sycophancy tests such as *Are You Sure?*, *Feedback*, *Answer*, and
*Mimicry*. These experiments operate on JSONL logs from model evaluations and
produce aggregated scores.

## License

This project is licensed under the terms of the MIT license.
