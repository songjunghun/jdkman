from pathlib import Path

import pytest

import jdkman.installer as installer
from jdkman.installer import make_jvm_dir_name, find_dist_jvm_root


def _info(vendor, image_type="jdk", features=None, major_version=21):
    return {
        "vendor": vendor,
        "image_type": image_type,
        "features": features or [],
        "jvm_impl": "hotspot",
        "major_version": major_version,
    }


@pytest.mark.parametrize("info, expected", [
    # 기본
    (_info("zulu"),                                "zulu-21.jdk"),
    (_info("temurin"),                             "temurin-21.jdk"),
    (_info("zulu", major_version=17),       "zulu-17.jdk"),
    # JRE
    (_info("zulu", image_type="jre"),       "zulu-21.jre"),
    # vendor alias
    (_info("graalvm"),                             "graalvm-ce-21.jdk"),
    (_info("graalvm-community"),                   "graalvm-ce-21.jdk"),
    (_info("oracle-graalvm"),                      "graalvm-21.jdk"),
    (_info("microsoft"),                           "ms-21.jdk"),
    (_info("jetbrains"),                           "jbr-21.jdk"),
    # feature 포함
    (_info("zulu", features=["javafx"]),    "zulu-javafx-21.jdk"),
    # notarized 는 무시
    (_info("kona", features=["notarized"]), "kona-21.jdk"),
])
def test_make_jvm_root_name(info, expected):
    assert make_jvm_dir_name(info) == expected


def _touch_java(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def test_find_dist_jvm_root_macos(tmp_path, monkeypatch):
    monkeypatch.setattr(installer, "is_macos", lambda: True)
    monkeypatch.setattr(installer, "is_windows", lambda: False)
    jvm_root = tmp_path / "zulu-21.jdk"
    _touch_java(jvm_root / "Contents" / "Home" / "bin" / "java")

    assert find_dist_jvm_root(tmp_path) == jvm_root


def test_find_dist_jvm_root_windows(tmp_path, monkeypatch):
    monkeypatch.setattr(installer, "is_macos", lambda: False)
    monkeypatch.setattr(installer, "is_windows", lambda: True)
    jvm_root = tmp_path / "jdk-21"
    _touch_java(jvm_root / "bin" / "java.exe")

    assert find_dist_jvm_root(tmp_path) == jvm_root


def test_find_dist_jvm_root_linux(tmp_path, monkeypatch):
    monkeypatch.setattr(installer, "is_macos", lambda: False)
    monkeypatch.setattr(installer, "is_windows", lambda: False)
    jvm_root = tmp_path / "jdk-21"
    _touch_java(jvm_root / "bin" / "java")

    assert find_dist_jvm_root(tmp_path) == jvm_root
