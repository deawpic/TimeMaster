"""
Time Calculations Test Suite for TimeMaster
Verifies that all relativistic, packet timing, and chronometric formulas match ground-truth physics.
Compatible with standard library unittest and pytest.
"""

import sys
import math
import unittest
from pathlib import Path

# Add sympy-time-mechanics script path to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "sympy-time-mechanics" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from time_math import (
    calculate_gps_relativistic_effects,
    calculate_ntp_packet_math,
    calculate_allan_deviation,
    calculate_y2038_overflow_epoch
)


class TestTimeCalculations(unittest.TestCase):

    def test_gps_relativistic_effects(self):
        """Verify GPS satellite relativistic calculations match physical measurements."""
        res = calculate_gps_relativistic_effects()

        # Special relativity: satellite moves fast -> clock runs slower (-7.2 us/day)
        self.assertTrue(-7.5 < res["special_relativity_daily_us"] < -7.0,
                        f"Special relativity drift unexpected: {res['special_relativity_daily_us']}")

        # General relativity: higher gravitational potential -> clock runs faster (+45.7 us/day)
        self.assertTrue(45.0 < res["general_relativity_daily_us"] < 46.5,
                        f"General relativity drift unexpected: {res['general_relativity_daily_us']}")

        # Net drift: +38.44 us/day
        self.assertTrue(38.0 < res["net_daily_drift_us"] < 39.0,
                        f"Net daily drift unexpected: {res['net_daily_drift_us']}")

        # Steered oscillator frequency: factory adjusted to ~ 10.2299999954 MHz
        self.assertTrue(abs(res["steered_frequency_hz"] - 10229999.9954) < 0.01,
                        f"Steered frequency unexpected: {res['steered_frequency_hz']}")

        # Uncorrected position error: ~ 11.5 km/day
        self.assertTrue(11.0 < res["position_error_per_day_km"] < 12.0,
                        f"Position error unexpected: {res['position_error_per_day_km']}")

    def test_ntp_packet_math(self):
        """Verify NTP 4-timestamp offset and delay equations."""
        # Scenario: 10ms forward delay, 10ms return delay, +5ms server clock ahead
        t1 = 100.000  # Client send (client clock: 100.000)
        t2 = 100.015  # Server receive (server clock: 100.010 real + 0.005 offset = 100.015)
        t3 = 100.020  # Server send after 5ms processing (server clock: 100.020)
        t4 = 100.025  # Client receive (client clock: 100.015 real + 0.010 return = 100.025)

        res = calculate_ntp_packet_math(t1, t2, t3, t4)
        self.assertTrue(math.isclose(res["round_trip_delay"], 0.020, rel_tol=1e-4),
                        f"Round trip delay unexpected: {res['round_trip_delay']}")
        self.assertTrue(math.isclose(res["clock_offset"], 0.005, rel_tol=1e-4),
                        f"Clock offset unexpected: {res['clock_offset']}")
        self.assertTrue(res["symmetric_assumption_valid"])

    def test_allan_deviation(self):
        """Verify Allan deviation computation from frequency samples."""
        # Constant frequency series should yield zero Allan deviation
        constant_series = [1.0, 1.0, 1.0, 1.0, 1.0]
        res_const = calculate_allan_deviation(constant_series)
        self.assertEqual(res_const["allan_deviation"], 0.0)

        # Series with variations
        varying_series = [1.0, 1.0000001, 0.9999999, 1.0000002]
        res_var = calculate_allan_deviation(varying_series)
        self.assertGreater(res_var["allan_deviation"], 0.0)
        self.assertEqual(res_var["sample_count"], 4)

    def test_y2038_overflow(self):
        """Verify Unix 32-bit epoch overflow boundary parameters."""
        res = calculate_y2038_overflow_epoch()
        self.assertEqual(res["max_32bit_signed_int"], 2147483647)
        self.assertEqual(res["overflow_utc_string"], "2038-01-19 03:14:07 UTC")
        self.assertEqual(res["post_overflow_year"], 1901)
        self.assertGreater(res["years_covered_by_64bit"], 2.9e11)


if __name__ == "__main__":
    unittest.main()
