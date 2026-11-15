from src import main as app
from src.logging_config import configure_logging


def test_missing_dataset_exits_cleanly_without_traceback(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(app, "DATASET_PATH", tmp_path / "missing.csv")
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "logs" / "test.log"),
    )

    exit_code = app.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "unable to load data/opportunities.csv" in captured.err
    assert "FileNotFoundError" in captured.err
    assert "Traceback" not in captured.err


def test_invalid_default_profile_exits_with_validation_message(
    monkeypatch, tmp_path, capsys
):
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "logs" / "test.log"),
    )
    monkeypatch.setattr(app, "DEFAULT_PROFILE", {**app.DEFAULT_PROFILE, "skill_level": 2})

    exit_code = app.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "invalid profile" in captured.err
    assert "skill_level must be a number from 0 to 1" in captured.err
    assert "Traceback" not in captured.err
