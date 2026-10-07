import pytest

import jdkman.cli as cli


@pytest.fixture
def out_objs(monkeypatch):
    objs = []
    monkeypatch.setattr(cli, "out", lambda *args, **kwargs: objs.extend(args))
    return objs


def test_outdated_without_installed_skips_catalog_refresh(monkeypatch, out_objs):
    refresh_calls = []
    monkeypatch.setattr(cli, "get_installed", lambda: {})
    monkeypatch.setattr(cli, "get_outdated", lambda clear=False: refresh_calls.append(clear) or {})

    cli.outdated()

    assert refresh_calls == []
    assert len(out_objs) == 1
    assert "No installed JVM distributions." in out_objs[0]


def test_outdated_all_current_reports_up_to_date(monkeypatch, out_objs):
    monkeypatch.setattr(cli, "get_installed", lambda: {"zulu-21": {"version": "21.0.5+11"}})
    monkeypatch.setattr(cli, "get_outdated", lambda clear=False: {})

    cli.outdated()

    assert len(out_objs) == 1
    assert "up-to-date" in out_objs[0]


def test_outdated_refreshes_catalog_and_lists_stale(monkeypatch, out_objs):
    refresh_calls = []
    monkeypatch.setattr(cli, "get_installed", lambda: {"zulu-21": {"version": "21.0.3+9"}})
    monkeypatch.setattr(
        cli, "get_outdated",
        lambda clear=False: refresh_calls.append(clear) or {
            "zulu-21": {"installed": "21.0.3+9", "latest": "21.0.5+11"},
        },
    )

    cli.outdated()

    assert refresh_calls == [True]
    assert len(out_objs) == 1
    assert out_objs[0].row_count == 1
