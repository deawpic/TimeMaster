#!/usr/bin/env python3
"""
NOAA Solar Calculator Engine
Implements the exact 12-step Jean Meeus astronomical algorithm from NOAAcalc.html.
Standard library only (math, datetime, argparse, json).
"""

import math
import argparse
import datetime
import json
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any

D2R = math.pi / 180.0
R2D = 180.0 / math.pi


def sin_d(d: float) -> float:
    return math.sin(d * D2R)


def cos_d(d: float) -> float:
    return math.cos(d * D2R)


def tan_d(d: float) -> float:
    return math.tan(d * D2R)


def asin_d(x: float) -> float:
    clamped = max(-1.0, min(1.0, x))
    return math.asin(clamped) * R2D


def acos_d(x: float) -> float:
    clamped = max(-1.0, min(1.0, x))
    return math.acos(clamped) * R2D


def mod360(x: float) -> float:
    return ((x % 360.0) + 360.0) % 360.0


def julian_day(year: int, month: int, day: int) -> float:
    """
    Step 1: Calculate Julian Day at 00:00 UT
    Exact formula from NOAAcalc.html julianDay(y, m, d)
    """
    y = year
    m = month
    d = day
    if m <= 2:
        y -= 1
        m += 12
    a = math.floor(y / 100)
    b = 2 - a + math.floor(a / 4)
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5


@dataclass
class SolarResult:
    latitude: float
    longitude: float
    timezone_offset: float
    year: int
    month: int
    day: int

    # 12 steps
    jd_noon: float
    t: float
    l0: float
    m0: float
    ec: float
    c: float
    tl: float
    om: float
    lam: float
    eps: float
    dec: float
    yv: float
    eot: float
    solar_noon: float
    hour_angle: Optional[float]
    sunrise: Optional[float]
    sunset: Optional[float]
    civil_dawn: Optional[float]
    civil_dusk: Optional[float]
    nautical_dawn: Optional[float]
    nautical_dusk: Optional[float]
    astronomical_dawn: Optional[float]
    astronomical_dusk: Optional[float]
    azimuth_rise: Optional[float]
    azimuth_set: Optional[float]
    day_length: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone_offset": self.timezone_offset,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "julian_day_noon": self.jd_noon,
            "julian_century": self.t,
            "geom_mean_long_deg": self.l0,
            "geom_mean_anom_deg": self.m0,
            "eccentricity": self.ec,
            "eq_of_center_deg": self.c,
            "true_long_deg": self.tl,
            "apparent_long_deg": self.lam,
            "obliquity_deg": self.eps,
            "solar_declination_deg": self.dec,
            "equation_of_time_min": self.eot,
            "solar_noon_min": self.solar_noon,
            "hour_angle_deg": self.hour_angle,
            "sunrise_min": self.sunrise,
            "sunset_min": self.sunset,
            "day_length_min": self.day_length,
            "azimuth_rise_deg": self.azimuth_rise,
            "azimuth_set_deg": self.azimuth_set,
            "civil_dawn_min": self.civil_dawn,
            "civil_dusk_min": self.civil_dusk,
            "nautical_dawn_min": self.nautical_dawn,
            "nautical_dusk_min": self.nautical_dusk,
            "astronomical_dawn_min": self.astronomical_dawn,
            "astronomical_dusk_min": self.astronomical_dusk,
            "formatted": {
                "sunrise": minutes_to_hms(self.sunrise),
                "sunset": minutes_to_hms(self.sunset),
                "solar_noon": minutes_to_hms(self.solar_noon),
                "sunrise_hm": minutes_to_hm(self.sunrise),
                "sunset_hm": minutes_to_hm(self.sunset),
                "solar_noon_hm": minutes_to_hm(self.solar_noon),
                "day_length": minutes_to_duration_th(self.day_length),
                "civil_dawn": minutes_to_hms(self.civil_dawn),
                "civil_dusk": minutes_to_hms(self.civil_dusk),
                "nautical_dawn": minutes_to_hms(self.nautical_dawn),
                "nautical_dusk": minutes_to_hms(self.nautical_dusk),
                "astronomical_dawn": minutes_to_hms(self.astronomical_dawn),
                "astronomical_dusk": minutes_to_hms(self.astronomical_dusk),
            }
        }


