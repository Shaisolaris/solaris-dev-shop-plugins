#!/usr/bin/env python3
"""Verify the generated plugin against its pinned upstream Git revision."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tarfile
import tempfile

import yaml


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_source(path):
    head = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    raw = subprocess.check_output(["git", "-C", str(path), "archive", "--format=tar", head])
    result = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        for entry in archive:
            if entry.isdir():
                continue
            assert entry.isfile(), "non-regular upstream source: " + entry.name
            result[entry.name] = archive.extractfile(entry).read()
    return head, result


def validate(root, revision, source):
    package = root / "plugin"
    build = json.loads((root / "BUILD.json").read_text())
    provenance = json.loads((package / "SOLARIS-BUILD-SOURCE.json").read_text())
    assert build["source_commit"] == provenance["source_commit"] == revision, "revision mismatch"
    assert provenance["source_path_map"] == {"README.md": "SOURCE-README.md"}
    assert provenance["omitted_repository_config"] == [".gitignore"]
    expected = {provenance["source_path_map"].get(name, name): sha(data)
                for name, data in source.items() if name != ".gitignore"}
    assert provenance["canonical_files"] == expected, "source manifest mismatch"
    for name, digest in expected.items():
        file = package / name
        assert file.is_file() and not file.is_symlink(), "missing/non-regular source: " + name
        assert sha(file.read_bytes()) == digest, "changed source: " + name
    paths = ["chief-of-staff/SKILL.md"] + sorted(name for name in source
             if re.fullmatch(r"employees/[^/]+/[^/]+/SKILL.md", name))
    assert len(paths) == 62, "original role roster changed"
    index = json.loads((package / "native/skills.json").read_text())
    expected_skills = []
    for path in paths:
        metadata = yaml.safe_load(source[path].decode().split("---", 2)[1])
        expected_skills.append({"name": metadata["name"], "description": metadata["description"], "canonical": path})
    assert index == expected_skills, "workflow index differs from source"
    assert len({skill["name"] for skill in index}) == 62
    extra = {"README.md", "DATA-HANDLING.md", "assets/native-plugin-icon.png", "plugin.json",
             ".claude-plugin/plugin.json", "package.json", "native/skills.json", "native/opencode.mjs",
             "server.mjs", "SOLARIS-BUILD-SOURCE.json"}
    for skill in index:
        relative = "skills/" + skill["name"] + "/SKILL.md"
        extra.add(relative)
        file = package / relative
        text = file.read_text()
        metadata = yaml.safe_load(text.split("---", 2)[1])
        assert metadata == {"name": skill["name"], "description": skill["description"]}
        link = "../../" + skill["canonical"]
        assert "](" + link + ")" in text
        assert (file.parent / link).resolve() == (package / skill["canonical"]).resolve()
    actual = set()
    for file in package.rglob("*"):
        assert not file.is_symlink(), "symlink in plugin"
        if file.is_file():
            actual.add(str(file.relative_to(package)))
    assert actual == set(expected) | extra, "unexpected or missing package files"
    portable = json.loads((package / "plugin.json").read_text())
    claude = json.loads((package / ".claude-plugin/plugin.json").read_text())
    node = json.loads((package / "package.json").read_text())
    assert portable["version"] == claude["version"] == node["version"] == build["plugin_version"]
    assert portable["name"] == claude["name"] == "solaris-dev-shop"
    assert portable["extensions"]["com.openai"]["requires_local_executor"] is True
    assert portable["author"]["name"] == claude["author"]["name"] == "Solaris Technologies"
    assert "mcpServers" not in claude and "hooks" not in claude
    assert node["dependencies"] == {"@opencode/plugin": "2.1.2"}
    icon = (package / "assets/native-plugin-icon.png").read_bytes()
    assert icon[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", icon[16:24])
    assert width == height and 512 <= width <= 2048 and len(icon) < 2 * 1024 * 1024
    assert sha(icon) == provenance["listing_icon_sha256"]
    openai_catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
    claude_catalog = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    assert openai_catalog["name"] == claude_catalog["name"] == "solaris-technologies"
    assert openai_catalog["plugins"][0]["source"]["path"] == claude_catalog["plugins"][0]["source"] == "./plugin"
    for folder in [root, package]:
        for link in re.findall(r"\]\(([^)]+)\)", (folder / "README.md").read_text()):
            if not link.startswith(("https:", "#")):
                assert (folder / link).is_file(), "broken README link: " + link
    return {"source_commit": revision, "canonical_files": len(expected), "workflows": len(index),
            "native_formats": 3, "icon_dimensions": [width, height], "result": "PASS"}


def controls(root, revision, source):
    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary) / "distribution"
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
        probes = [
            ("changed helper", "plugin/employees/product-project/delivery-lead/delivery_evidence.py", b"print('stub')\n"),
            ("missing workflow", "plugin/skills/backend-developer/SKILL.md", None),
            ("dropped workflow index", "plugin/native/skills.json", b"[]\n"),
            ("unbound revision", "BUILD.json", json.dumps(dict(json.loads((copy / "BUILD.json").read_text()), source_commit="0" * 40)).encode()),
        ]
        rejected = []
        for label, name, replacement in probes:
            file = copy / name
            original = file.read_bytes()
            if replacement is None:
                file.unlink()
            else:
                file.write_bytes(replacement)
            try:
                validate(copy, revision, source)
            except (AssertionError, OSError, ValueError, KeyError):
                rejected.append(label)
            finally:
                file.write_bytes(original)
            assert label in rejected, "negative control falsely accepted: " + label
        return rejected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    revision, files = read_source(args.source)
    result = validate(root, revision, files)
    if args.self_test:
        result["rejected_controls"] = controls(root, revision, files)
    print(json.dumps(result, indent=2))
