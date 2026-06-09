from pathlib import Path
import subprocess
import tempfile
import unittest

from smd.templates import render_template, render_project_memory, write_rendered_files


class TemplateRenderingTests(unittest.TestCase):
    def test_base_memory_renders_and_validates_with_mdbind(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = render_project_memory({"project_name": "fixture", "owner": "Tester"})
            write_rendered_files(root, files)

            result = subprocess.run(
                [".venv/bin/mdb", "validate", "--root", str(root), "--json"],
                cwd=Path(__file__).resolve().parents[1],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"errors": []', result.stdout)

    def test_missing_required_variable_fails(self) -> None:
        with self.assertRaises(Exception):
            render_template("default/CONSTITUTION.md.j2", {"project_name": "fixture"})


if __name__ == "__main__":
    unittest.main()