def calculate_solar(lat: float, lon: float, tz: float, year: int, month: int, day: int) -> SolarResult:
    """
    Steps 1 to 12 matching NOAAcalc.html solar(lat, lon, tz, Y, M, D) exactly.
    """
    # 1) Julian Day at local solar noon
    jd = julian_day(year, month, day) + (12.0 - tz) / 24.0

    # 2) Julian Century
    t = (jd - 2451545.0) / 36525.0

    # 3) Geometric Mean Longitude
    l0 = mod360(280.46646 + t * (36000.76983 + t * 0.0003032))

    # 4) Geometric Mean Anomaly
    m0 = 357.52911 + t * (35999.05029 - 0.0001537 * t)

    # 5) Eccentricity
    ec = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)

    # 6) Equation of Center
    c = (
        sin_d(m0) * (1.914602 - t * (0.004817 + 0.000014 * t))
        + sin_d(2.0 * m0) * (0.019993 - 0.000101 * t)
        + sin_d(3.0 * m0) * 0.000289
    )

    # 7) True Longitude
    tl = l0 + c

    # 8) Apparent Longitude
    om = 125.04 - 1934.136 * t
    lam = tl - 0.00569 - 0.00478 * sin_d(om)

    # 9) Obliquity of Ecliptic
    e0 = 23.0 + (26.0 + ((21.448 - t * (46.815 + t * (0.00059 - t * 0.001813)))) / 60.0) / 60.0
    eps = e0 + 0.00256 * cos_d(om)

    # 10) Solar Declination
    dec = asin_d(sin_d(eps) * sin_d(lam))

    # 11) Equation of Time
    yv = math.pow(tan_d(eps / 2.0), 2)
    eot = 4.0 * R2D * (
        yv * sin_d(2.0 * l0)
        - 2.0 * ec * sin_d(m0)
        + 4.0 * ec * yv * sin_d(m0) * cos_d(2.0 * l0)
        - 0.5 * yv * yv * sin_d(4.0 * l0)
        - 1.25 * ec * ec * sin_d(2.0 * m0)
    )

    # Solar noon in minutes from local midnight
    noon = 720.0 - 4.0 * lon - eot + tz * 60.0

    # 12) Hour angle for given zenith angle
    def ha(z: float) -> Optional[float]:
        cos_den = cos_d(lat) * cos_d(dec)
        if abs(cos_den) < 1e-12:
            return None
        cos_ha = cos_d(z) / cos_den - tan_d(lat) * tan_d(dec)
        if cos_ha > 1.0 or cos_ha < -1.0:
            return None
        return acos_d(cos_ha)

    def pair(z: float) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        h = ha(z)
        if h is None:
            return None, None, None
        return noon - 4.0 * h, noon + 4.0 * h, h

    rise, set_, h_val = pair(90.833)
    cv_a, cv_b, _ = pair(96.0)
    nt_a, nt_b, _ = pair(102.0)
    as_a, as_b, _ = pair(108.0)

    # Azimuth at rise/set
    az_r: Optional[float] = None
    az_s: Optional[float] = None
    if rise is not None:
        h_alt = -0.833
        den = cos_d(lat) * cos_d(h_alt)
        if abs(den) > 1e-12:
            cos_az = (sin_d(dec) - sin_d(lat) * sin_d(h_alt)) / den
            cos_az = max(-1.0, min(1.0, cos_az))
            az_r = acos_d(cos_az)
            az_s = 360.0 - az_r

    day_len = None if rise is None or set_ is None else (set_ - rise)

    return SolarResult(
        latitude=lat,
        longitude=lon,
        timezone_offset=tz,
        year=year,
        month=month,
        day=day,
        jd_noon=jd,
        t=t,
        l0=l0,
        m0=m0,
        ec=ec,
        c=c,
        tl=tl,
        om=om,
        lam=lam,
        eps=eps,
        dec=dec,
        yv=yv,
        eot=eot,
        solar_noon=noon,
        hour_angle=h_val,
        sunrise=rise,
        sunset=set_,
        civil_dawn=cv_a,
        civil_dusk=cv_b,
        nautical_dawn=nt_a,
        nautical_dusk=nt_b,
        astronomical_dawn=as_a,
        astronomical_dusk=as_b,
        azimuth_rise=az_r,
        azimuth_set=az_s,
        day_length=day_len
    )


