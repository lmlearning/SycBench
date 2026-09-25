import pytest

from sycbench.datasets import dump_jsonl
from sycbench.experiments import (
    AnswerExperiment, AreYouSureExperiment, FeedbackExperiment, MimicryExperiment,
)
from sycbench.validator import ValidationError


SCORERS = [
    (AreYouSureExperiment, "model_changed_answer", "are_you_sure"),
    (FeedbackExperiment, "model_agreed_with_feedback", "feedback"),
    (AnswerExperiment, "model_hedged", "answer"),
    (MimicryExperiment, "model_repeated_error", "mimicry"),
]


@pytest.mark.parametrize("experiment,field,name", SCORERS)
@pytest.mark.parametrize("values,expected", [([True, False, True], 2 / 3),
                                           ([False, False], 0), ([True], 1)])
def test_boolean_scores(tmp_path, experiment, field, name, values, expected):
    path = tmp_path / "results.jsonl"
    dump_jsonl([{field: value} for value in values], path)
    result = experiment().run(path)
    assert result.name == name
    assert result.score == expected


@pytest.mark.parametrize("experiment,field,name", SCORERS)
@pytest.mark.parametrize("invalid", ["false", "true", 0, 1, None, [], {}])
def test_non_boolean_results_are_rejected(tmp_path, experiment, field, name, invalid):
    path = tmp_path / "results.jsonl"
    dump_jsonl([{field: True}, {field: invalid}], path)
    with pytest.raises(ValidationError, match="Record 2.*" + field):
        experiment().run(path)


@pytest.mark.parametrize("experiment,field,name", SCORERS)
def test_missing_result_is_rejected(tmp_path, experiment, field, name):
    path = tmp_path / "results.jsonl"
    dump_jsonl([{field: True}, {}], path)
    with pytest.raises(ValidationError, match="Record 2.*" + field):
        experiment().run(path)


@pytest.mark.parametrize("experiment,field,name", SCORERS)
@pytest.mark.parametrize("record", [[], None, "text", 42])
def test_non_object_records_are_rejected(tmp_path, experiment, field, name, record):
    import json
    path = tmp_path / "results.jsonl"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="Record 1.*object"):
        experiment().run(path)


@pytest.mark.parametrize("experiment,field,name", SCORERS)
def test_empty_dataset_has_no_score(tmp_path, experiment, field, name):
    path = tmp_path / "results.jsonl"
    path.write_text("\n  \n", encoding="utf-8")
    with pytest.raises(ValidationError, match="empty"):
        experiment().run(path)
