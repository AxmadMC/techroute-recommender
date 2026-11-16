import pytest

from scripts.evaluate_reliability import PROFILES as EVALUATION_PROFILES
from src import main as app
from src.logging_config import configure_logging
from src.path_generator import FALLBACK_SOURCE
from src.profiles import (
    DEFAULT_PROFILE_NAME,
    EVALUATION_PROFILE_NAMES,
    PROFILE_LABELS,
    PROFILE_PRESETS,
)


def test_missing_dataset_exits_cleanly_without_traceback(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(app, "DATASET_PATH", tmp_path / "missing.csv")
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "logs" / "test.log"),
    )

    exit_code = app.main([])
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
    monkeypatch.setitem(
        app.PROFILE_PRESETS,
        DEFAULT_PROFILE_NAME,
        {**app.PROFILE_PRESETS[DEFAULT_PROFILE_NAME], "skill_level": 2},
    )

    exit_code = app.main([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "invalid profile" in captured.err
    assert "skill_level must be a number from 0 to 1" in captured.err
    assert "Traceback" not in captured.err


def test_list_profiles_prints_all_preset_names(capsys):
    exit_code = app.main(["--list-profiles"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.splitlines() == list(PROFILE_PRESETS)


def test_unknown_profile_exits_with_clean_error(capsys):
    exit_code = app.main(["--profile", "not_a_real_profile"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "unknown profile 'not_a_real_profile'" in captured.err
    assert all(name in captured.err for name in PROFILE_PRESETS)
    assert "Traceback" not in captured.err


def test_offline_profile_uses_fallback_without_calling_gemini(
    monkeypatch, tmp_path, capsys
):
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "logs" / "offline.log"),
    )
    monkeypatch.setattr(
        "src.path_generator._call_gemini",
        lambda *args: pytest.fail("offline mode must not call Gemini"),
    )

    exit_code = app.main(["--profile", "cybersecurity_beginner", "--offline"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert f"{FALLBACK_SOURCE} (reason: offline mode)" in captured.out
    assert "offline mode sends no data to Gemini" in captured.out


def test_no_options_uses_software_engineering_default_without_gemini(
    monkeypatch, tmp_path, capsys
):
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "logs" / "default.log"),
    )
    captured_profile = {}
    captured_guides = {}

    def fake_pipeline(
        profile, offline=False, dataset_path=None, use_guides=True
    ):
        captured_profile.update(profile)
        captured_guides["enabled"] = use_guides
        return {
            "recommendations": [],
            "learning_path": {"steps": []},
            "source_label": "test source",
            "fallback_reason": None,
        }

    monkeypatch.setattr(app, "run_pipeline", fake_pipeline)

    exit_code = app.main([])
    capsys.readouterr()

    assert exit_code == 0
    assert captured_profile == PROFILE_PRESETS[DEFAULT_PROFILE_NAME]
    assert captured_profile["target_track"] == "software_engineering"
    assert captured_guides["enabled"]


def test_no_guides_flag_disables_track_context(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "no-guides.log"),
    )
    captured = {}

    def fake_pipeline(profile, offline=False, dataset_path=None, use_guides=True):
        captured["use_guides"] = use_guides
        return {
            "recommendations": [],
            "learning_path": {"steps": []},
            "source_label": "test source",
            "fallback_reason": None,
        }

    monkeypatch.setattr(app, "run_pipeline", fake_pipeline)
    exit_code = app.main(["--no-guides"])
    capsys.readouterr()

    assert exit_code == 0
    assert captured["use_guides"] is False


def test_trace_flag_prints_agent_trace_after_learning_path(
    monkeypatch, tmp_path, capsys
):
    monkeypatch.setattr(
        app,
        "configure_logging",
        lambda: configure_logging(tmp_path / "trace.log"),
    )
    monkeypatch.setattr(
        app,
        "run_pipeline",
        lambda profile, offline=False, dataset_path=None, use_guides=True: {
            "recommendations": [],
            "learning_path": {
                "steps": [],
                "trace": [
                    {
                        "step_name": "PLAN",
                        "attempt_number": 1,
                        "decision": "accepted",
                        "detail": "Created a plan.",
                        "verifier_errors": [],
                        "plan": [],
                    }
                ],
            },
            "source_label": "test source",
            "fallback_reason": None,
        },
    )

    exit_code = app.main(["--trace"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.index("Generated learning path") < captured.out.index(
        "Agent trace:"
    )
    assert "PLAN (attempt 1): accepted - Created a plan." in captured.out


def test_cli_and_evaluator_use_shared_profile_presets():
    assert app.PROFILE_PRESETS is PROFILE_PRESETS
    assert set(EVALUATION_PROFILE_NAMES) == set(PROFILE_PRESETS)
    assert EVALUATION_PROFILES == [
        (PROFILE_LABELS[name], PROFILE_PRESETS[name])
        for name in EVALUATION_PROFILE_NAMES
    ]
