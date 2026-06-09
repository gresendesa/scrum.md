from pathlib import Path
import tempfile
import unittest

from smd.memory import MemoryRepository
from smd.templates import render_template, render_project_memory, write_rendered_files


class MemoryRepositoryTests(unittest.TestCase):
    def test_queries_rendered_memory_without_text_guessing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rendered_files(root, render_project_memory({"project_name": "fixture", "owner": "Tester"}))

            backlog_item = render_template(
                "default/scrum/backlog_item.md.j2",
                {
                    "item_id": "B-001",
                    "title": "First item",
                    "objective": "Make memory queryable.",
                    "criteria": ["Record is discoverable by status."],
                    "owner": "Tester",
                    "created_at": "2026-06-09",
                    "updated_at": "2026-06-09",
                    "status": "todo",
                    "po_priority": 1,
                    "risk": "medium",
                    "linked_sprint": "null",
                    "type": "implementation",
                },
            )
            item_path = root / "scrum" / "backlog" / "B-001.md"
            item_path.parent.mkdir(parents=True)
            item_path.write_text(backlog_item, encoding="utf-8")

            repo = MemoryRepository(root)

            self.assertTrue(repo.validate().ok)
            self.assertEqual(repo.next_backlog_id(), "B-002")
            self.assertEqual([item.title for item in repo.pending_backlog_items()], ["First item"])
            self.assertEqual(repo.next_decision_id(), "DEC-001")
            self.assertEqual(repo.next_experience_id(), "EXP-001")
            self.assertTrue(repo.next_sprint_id(2026).startswith("SPR-2026-"))

    def test_validation_reports_missing_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = MemoryRepository(tmp)
            result = repo.validate()

            self.assertFalse(result.ok)
            self.assertEqual(result.errors[0].code, "MISSING_REQUIRED_FILE")

    def test_validation_reports_broken_ref_and_duplicate_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rendered_files(root, render_project_memory({"project_name": "fixture", "owner": "Tester"}))

            first = root / "scrum" / "backlog" / "B-001.md"
            second = root / "scrum" / "backlog" / "B-002.md"
            first.parent.mkdir(parents=True)
            content = render_template(
                "default/scrum/backlog_item.md.j2",
                {
                    "item_id": "B-001",
                    "title": "Duplicate item",
                    "objective": "Create a duplicate section.",
                    "criteria": ["Validation detects duplicate section."],
                    "owner": "Tester",
                    "created_at": "2026-06-09",
                    "updated_at": "2026-06-09",
                    "status": "todo",
                    "po_priority": 1,
                    "risk": "medium",
                    "linked_sprint": "null",
                    "type": "implementation",
                },
            )
            first.write_text(content + "\n[@ref: Missing](missing.md#missing)\n", encoding="utf-8")
            second.write_text(content, encoding="utf-8")

            result = MemoryRepository(root).validate()
            codes = {error.code for error in result.errors}

            self.assertFalse(result.ok)
            self.assertIn("BROKEN_REF", codes)
            self.assertIn("DUPLICATE_SECTION", codes)


if __name__ == "__main__":
    unittest.main()
