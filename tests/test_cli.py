import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from typer.testing import CliRunner
import yaml

from smd.cli import app
from smd.templates import render_project_memory, write_rendered_files


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help_exposes_global_options(self) -> None:
        result = self.runner.invoke(app, ["--help"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("--json", result.output)
        self.assertIn("--root", result.output)
        self.assertIn("--quiet", result.output)
        self.assertIn("--verbose", result.output)

    def test_validate_emits_json_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rendered_files(root, render_project_memory({"project_name": "fixture", "owner": "Tester"}))

            result = self.runner.invoke(app, ["--root", str(root), "--json", "validate"])

            self.assertEqual(result.exit_code, 0, result.output)
            payload = json.loads(result.output)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "smd validate")
            self.assertEqual(payload["root"], str(root.resolve()))
            self.assertIn("data", payload)
            self.assertEqual(payload["warnings"], [])
            self.assertEqual(payload["errors"], [])

    def test_validate_errors_use_json_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = self.runner.invoke(app, ["--root", str(root), "--json", "validate"])

            self.assertEqual(result.exit_code, 1, result.output)
            payload = json.loads(result.output)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["command"], "smd validate")
            self.assertIsNone(payload["data"])
            self.assertEqual(payload["errors"][0]["code"], "MISSING_REQUIRED_FILE")

    def test_backlog_list_pending_uses_memory_foundation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rendered_files(root, render_project_memory({"project_name": "fixture", "owner": "Tester"}))
            package = _make_template_package(root / "package.zip")

            create_result = self.runner.invoke(
                app,
                [
                    "--root",
                    str(root),
                    "--json",
                    "template",
                    "render",
                    str(package),
                    "--project-name",
                    "fixture",
                    "--owner",
                    "Tester",
                ],
            )
            self.assertEqual(create_result.exit_code, 0, create_result.output)

            result = self.runner.invoke(app, ["--root", str(root), "--json", "backlog", "list", "--pending"])

            self.assertEqual(result.exit_code, 0, result.output)
            payload = json.loads(result.output)
            self.assertEqual(payload["data"]["items"][0]["section"], "backlog.item.B-001")

    def test_template_render_reports_created_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = _make_template_package(root / "package.zip")
            target = root / "target"

            result = self.runner.invoke(
                app,
                ["--root", str(root), "--json", "template", "render", str(package), "--target", str(target)],
            )

            self.assertEqual(result.exit_code, 0, result.output)
            payload = json.loads(result.output)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "smd template render")
            self.assertEqual(payload["data"]["package"]["name"], "fixture")
            self.assertEqual(payload["data"]["files"], ["scrum/backlog/B-001.md"])
            self.assertEqual(payload["data"]["instructions"], ["instructions/LLM.md"])
            self.assertTrue((target / "scrum" / "backlog" / "B-001.md").exists())

    def test_invalid_template_package_returns_structured_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "invalid.zip"
            with ZipFile(package, "w") as archive:
                archive.writestr("template.yml", "name: invalid\nfiles: []\ninstructions: []\n")

            result = self.runner.invoke(app, ["--root", str(root), "--json", "template", "render", str(package)])

            self.assertEqual(result.exit_code, 1, result.output)
            payload = json.loads(result.output)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["errors"][0]["code"], "INVALID_TEMPLATE_PACKAGE")

    def test_pack_creates_checksum_signed_zip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = _make_package_directory(root / "package")
            output = root / "package.zip"

            result = self.runner.invoke(
                app,
                ["--root", str(root), "--json", "pack", str(source), "--output", str(output)],
            )

            self.assertEqual(result.exit_code, 0, result.output)
            payload = json.loads(result.output)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "smd pack")
            self.assertEqual(payload["data"]["output"], str(output.resolve()))
            self.assertEqual(payload["data"]["manifest"]["name"], "fixture")
            self.assertEqual(payload["data"]["signature"]["policy"], "checksum-only")
            self.assertEqual(payload["data"]["signature"]["file"], "SIGNATURE.yaml")
            self.assertIn("manifest.yaml", payload["data"]["files"])
            self.assertIn("SIGNATURE.yaml", payload["data"]["files"])

            with ZipFile(output) as archive:
                names = archive.namelist()
                self.assertEqual(names, sorted(names))
                self.assertIn("manifest.yaml", names)
                self.assertIn("SIGNATURE.yaml", names)
                signature = yaml.safe_load(archive.read("SIGNATURE.yaml").decode("utf-8"))
                self.assertEqual(signature["policy"], "checksum-only")
                self.assertEqual(signature["algorithm"], "sha256")
                self.assertEqual(signature["scope"], "file_contents_relative_paths_deterministic_order")
                signed_paths = [item["path"] for item in signature["files"]]
                self.assertIn("manifest.yaml", signed_paths)
                self.assertNotIn("SIGNATURE.yaml", signed_paths)

    def test_pack_rejects_missing_input_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = self.runner.invoke(
                app,
                ["--root", str(root), "--json", "pack", str(root / "missing"), "--output", str(root / "out.zip")],
            )

            self.assertEqual(result.exit_code, 1, result.output)
            payload = json.loads(result.output)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["errors"][0]["code"], "PACK_FAILED")

    def test_pack_rejects_invalid_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "package"
            source.mkdir()
            (source / "manifest.yaml").write_text("name: fixture\n", encoding="utf-8")

            result = self.runner.invoke(
                app,
                ["--root", str(root), "--json", "pack", str(source), "--output", str(root / "out.zip")],
            )

            self.assertEqual(result.exit_code, 1, result.output)
            payload = json.loads(result.output)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["errors"][0]["code"], "PACK_FAILED")
            self.assertIn("missing required field", payload["errors"][0]["message"])

    def test_pack_protects_existing_output_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = _make_package_directory(root / "package")
            output = root / "package.zip"
            output.write_text("existing", encoding="utf-8")

            result = self.runner.invoke(
                app,
                ["--root", str(root), "--json", "pack", str(source), "--output", str(output)],
            )

            self.assertEqual(result.exit_code, 1, result.output)
            payload = json.loads(result.output)
            self.assertFalse(payload["ok"])
            self.assertIn("without --force", payload["errors"][0]["message"])


def _make_template_package(path: Path) -> Path:
    manifest = """
name: fixture
version: "1.0"
instructions:
  - instructions/LLM.md
files:
  - template: templates/backlog_item.md.j2
    target: scrum/backlog/B-001.md
"""
    template = """# B-001 - {{ project_name }}

```yaml
section: backlog.item.B-001
id: B-001
title: {{ project_name }}
status: todo
owner: {{ owner }}
tags: [backlog]
```
"""
    with ZipFile(path, "w") as archive:
        archive.writestr("template.yml", manifest)
        archive.writestr("instructions/LLM.md", "# LLM instructions\n")
        archive.writestr("templates/backlog_item.md.j2", template)
    return path


def _make_package_directory(path: Path) -> Path:
    (path / "templates").mkdir(parents=True)
    (path / "instructions").mkdir()
    manifest = """
name: fixture
version: "1.0"
description: Fixture package
author: Tester
template_engine: jinja2
smd_version: "0.1.0"
instructions:
  - instructions/LLM.md
files:
  - template: templates/backlog_item.md.j2
    target: scrum/backlog/B-001.md
"""
    (path / "manifest.yaml").write_text(manifest, encoding="utf-8")
    (path / "instructions" / "LLM.md").write_text("# LLM instructions\n", encoding="utf-8")
    (path / "templates" / "backlog_item.md.j2").write_text("# {{ project_name }}\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    unittest.main()