def minutes_to_hms(minutes: Optional[float]) -> str:
    """Format minutes from midnight to HH:MM:SS with exact NOAAcalc.html rounding logic."""
    if minutes is None or math.isnan(minutes):
        return "—"
    m = ((minutes % 1440.0) + 1440.0) % 1440.0
    h = int(m // 60)
    mi = int(m % 60)
    s = round(((m % 60) - mi) * 60)
    if s >= 60:
        s = 59
    return f"{h:02d}:{mi:02d}:{s:02d}"


def minutes_to_hm(minutes: Optional[float]) -> str:
    """Format minutes from midnight to HH:MM."""
    full = minutes_to_hms(minutes)
    if full == "—":
        return "—"
    return full[:5]


def minutes_to_duration_th(minutes: Optional[float]) -> str:
    """Format duration in Thai: X ชม. Y นาที matching dur(min) in NOAAcalc.html."""
    if minutes is None or math.isnan(minutes):
        return "—"
    h = int(minutes // 60)
    mi = round(minutes % 60)
    return f"{h} ชม. {mi} นาที"


def run_benchmark():
    """Verify against NOAAcalc.html ground-truth reference values (Ban Pong, 2022-03-27)."""
    # Ban Pong, Ratchaburi: 13.8199 N, 99.8722 E, TZ +7, 27 March 2022
    res = calculate_solar(13.8199, 99.8722, 7.0, 2022, 3, 27)

    assert minutes_to_hms(res.sunrise) == "06:19:58", f"Sunrise mismatch: {minutes_to_hms(res.sunrise)}"
    assert minutes_to_hms(res.sunset) == "18:31:55", f"Sunset mismatch: {minutes_to_hms(res.sunset)}"
    assert minutes_to_hms(res.solar_noon) == "12:25:57", f"Solar noon mismatch: {minutes_to_hms(res.solar_noon)}"
    assert minutes_to_duration_th(res.day_length) == "12 ชม. 12 นาที", f"Day length mismatch: {minutes_to_duration_th(res.day_length)}"
    assert round(res.dec, 3) == 2.584, f"Declination mismatch: {res.dec}"
    assert round(res.eot, 2) == -5.43, f"EoT mismatch: {res.eot}"
    print("NOAAcalc benchmark verification passed: 100% exact match with NOAAcalc.html reference.")


def main():
    parser = argparse.ArgumentParser(description="NOAA Solar Calculator Engine (Jean Meeus algorithm)")
    parser.add_argument("--lat", type=float, default=13.8199, help="Latitude (degrees N +)")
    parser.add_argument("--lon", type=float, default=99.8722, help="Longitude (degrees E +)")
    parser.add_argument("--tz", type=float, default=7.0, help="UTC timezone offset")
    parser.add_argument("--date", type=str, default="2022-03-27", help="Date in YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--benchmark", action="store_true", help="Run ground truth verification benchmark")

    args = parser.parse_args()

    if args.benchmark:
        run_benchmark()
        return

    year, month, day = map(int, args.date.split("-"))
    res = calculate_solar(args.lat, args.lon, args.tz, year, month, day)

    if args.json:
        print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"NOAA Solar Calculation: {args.lat:.4f}°, {args.lon:.4f}° | Date: {args.date} | TZ: UTC+{args.tz:g}")
        print(f"Sunrise:            {minutes_to_hms(res.sunrise)} (HM: {minutes_to_hm(res.sunrise)})")
        print(f"Sunset:             {minutes_to_hms(res.sunset)} (HM: {minutes_to_hm(res.sunset)})")
        print(f"Solar Noon:         {minutes_to_hms(res.solar_noon)}")
        print(f"Day Length:         {minutes_to_duration_th(res.day_length)}")
        print(f"Civil Twilight:     {minutes_to_hms(res.civil_dawn)} - {minutes_to_hms(res.civil_dusk)}")
        print(f"Nautical Twilight:  {minutes_to_hms(res.nautical_dawn)} - {minutes_to_hms(res.nautical_dusk)}")
        print(f"Astronomical Twil.: {minutes_to_hms(res.astronomical_dawn)} - {minutes_to_hms(res.astronomical_dusk)}")
        print(f"Declination (δ):    {res.dec:+.4f}°")
        print(f"Equation of Time:   {res.eot:+.3f} min")


if __name__ == "__main__":
    main()
