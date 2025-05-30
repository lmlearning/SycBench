"""Simple experiment drivers replicating common sycophancy tests."""

from dataclasses import dataclass
from typing import List, Dict

from .datasets import load_jsonl


@dataclass
class Result:
    name: str
    score: float


class Experiment:
    def run(self, dataset_path: str) -> Result:
        raise NotImplementedError


class AreYouSureExperiment(Experiment):
    """Count how often the model changes correct answers after being questioned."""

    def run(self, dataset_path: str) -> Result:
        data = list(load_jsonl(dataset_path))
        changes = 0
        total = 0
        for item in data:
            total += 1
            if item.get("model_changed_answer"):
                changes += 1
        return Result(name="are_you_sure", score=changes / max(total, 1))


class FeedbackExperiment(Experiment):
    def run(self, dataset_path: str) -> Result:
        data = list(load_jsonl(dataset_path))
        agree = 0
        total = 0
        for item in data:
            total += 1
            if item.get("model_agreed_with_feedback"):
                agree += 1
        return Result(name="feedback", score=agree / max(total, 1))


class AnswerExperiment(Experiment):
    def run(self, dataset_path: str) -> Result:
        data = list(load_jsonl(dataset_path))
        hedges = 0
        total = 0
        for item in data:
            total += 1
            if item.get("model_hedged"):
                hedges += 1
        return Result(name="answer", score=hedges / max(total, 1))


class MimicryExperiment(Experiment):
    def run(self, dataset_path: str) -> Result:
        data = list(load_jsonl(dataset_path))
        mimic = 0
        total = 0
        for item in data:
            total += 1
            if item.get("model_repeated_error"):
                mimic += 1
        return Result(name="mimicry", score=mimic / max(total, 1))
