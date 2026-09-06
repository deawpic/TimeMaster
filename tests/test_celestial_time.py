"""
Unit tests for Celestial & Relativistic Time Mechanics Engine.
Verifies calculations for Coordinated Lunar Time (LTC), Mars (MTC), and IAU coordinate clocks.
"""

import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "celestial-time-mechanics" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

from celestial_time import (
    calculate_lunar_time_dilation,
    calculate_mars_time_parameters,
    convert_coordinate_times
)


class TestCelestialTimeMechanics(unittest.TestCase):

    def test_lunar_time_dilation(self):
        """Verify lunar surface clock ticks ~ 56.0 us/day faster than Earth geoid."""
        res = calculate_lunar_time_dilation()
        self.assertTrue(res["lunar_clock_faster"], "Lunar clock must tick faster due to lower gravity")
        self.assertTrue(55.0 < res["daily_drift_us"] < 57.5,
                        f"Expected daily drift ~ 56.0 us, got: {res['daily_drift_us']}")
        self.assertAlmostEqual(res["daily_drift_us"], 56.02, delta=0.5)

    def test_mars_time_parameters(self):
        """Verify Mars Sol duration and conversion ratios."""
        res = calculate_mars_time_parameters()
        self.assertEqual(res["sol_duration_seconds"], 88775.244)
        self.assertIn("24h 39m 35", res["sol_hms"])
        self.assertAlmostEqual(res["ratio_sol_to_earth_day"], 1.02749125, places=5)

    def test_iau_coordinate_conversions(self):
        """Verify TT and TCG coordinate time relations."""
        tai_epoch = 1772841600.0  # Sample epoch
        res = convert_coordinate_times(tai_epoch)

        # TT = TAI + 32.184s
        self.assertAlmostEqual(res["tt"] - res["tai"], 32.184, places=6)
        # TCG ticks faster than TT (positive secular difference after 1977)
        self.assertGreater(res["tcg"], res["tt"])


if __name__ == "__main__":
    unittest.main()
