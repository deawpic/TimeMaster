"""
Unit tests for oscillator holdover calculation engine.
Verifies drift models, aging rates, and target divergence time solutions.
"""

import sys
import unittest
from pathlib import Path

SKILL_SCRIPT_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "oscillator-holdover-modeler" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPT_DIR))

from holdover_math import calculate_holdover_drift, max_holdover_time_for_target, OSCILLATOR_PROFILES


class TestHoldoverCalculations(unittest.TestCase):

    def test_oscillator_profiles_loaded(self):
        """Verify all expected oscillator profiles are defined."""
        expected = ["tcxo", "standard_ocxo", "double_oven_ocxo", "rubidium", "csac"]
        for osc in expected:
            self.assertIn(osc, OSCILLATOR_PROFILES)

    def test_tcxo_drift_order_of_magnitude(self):
        """TCXO should drift on the order of milliseconds over 24 hours."""
        res = calculate_holdover_drift("tcxo", 86400.0)
        drift_ms = res["total_drift_us"] / 1000.0
        self.assertTrue(1.0 < drift_ms < 100.0, f"TCXO drift unexpected: {drift_ms} ms")

    def test_ocxo_drift_order_of_magnitude(self):
        """Standard OCXO should drift ~ 5 to 20 us over 24 hours."""
        res = calculate_holdover_drift("standard_ocxo", 86400.0)
        drift_us = res["total_drift_us"]
        self.assertTrue(2.0 < drift_us < 30.0, f"Standard OCXO drift unexpected: {drift_us} us")

    def test_double_oven_ocxo_drift(self):
        """Double-oven OCXO should achieve ~ 1 us/day holdover."""
        res = calculate_holdover_drift("double_oven_ocxo", 86400.0)
        drift_us = res["total_drift_us"]
        self.assertTrue(0.5 < drift_us < 5.0, f"Double-oven OCXO drift unexpected: {drift_us} us")

    def test_rubidium_drift(self):
        """Rubidium should drift well under 1 us over 24 hours."""
        res = calculate_holdover_drift("rubidium", 86400.0)
        drift_us = res["total_drift_us"]
        self.assertTrue(0.05 < drift_us < 1.0, f"Rubidium drift unexpected: {drift_us} us")

    def test_max_holdover_time_for_target(self):
        """Verify solving for max holdover time for 100 us MiFID II target."""
        res_ocxo = max_holdover_time_for_target("standard_ocxo", 100.0)
        self.assertGreater(res_ocxo["max_holdover_hours"], 24.0, "Standard OCXO should hold 100 us for > 24h")

        res_docxo = max_holdover_time_for_target("double_oven_ocxo", 1.5)
        self.assertGreater(res_docxo["max_holdover_hours"], 10.0, "Double-oven OCXO should hold 1.5 us for > 10h")

    def test_invalid_oscillator_raises(self):
        """Invalid oscillator identifier should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_holdover_drift("invalid_oscillator", 3600.0)


if __name__ == "__main__":
    unittest.main()
