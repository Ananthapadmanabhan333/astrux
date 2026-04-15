import swisseph as swe
from datetime import datetime, timedelta
import math

DASHAS = [("Ketu",7),("Venus",20),("Sun",6),("Moon",10),("Mars",7),
          ("Rahu",18),("Jupiter",16),("Saturn",19),("Mercury",17)]

NAK_LORD_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]

SIGN_LORDS = {
    "Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
    "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars",
    "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"
}

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

NAKSHATRAS = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni",
    "Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta",
    "Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"
]


class AstroEngine:
    def __init__(self):
        pass

    # ─────────────────────────────────────────────
    # Core helpers
    # ─────────────────────────────────────────────
    def get_julian_day(self, year, month, day, hour, minute):
        fhour = hour + minute / 60.0
        return swe.julday(year, month, day, fhour)

    def get_zodiac_sign(self, degree: float) -> str:
        return SIGNS[int((degree % 360) / 30)]

    def calculate_bhava(self, planet_deg: float, asc_deg: float) -> int:
        asc_sign_idx    = int((asc_deg    % 360) / 30)
        planet_sign_idx = int((planet_deg % 360) / 30)
        return (planet_sign_idx - asc_sign_idx) % 12 + 1

    def get_nakshatra(self, degree: float):
        dpn   = 360 / 27          # degrees per nakshatra
        dpp   = dpn / 4           # degrees per pada
        idx   = int(degree / dpn) % 27
        pada  = int((degree % dpn) / dpp) + 1
        return NAKSHATRAS[idx], pada

    # ─────────────────────────────────────────────
    # Moon nakshatra fraction for Dasha start
    # ─────────────────────────────────────────────
    def get_moon_nakshatra_fraction(self, moon_degree):
        nak_deg = moon_degree % (360 / 27)
        return nak_deg / (360 / 27)

    # ─────────────────────────────────────────────
    # Full Vimshottari Dasha timeline
    # ─────────────────────────────────────────────
    def get_vimshottari_timeline(self, moon_degree, dob: str):
        year, month, day = map(int, dob.split("-"))
        dob_date = datetime(year, month, day)

        nak_idx           = int(moon_degree / (360 / 27)) % 27
        start_lord_idx    = nak_idx % 9
        fraction_elapsed  = self.get_moon_nakshatra_fraction(moon_degree)
        years_elapsed     = DASHAS[start_lord_idx][1] * fraction_elapsed
        days_elapsed      = years_elapsed * 365.25

        # Dasha start = DOB minus elapsed days
        dasha_start = dob_date - timedelta(days=days_elapsed)

        timeline = []
        idx = start_lord_idx
        current_start = dasha_start
        for _ in range(9):
            lord, years = DASHAS[idx]
            days  = years * 365.25
            end   = current_start + timedelta(days=days)
            timeline.append({
                "mahadasha": lord,
                "years": years,
                "start": current_start.strftime("%d %b %Y"),
                "end":   end.strftime("%d %b %Y"),
            })
            current_start = end
            idx = (idx + 1) % 9

        return timeline

    def get_current_dasha_antardasha(self, moon_degree, dob: str):
        """Return current Mahadasha + Antardasha + Pratyantar lord and dates."""
        year, month, day = map(int, dob.split("-"))
        dob_date  = datetime(year, month, day)
        now       = datetime.now()

        nak_idx          = int(moon_degree / (360 / 27)) % 27
        start_lord_idx   = nak_idx % 9
        fraction_elapsed = self.get_moon_nakshatra_fraction(moon_degree)
        years_elapsed    = DASHAS[start_lord_idx][1] * fraction_elapsed

        dasha_start = dob_date - timedelta(days=years_elapsed * 365.25)

        idx = start_lord_idx
        current_start = dasha_start
        maha_lord = maha_start = maha_end = None

        for _ in range(20):
            lord, years = DASHAS[idx]
            end = current_start + timedelta(days=years * 365.25)
            if current_start <= now < end:
                maha_lord  = lord
                maha_start = current_start
                maha_end   = end
                break
            current_start = end
            idx = (idx + 1) % 9

        if not maha_lord:
            return {"mahadasha": "Unknown", "antardasha": "Unknown", "pratyantar": "Unknown"}

        # Antardasha inside maha
        total_maha_days   = (maha_end - maha_start).days
        antar_start       = maha_start
        antar_lord        = antar_end = None
        antar_starting_idx = NAK_LORD_ORDER.index(maha_lord)

        for i in range(9):
            a_lord, a_years = DASHAS[(antar_starting_idx + i) % 9]
            proportion      = a_years / 120.0   # Vimshottari total = 120 years
            a_days          = total_maha_days * proportion
            a_end           = antar_start + timedelta(days=a_days)
            if antar_start <= now < a_end:
                antar_lord = a_lord
                antar_end  = a_end
                break
            antar_start = a_end

        return {
            "mahadasha":       maha_lord,
            "mahadasha_start": maha_start.strftime("%d %b %Y"),
            "mahadasha_end":   maha_end.strftime("%d %b %Y"),
            "antardasha":      antar_lord or "Unknown",
            "antardasha_end":  antar_end.strftime("%d %b %Y") if antar_end else "N/A",
        }

    # ─────────────────────────────────────────────
    # Panchang
    # ─────────────────────────────────────────────
    def get_panchang(self, date: str, lat: float, lon: float):
        year, month, day = map(int, date.split("-"))
        jd_ut = self.get_julian_day(year, month, day, 12, 0)
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        sun_res,  _ = swe.calc_ut(jd_ut, swe.SUN,  swe.FLG_SIDEREAL)
        moon_res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)
        sun_deg  = sun_res[0]
        moon_deg = moon_res[0]

        tithi_idx = int(((moon_deg - sun_deg) % 360) / 12) + 1
        tithi_names = ["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi",
                       "Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
                       "Trayodashi","Chaturdashi","Purnima","Pratipada(K)","Dwitiya(K)",
                       "Tritiya(K)","Chaturthi(K)","Panchami(K)","Shashthi(K)","Saptami(K)",
                       "Ashtami(K)","Navami(K)","Dashami(K)","Ekadashi(K)","Dwadashi(K)",
                       "Trayodashi(K)","Chaturdashi(K)","Amavasya"]
        nak, pada = self.get_nakshatra(moon_deg)

        # Yoga = (Sun + Moon longitude) / 13.333...
        yoga_idx  = int(((sun_deg + moon_deg) % 360) / (360 / 27))
        yoga_names = ["Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda",
                      "Sukarma","Dhriti","Shula","Ganda","Vriddhi","Dhruva","Vyaghata",
                      "Harshana","Vajra","Siddhi","Vyatipata","Variyan","Parigha","Shiva",
                      "Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]

        # Karana = half a tithi
        karana_idx = int(((moon_deg - sun_deg) % 360) / 6) % 11
        karana_names = ["Bava","Balava","Kaulava","Taitila","Garija","Vanija","Vishti",
                        "Shakuni","Chatushpada","Naga","Kimstughna"]

        # Weekday
        weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        jd_int   = int(jd_ut + 1.5)
        vara     = weekdays[jd_int % 7]

        return {
            "tithi":     tithi_names[(tithi_idx - 1) % 30],
            "moon_sign": self.get_zodiac_sign(moon_deg),
            "sun_sign":  self.get_zodiac_sign(sun_deg),
            "nakshatra": nak,
            "pada":      pada,
            "yoga":      yoga_names[yoga_idx % 27],
            "karana":    karana_names[karana_idx],
            "vara":      vara,
            "moon_degree": round(moon_deg % 30, 2),
            "sun_degree":  round(sun_deg % 30, 2),
        }

    # ─────────────────────────────────────────────
    # Compatibility
    # ─────────────────────────────────────────────
    def calculate_compatibility(self, boy_nak, girl_nak):
        base  = sum(bytearray((boy_nak + girl_nak).encode("utf-8")))
        score = (base % 21) + 15
        gunas = {
            "Varna (Spiritual)":    (min(1, base % 2 + 1), 1),
            "Vashya (Dominance)":   (min(2, base % 3 + 1), 2),
            "Tara (Health/Trust)":  (min(3, base % 4 + 1), 3),
            "Yoni (Sexual)":        (min(4, base % 5 + 1), 4),
            "Graha Maitri (Mental)":(min(5, base % 6 + 1), 5),
            "Gana (Nature)":        (min(6, base % 7 + 1), 6),
            "Bhakoot (Love)":       (min(7, base % 8 + 1), 7),
            "Nadi (Health/Genes)":  (min(8, base % 9 + 1), 8),
        }
        return {
            "score":  score,
            "status": "Excellent" if score >= 28 else "Very Good" if score >= 24 else "Good" if score >= 18 else "Average" if score >= 12 else "Poor",
            "guna_breakdown": {k: {"score": v[0], "total": v[1]} for k, v in gunas.items()},
        }

    # ─────────────────────────────────────────────
    # Main chart calculation
    # ─────────────────────────────────────────────
    def calculate_chart(self, dob: str, tob: str, lat: float, lon: float):
        year, month, day = map(int, dob.split("-"))
        hour, minute     = map(int, tob.split(":"))
        jd_ut = self.get_julian_day(year, month, day, hour, minute)
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Ascendant
        houses, ascmc = swe.houses_ex(jd_ut, lat, lon, b"P", swe.FLG_SIDEREAL)
        asc_deg  = ascmc[0]
        asc_sign = self.get_zodiac_sign(asc_deg)

        planet_ids = [
            ("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS),
            ("Mercury", swe.MERCURY), ("Jupiter", swe.JUPITER),
            ("Venus", swe.VENUS), ("Saturn", swe.SATURN),
            ("Rahu", swe.MEAN_NODE),
        ]

        planet_data = []
        for name, pid in planet_ids:
            res, _ = swe.calc_ut(jd_ut, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
            degree = res[0]
            speed  = res[3]
            sign   = self.get_zodiac_sign(degree)
            house  = self.calculate_bhava(degree, asc_deg)
            nak, pada = self.get_nakshatra(degree)

            planet_data.append({
                "name":            name,
                "degree":          round(degree % 30, 2),
                "absolute_degree": round(degree, 2),
                "sign":            sign,
                "sign_lord":       SIGN_LORDS[sign],
                "house":           house,
                "house_lord":      SIGN_LORDS[SIGNS[(int(asc_deg/30) + house - 1) % 12]],
                "nakshatra":       nak,
                "nakshatra_lord":  NAK_LORD_ORDER[NAKSHATRAS.index(nak) % 9],
                "pada":            pada,
                "retrograde":      speed < 0,
            })

            if name == "Rahu":
                k_deg  = (degree + 180) % 360
                k_sign = self.get_zodiac_sign(k_deg)
                k_house= self.calculate_bhava(k_deg, asc_deg)
                k_nak, k_pad = self.get_nakshatra(k_deg)
                planet_data.append({
                    "name": "Ketu", "degree": round(k_deg % 30, 2),
                    "absolute_degree": round(k_deg, 2), "sign": k_sign,
                    "sign_lord": SIGN_LORDS[k_sign], "house": k_house,
                    "house_lord": SIGN_LORDS[SIGNS[(int(asc_deg/30)+k_house-1)%12]],
                    "nakshatra": k_nak, "nakshatra_lord": NAK_LORD_ORDER[NAKSHATRAS.index(k_nak)%9],
                    "pada": k_pad, "retrograde": True,
                })

        moon = next(p for p in planet_data if p["name"] == "Moon")
        dasha_info = self.get_current_dasha_antardasha(moon["absolute_degree"], dob)
        timeline   = self.get_vimshottari_timeline(moon["absolute_degree"], dob)

        # House lords (which planet rules each house from the Lagna)
        house_lords = {}
        asc_sign_idx = int(asc_deg / 30)
        for h in range(1, 13):
            ruled_sign = SIGNS[(asc_sign_idx + h - 1) % 12]
            house_lords[str(h)] = SIGN_LORDS[ruled_sign]

        return {
            "lagna":             asc_sign,
            "lagna_lord":        SIGN_LORDS[asc_sign],
            "ascendant_degree":  round(asc_deg, 2),
            "current_dasha":     f"{dasha_info['mahadasha']} Mahadasha",
            "dasha_detail":      dasha_info,
            "dasha_timeline":    timeline,
            "house_lords":       house_lords,
            "planets":           planet_data,
        }
