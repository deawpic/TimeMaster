"""
Unit tests for the Writing & Citation Linter Engine.
Verifies detection of AI clichés, vague attributions, and citation validation.
"""

import sys
import unittest
from pathlib import Path

LINTER_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "avoid-ai-writing" / "scripts"
sys.path.insert(0, str(LINTER_DIR))

from writing_linter import lint_text, audit_path


class TestWritingLinter(unittest.TestCase):

    def test_detect_english_cliches(self):
        """Verify English AI clichés are flagged."""
        dirty_text = "Let us delve into this rich tapestry of clocks, a pivotal game-changer."
        res = lint_text(dirty_text)
        self.assertFalse(res["passed"])
        self.assertGreaterEqual(res["issues_count"], 3)
        matched_words = [issue["matched"].lower() for issue in res["issues"]]
        self.assertTrue(any("delve" in w for w in matched_words))
        self.assertTrue(any("tapestry" in w for w in matched_words))

    def test_detect_thai_cliches(self):
        """Verify Thai AI clichés are flagged."""
        dirty_thai = "ระบบนี้เป็นพยานถึงความสำคัญของการเจาะลึกและก้าวเข้าสู่การเดินทางอันยิ่งใหญ่"
        res = lint_text(dirty_thai)
        self.assertFalse(res["passed"])
        self.assertGreaterEqual(res["issues_count"], 3)
        matched_words = [issue["matched"] for issue in res["issues"]]
        self.assertIn("เป็นพยานถึง", matched_words)
        self.assertIn("เจาะลึก", matched_words)
        self.assertIn("ก้าวเข้าสู่การเดินทาง", matched_words)

    def test_detect_vague_attributions(self):
        """Verify vague ungrounded claims are caught."""
        vague_text = "As experts agree and scientists widely acknowledge, the system works. เป็นที่ทราบกันดีว่ามีความเสถียร"
        res = lint_text(vague_text)
        self.assertFalse(res["passed"])
        categories = [issue["category"] for issue in res["issues"]]
        self.assertIn("vague_attribution", categories)

    def test_clean_academic_text_passes(self):
        """Clean, grounded scholarly text with authentic citations must pass."""
        clean_text = (
            "Under IEEE 1588-2019 and IETF RFC 5905, the packet round-trip delay "
            "is evaluated symmetrically. The BIPM publishes Circular T monthly to steer "
            "UTC(k) within 100 ns relative to UTC."
        )
        res = lint_text(clean_text)
        self.assertTrue(res["passed"], f"Unexpected issues in clean text: {res['issues']}")
        self.assertEqual(res["issues_count"], 0)
        self.assertIn("IEEE 1588", res["citations_found"])
        self.assertIn("RFC 5905", res["citations_found"])
        self.assertIn("BIPM", res["citations_found"])
        self.assertIn("Circular T", res["citations_found"])

    def test_audit_path_reports_directory(self):
        """Verify auditing reports directory succeeds."""
        reports_path = Path(__file__).resolve().parent.parent / "reports"
        res = audit_path(str(reports_path))
        self.assertTrue(res["passed"])


if __name__ == "__main__":
    unittest.main()
