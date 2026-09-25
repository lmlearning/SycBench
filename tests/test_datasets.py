import pytest

from sycbench.datasets import dump_jsonl, load_jsonl


def test_round_trip_replaces_existing_file_with_unicode_records(tmp_path):
    path = tmp_path / "dataset.jsonl"
    path.write_text("old contents\n", encoding="utf-8")
    records = [{"prompt": "Café?"}, {"answer": True}]
    dump_jsonl(iter(records), path)
    assert list(load_jsonl(path)) == records
    assert "Café" in path.read_text(encoding="utf-8")
    assert list(tmp_path.iterdir()) == [path]


def invalid_records():
    yield {"valid": True}
    yield {"invalid": object()}


def interrupted_records():
    yield {"valid": True}
    raise RuntimeError("input interrupted")


@pytest.mark.parametrize("records,error", [
    (invalid_records, TypeError),
    (interrupted_records, RuntimeError),
])
@pytest.mark.parametrize("existing", [True, False])
def test_failure_preserves_destination_and_removes_temporary_file(
    tmp_path, records, error, existing,
):
    path = tmp_path / "dataset.jsonl"
    original = b'{"original": true}\n'
    if existing:
        path.write_bytes(original)
    with pytest.raises(error):
        dump_jsonl(records(), path)
    if existing:
        assert path.read_bytes() == original
    else:
        assert not path.exists()
    assert list(tmp_path.iterdir()) == ([path] if existing else [])


def test_empty_input_replaces_destination_with_empty_file(tmp_path):
    path = tmp_path / "dataset.jsonl"
    path.write_text("old contents", encoding="utf-8")
    dump_jsonl([], path)
    assert path.read_bytes() == b""


def test_failed_replacement_preserves_destination(tmp_path, monkeypatch):
    path = tmp_path / "dataset.jsonl"
    path.write_bytes(b"original\n")

    def fail_replace(source, destination):
        raise PermissionError("destination unavailable")

    monkeypatch.setattr("sycbench.datasets.os.replace", fail_replace)
    with pytest.raises(PermissionError, match="destination unavailable"):
        dump_jsonl([{"valid": True}], path)
    assert path.read_bytes() == b"original\n"
    assert list(tmp_path.iterdir()) == [path]
