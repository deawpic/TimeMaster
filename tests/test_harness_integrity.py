"""
Harness Integrity Test Suite for TimeMaster
Verifies that all skills, knowledge base files, and configurations meet quality standards.
Compatible with standard library unittest and pytest.
"""

import unittest
from pathlib import Path

TIMEMASTER_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_SKILLS = [
    "scientific-writing",
    "avoid-ai-writing",
    "mermaid-expert",
    "papers-skill",
    "verify-citations",
    "sympy-time-mechanics",
    "technical-tutorials",
    "docs-architect",
    "code-documentation-code-explain",
    "regulatory-timing-audit",
    "linux-timing-diagnostics",
    "oscillator-holdover-modeler",
    "gnss-security-auditor",
    "celestial-time-mechanics",
    "noaacalc"
]


class TestHarnessIntegrity(unittest.TestCase):

    def test_root_files_exist(self):
        """Verify primary harness documentation and agent specifications exist."""
        self.assertTrue((TIMEMASTER_ROOT / "AGENTS.md").exists(), "Root AGENTS.md missing")
        self.assertTrue((TIMEMASTER_ROOT / ".agents" / "AGENTS.md").exists(), ".agents/AGENTS.md mirror missing")
        self.assertTrue((TIMEMASTER_ROOT / "README.md").exists(), "README.md missing")

        agents_root = (TIMEMASTER_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        agents_mirror = (TIMEMASTER_ROOT / ".agents" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(agents_root, agents_mirror, "AGENTS.md and .agents/AGENTS.md must be identical mirrors")

    def test_knowledge_base_files(self):
        """Verify that both foundational knowledge base documents exist and are populated."""
        kb_dir = TIMEMASTER_ROOT / "kb"
        self.assertTrue(kb_dir.exists(), "kb directory missing")

        dim11_file = kb_dir / "global_time_standard_11_dimensions.md"
        stack_file = kb_dir / "Global_time_stack.md"

        self.assertTrue(dim11_file.exists(), "global_time_standard_11_dimensions.md missing")
        self.assertGreater(dim11_file.stat().st_size, 10000, "11 dimensions file suspiciously small")

        self.assertTrue(stack_file.exists(), "Global_time_stack.md missing")
        self.assertGreater(stack_file.stat().st_size, 100000, "Global time stack handbook suspiciously small")

    def test_all_curated_skills_exist(self):
        """Verify all curated skills exist with valid SKILL.md and YAML frontmatter."""
        skills_dir = TIMEMASTER_ROOT / ".agents" / "skills"
        self.assertTrue(skills_dir.exists(), ".agents/skills directory missing")

        for skill_name in EXPECTED_SKILLS:
            skill_path = skills_dir / skill_name
            self.assertTrue(skill_path.exists(), f"Skill directory '{skill_name}' missing")

            skill_md = skill_path / "SKILL.md"
            self.assertTrue(skill_md.exists(), f"SKILL.md for '{skill_name}' missing")

            content = skill_md.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"SKILL.md for '{skill_name}' missing frontmatter start")
            self.assertIn("name:", content, f"SKILL.md for '{skill_name}' missing 'name' attribute")
            self.assertIn("description:", content, f"SKILL.md for '{skill_name}' missing 'description' attribute")

    def test_bundled_scripts_exist(self):
        """Verify bundled CLI scripts exist."""
        papers_script = TIMEMASTER_ROOT / ".agents" / "skills" / "papers-skill" / "scripts" / "papers.py"
        time_math_script = TIMEMASTER_ROOT / ".agents" / "skills" / "sympy-time-mechanics" / "scripts" / "time_math.py"
        holdover_math_script = TIMEMASTER_ROOT / ".agents" / "skills" / "oscillator-holdover-modeler" / "scripts" / "holdover_math.py"
        writing_linter_script = TIMEMASTER_ROOT / ".agents" / "skills" / "avoid-ai-writing" / "scripts" / "writing_linter.py"
        celestial_time_script = TIMEMASTER_ROOT / ".agents" / "skills" / "celestial-time-mechanics" / "scripts" / "celestial_time.py"
        noaacalc_script = TIMEMASTER_ROOT / ".agents" / "skills" / "noaacalc" / "scripts" / "noaacalc.py"

        self.assertTrue(papers_script.exists(), "papers.py script missing")
        self.assertTrue(time_math_script.exists(), "time_math.py script missing")
        self.assertTrue(holdover_math_script.exists(), "holdover_math.py script missing")
        self.assertTrue(writing_linter_script.exists(), "writing_linter.py script missing")
        self.assertTrue(celestial_time_script.exists(), "celestial_time.py script missing")
        self.assertTrue(noaacalc_script.exists(), "noaacalc.py script missing")


if __name__ == "__main__":
    unittest.main()
