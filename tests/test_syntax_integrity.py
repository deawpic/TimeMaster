"""
Test Suite for Mermaid & Markdown Syntax Validator
Verifies that syntax_validator.py correctly detects syntax errors,
unclosed blocks, unquoted special characters, and table misalignments,
and verifies that all markdown documents across TimeMaster pass 100%.
"""

import sys
import unittest
from pathlib import Path

# Add syntax_validator script directory to sys.path
SCRIPT_DIR = (
    Path(__file__).resolve().parent.parent
    / ".agents"
    / "skills"
    / "mermaid-expert"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIR))

from syntax_validator import (
    audit_markdown_content,
    audit_path,
    validate_mermaid_diagram,
    validate_markdown_tables,
    validate_code_fences,
)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class TestMermaidSyntaxValidator(unittest.TestCase):

    def test_valid_flowchart(self):
        content = """
```mermaid
flowchart TD
    A["Node A (High Precision)"] --> B["Node B"]
    B -->|Sync Packet| C["Node C"]
```
"""
        report = audit_markdown_content(content)
        self.assertTrue(report["passed"])
        self.assertEqual(report["errors_count"], 0)

    def test_unquoted_special_chars_detected(self):
        content = """
```mermaid
graph TD
    A[Stratum 0 (Cesium-133)] --> B
```
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        self.assertGreaterEqual(report["errors_count"], 1)
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("mermaid_unquoted_special_chars", categories)

    def test_unclosed_subgraph_detected(self):
        content = """
```mermaid
graph TD
    subgraph Cluster1 ["Core Infrastructure"]
        A --> B
```
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("mermaid_unclosed_subgraph", categories)

    def test_unclosed_sequence_block_detected(self):
        content = """
```mermaid
sequenceDiagram
    autonumber
    loop Hourly Calibration
        A->>B: PTP Sync
```
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("mermaid_unclosed_sequence_block", categories)

    def test_unclosed_edge_pipe_detected(self):
        content = """
```mermaid
flowchart LR
    A -->|Broken Edge Pipe B
```
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("mermaid_unclosed_edge_pipe", categories)


class TestMarkdownTableValidator(unittest.TestCase):

    def test_valid_markdown_table(self):
        content = """
| Layer | Protocol | Precision |
| :--- | :--- | :--- |
| Physical | 1PPS | 1 ns |
| Network | PTP | 100 ns |
| Application | NTP | 1 ms |
"""
        report = audit_markdown_content(content)
        self.assertTrue(report["passed"])
        self.assertEqual(report["errors_count"], 0)

    def test_row_column_mismatch_detected(self):
        content = """
| Col1 | Col2 | Col3 |
| :--- | :--- | :--- |
| Val1 | Val2 |
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("table_row_column_mismatch", categories)

    def test_separator_column_mismatch_detected(self):
        content = """
| Col1 | Col2 | Col3 |
| :--- | :--- |
| Val1 | Val2 | Val3 |
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("table_separator_column_mismatch", categories)


class TestCodeFenceValidator(unittest.TestCase):

    def test_unclosed_code_fence_detected(self):
        content = """
# Header
```python
def foo():
    return 42
"""
        report = audit_markdown_content(content)
        self.assertFalse(report["passed"])
        categories = [i["category"] for i in report["issues"]]
        self.assertIn("unclosed_code_fence", categories)


class TestWorkspaceIntegrityAudit(unittest.TestCase):

    def test_all_workspace_markdown_files_pass_syntax_validation(self):
        """Scans every Markdown file across TimeMaster to ensure zero syntax errors."""
        report = audit_path(str(WORKSPACE_ROOT))
        self.assertTrue(
            report["passed"],
            f"Workspace Markdown validation failed with {report['total_errors']} errors: {report.get('issues', [])}",
        )
        self.assertEqual(report["total_errors"], 0)
        self.assertGreaterEqual(report["files_scanned"], 15)
        self.assertGreaterEqual(report["mermaid_blocks_scanned"], 5)


if __name__ == "__main__":
    unittest.main()
