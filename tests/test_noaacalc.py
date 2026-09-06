"""
Test Suite for NOAA Solar Calculator Engine
Validates the 12-step Jean Meeus astronomical algorithms against NOAAcalc.html ground truth.
"""

import unittest
from pathlib import Path
import sys

# Add script directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "noaacalc" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from noaacalc import calculate_solar, julian_day, minutes_to_hms, minutes_to_hm, minutes_to_duration_th


class TestNOAASolarCalculator(unittest.TestCase):

    def test_julian_day_calculation(self):
        """Verify Julian Day calculation matches Jean Meeus formula."""
        # 2000-01-01 12:00 UT is JD 2451545.0
        # 00:00 UT is JD 2451544.5
        jd_2000 = julian_day(2000, 1, 1)
        self.assertAlmostEqual(jd_2000, 2451544.5, places=1)

    def test_ban_pong_ground_truth(self):
        """
        Test reference case from NOAAcalc.html line 153:
        Ban Pong, Ratchaburi (13.8199 N, 99.8722 E, UTC+7) on 27 March 2022.
        """
        res = calculate_solar(13.8199, 99.8722, 7.0, 2022, 3, 27)

        # Sunrise: 06:19:58 (06:19 or 06:20)
        self.assertEqual(minutes_to_hms(res.sunrise), "06:19:58")
        self.assertEqual(minutes_to_hm(res.sunrise), "06:19")

        # Sunset: 18:31:55 (18:31 or 18:32)
        self.assertEqual(minutes_to_hms(res.sunset), "18:31:55")
        self.assertEqual(minutes_to_hm(res.sunset), "18:31")

        # Solar Noon: 12:25:57
        self.assertEqual(minutes_to_hms(res.solar_noon), "12:25:57")
        self.assertEqual(minutes_to_hm(res.solar_noon), "12:25")

        # Day length: 12 ชม. 12 นาที
        self.assertEqual(minutes_to_duration_th(res.day_length), "12 ชม. 12 นาที")

        # Astronomical parameters
        self.assertAlmostEqual(res.dec, 2.5842, places=3)
        self.assertAlmostEqual(res.eot, -5.4309, places=2)

    def test_twilight_calculations(self):
        """Verify civil, nautical, and astronomical twilights order and presence."""
        res = calculate_solar(13.8199, 99.8722, 7.0, 2022, 3, 27)

        # Dawn order: Astronomical < Nautical < Civil < Sunrise
        self.assertLess(res.astronomical_dawn, res.nautical_dawn)
        self.assertLess(res.nautical_dawn, res.civil_dawn)
        self.assertLess(res.civil_dawn, res.sunrise)

        # Dusk order: Sunset < Civil < Nautical < Astronomical
        self.assertLess(res.sunset, res.civil_dusk)
        self.assertLess(res.civil_dusk, res.nautical_dusk)
        self.assertLess(res.nautical_dusk, res.astronomical_dusk)

    def test_solar_azimuth(self):
        """Verify solar azimuth angles at sunrise and sunset."""
        res = calculate_solar(13.8199, 99.8722, 7.0, 2022, 3, 27)

        # Azimuth at rise in East quadrant (~87.13°)
        self.assertAlmostEqual(res.azimuth_rise, 87.13, places=1)
        # Azimuth at set in West quadrant (~272.87°)
        self.assertAlmostEqual(res.azimuth_set, 272.87, places=1)
        # Complementary symmetry: az_rise + az_set == 360°
        self.assertAlmostEqual(res.azimuth_rise + res.azimuth_set, 360.0, places=4)


if __name__ == "__main__":
    unittest.main()
