import pytest

import jdkman.config as config


@pytest.mark.parametrize("system, machine, expected", [
    ("windows", "amd64", "https://mise-java.jdx.dev/jvm/ga/windows/x86_64.json"),
    ("windows", "arm64", "https://mise-java.jdx.dev/jvm/ga/windows/aarch64.json"),
    ("darwin",  "arm64", "https://mise-java.jdx.dev/jvm/ga/macosx/aarch64.json"),
    ("linux",   "x86_64", "https://mise-java.jdx.dev/jvm/ga/linux/x86_64.json"),
])
def test_get_jvm_api_url_per_platform(monkeypatch, system, machine, expected):
    monkeypatch.setattr(config, "_platform_system", system)
    monkeypatch.setattr(config, "_platform_machine", machine)

    assert config.get_jvm_api_url() == expected
