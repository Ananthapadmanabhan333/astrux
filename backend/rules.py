from knowledge import (PLANET_IN_HOUSE, PLANET_IN_SIGN,
                       NAKSHATRA_INTERPRETATIONS, YOGA_DESCRIPTIONS,
                       DOSHA_REMEDIES, GEMSTONE_GUIDE)

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

SIGN_LORDS = {
    "Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
    "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars",
    "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"
}

NATURAL_BENEFICS  = {"Jupiter","Venus","Moon","Mercury"}
NATURAL_MALEFICS  = {"Sun","Mars","Saturn","Rahu","Ketu"}

TRIKONA_HOUSES    = {1, 5, 9}
KENDRA_HOUSES     = {1, 4, 7, 10}
UPACHAYA_HOUSES   = {3, 6, 10, 11}
DUSTHANA_HOUSES   = {6, 8, 12}

# ─────────────────────────────────────────────────────────────────────
# House lord descriptions (what each house rules)
# ─────────────────────────────────────────────────────────────────────
HOUSE_SIGNIFICATIONS = {
    1:  "Self, physique, vitality, personality, life direction, childhood, character",
    2:  "Wealth, savings, family lineage, speech, face, right eye, food, values",
    3:  "Courage, younger siblings, communication, writing, short journeys, media, efforts",
    4:  "Mother, home, inner peace, real estate, vehicles, land, ancestral happiness",
    5:  "Intellect, children, romance, creativity, speculation, past-life merit (Purva Punya)",
    6:  "Enemies, debts, diseases, litigation, daily routine, service, competitive ability",
    7:  "Marriage, life partner, business partnerships, legal agreements, foreign travel",
    8:  "Longevity, sudden events, inheritance, occult, transformation, chronic disease, research",
    9:  "Dharma, father, gurus, higher education, long journeys, luck, religion, fortune",
    10: "Career, profession, fame, authority, government, karma, public reputation",
    11: "Gains (Labha), income, elder siblings, social networks, fulfilment of desires",
    12: "Losses, foreign travel, spiritual liberation (Moksha), isolation, hospitalization, sleep",
}

# ─────────────────────────────────────────────────────────────────────
# Nakshatra ruler → qualities added to planet interpretation
# ─────────────────────────────────────────────────────────────────────
NAK_LORD_QUALITY = {
    "Ketu":    "gives intuition, detachment, and past-life karmic activation",
    "Venus":   "bestows charm, artistic talent, and material abundance",
    "Sun":     "grants vitality, authority, and ego-driven ambition",
    "Moon":    "enhances emotional sensitivity, nurturing, and public appeal",
    "Mars":    "adds courage, competitive drive, and physical energy",
    "Rahu":    "creates obsession, unconventional brilliance, and material desire",
    "Jupiter": "confers wisdom, expansion, optimism, and dharmic fortune",
    "Saturn":  "enforces discipline, delays, and deep karmic lessons",
    "Mercury": "sharpens intellect, communication, and analytical precision",
}

# ─────────────────────────────────────────────────────────────────────
# Complete planet-in-house descriptions for all missing planets/houses
# ─────────────────────────────────────────────────────────────────────
EXTENDED_PLACEMENTS = {
    ("Rahu", 1):  "Rahu in the 1st house creates an unconventional, magnetic, and ambitious personality. You appear mysterious and unusual to others. Intense desire to reinvent identity. Foreign contacts, technology, and non-traditional paths favour you strongly.",
    ("Rahu", 2):  "Rahu in the 2nd house creates obsession with wealth, speech, and family status. Income through unconventional or foreign sources. Tendency to exaggerate. Financial ups and downs until discipline is applied.",
    ("Rahu", 3):  "Rahu in the 3rd house gives extraordinary communication skills, strategic intelligence, and courage in unconventional media, digital technology, and travel. Younger siblings may be unconventional.",
    ("Rahu", 4):  "Rahu in the 4th house creates restlessness in domestic life. Multiple home changes. May live abroad. Unconventional relationship with mother. Real estate transactions can be profitable but complex.",
    ("Rahu", 5):  "Rahu in the 5th house gives extraordinary creative and speculative intelligence. Unconventional romance. Children may be born under unusual circumstances. Genius-level intellect in technology, occult, or stock markets.",
    ("Rahu", 6):  "Rahu in the 6th house gives tremendous competitive advantage over enemies through strategy and unconventional means. Excellent for law, medicine, and competitive professions. Enemies are ultimately defeated.",
    ("Rahu", 7):  "Rahu in the 7th house brings an unusual, foreign, or unconventional marriage partner. Business partnerships with foreigners or in non-traditional fields. Strong attraction to taboo or exotic relationships.",
    ("Rahu", 8):  "Rahu in the 8th house is powerful and dangerous. Psychic abilities, research into the occult, and sudden life transformations. Inheritance through unusual means. Must guard against obsessive behaviours.",
    ("Rahu", 9):  "Rahu in the 9th house creates a non-conventional philosophical and religious outlook. Foreign gurus, non-traditional spiritual paths. Fortune through long-distance travel and unconventional higher education.",
    ("Rahu",10):  "Rahu in the 10th house gives exceptional ambition and career success — often through technology, media, politics, or unconventional fields. Fame can be sudden and spectacular. A powerhouse for professional achievement.",
    ("Rahu",11):  "Rahu in the 11th house is one of its finest placements. Enormous gains, large income, wide social networks with influential friends. Fulfilment of unusual desires and ambitions.",
    ("Rahu",12):  "Rahu in the 12th house indicates foreign settlement, spiritual liberation, and expenses on unusual pleasures. Sleep disturbances are possible. Interest in meditation, isolation, and hidden spiritual dimensions.",
    ("Ketu", 1):  "Ketu in the 1st house gives a spiritually detached, philosophical, and introspective personality. You appear mysterious and disinterested in material life. Past-life spiritual attainments are strong. Psychic sensitivity is high.",
    ("Ketu", 2):  "Ketu in the 2nd house can bring indifference to material wealth and family traditions. Speech may be blunt or unusual. However, past-life skills in healing, mathematics, or sacred knowledge emerge naturally.",
    ("Ketu", 4):  "Ketu in the 4th house indicates detachment from home and mother in this life. Interest in past lives, ancestral lands, and mystical traditions. Inner spiritual life is very rich despite outer restlessness.",
    ("Ketu", 5):  "Ketu in the 5th house gives extraordinary intuitive intelligence and past-life creative genius. Unconventional children. Detachment from romantic love. Deep interest in mantras, meditation, and esoteric studies.",
    ("Ketu", 7):  "Ketu in the 7th house creates detachment in marriage and partnerships. Relationships are spiritualised. Spouse may be spiritual, unusual, or foreign. Deep learning about relationships through separation or loss.",
    ("Ketu",10):  "Ketu in the 10th house gives detachment from material career ambitions. Past-life professional mastery emerges effortlessly. Spiritual leadership, research, or healing professions are indicated. Fame comes without ego.",
    ("Ketu",12):  "Ketu in the 12th house is a moksha-giving placement. Deep spiritual liberation, meditation, and retreat are central themes. Past-life spiritual practitioner. Excellent for yogis, healers, and renunciates.",
}


class AstroRulesEngine:
    def __init__(self, chart_data):
        self.lagna        = chart_data["lagna"]
        self.lagna_lord   = chart_data.get("lagna_lord", "")
        self.house_lords  = chart_data.get("house_lords", {})
        self.planets      = {p["name"]: p for p in chart_data["planets"]}
        self.dasha_detail = chart_data.get("dasha_detail", {})
        self.dasha_timeline = chart_data.get("dasha_timeline", [])

    def analyze(self):
        insights = []
        insights.extend(self.check_lagna())
        insights.extend(self.check_placements())
        insights.extend(self.check_sign_dignities())
        insights.extend(self.check_nakshatra_interpretations())
        insights.extend(self.check_house_lord_strengths())
        insights.extend(self.check_doshas())
        insights.extend(self.check_yogas())
        insights.extend(self.check_raj_yogas())
        insights.extend(self.check_dhana_yogas())
        insights.extend(self.check_pancha_mahapurusha())
        insights.extend(self.check_viparita_raj_yoga())
        insights.extend(self.get_dasha_report())
        insights.extend(self.get_gemstones_and_remedies())
        insights.extend(self.get_karmic_axis())
        insights.extend(self.check_special_combinations())
        return insights

    # ─────────────────────────────────────────────
    # 1. Lagna
    # ─────────────────────────────────────────────
    def check_lagna(self):
        descriptions = {
            "Aries":       "Mesha Lagna (Ruled by Mars) — Born pioneer: energetic, courageous, fiercely independent. Your life is shaped by action and initiative. Natural leaders who thrive in competition. Lagna Lord Mars rules your vitality, self-expression and life direction. Guard against impatience.",
            "Taurus":      "Vrishabha Lagna (Ruled by Venus) — Stable, sensual, deeply appreciative of beauty. Life shaped by security, aesthetic refinement, and the accumulation of value. Venus as Lagna Lord links your identity to beauty, wealth, and harmonious relationships. Guard against stubbornness.",
            "Gemini":      "Mithuna Lagna (Ruled by Mercury) — Quick-witted, curious, constantly adapting. Life shaped by intellectual variety, writing, and social connections. Mercury as Lagna Lord makes you a natural communicator and analyst. Guard against restlessness.",
            "Cancer":      "Karka Lagna (Ruled by Moon) — Deeply intuitive, nurturing, emotionally perceptive. Life shaped by family bonds, emotional security, and psychic sensitivity. Moon as Lagna Lord links your entire life to emotional cycles. Guard against moodiness.",
            "Leo":         "Simha Lagna (Ruled by Sun) — Regal, generous, creatively expressive. Life shaped by recognition, leadership, and noble dignity. Sun as Lagna Lord gives extraordinary vitality and a magnetic public presence. Guard against pride.",
            "Virgo":       "Kanya Lagna (Ruled by Mercury) — Analytical, precise, service-oriented. Life shaped by critical thinking, health, and devotion to improvement and order. Mercury as Lagna Lord makes you an exceptional analyst and communicator. Guard against anxiety.",
            "Libra":       "Tula Lagna (Ruled by Venus) — Diplomatic, aesthetically gifted, inherently fair. Life shaped by partnerships, justice, and harmony. Venus as Lagna Lord gives beauty, charm, and a deep need for balanced relationships. Guard against indecision.",
            "Scorpio":     "Vrishchika Lagna (Ruled by Mars/Ketu) — Intensely perceptive, psychologically powerful, deeply transformative. Life shaped by hidden depths, research, and profound emotional experiences. Guard against jealousy.",
            "Sagittarius": "Dhanu Lagna (Ruled by Jupiter) — Philosophical, adventurous, inherently optimistic. Life shaped by dharma, higher learning, and the pursuit of truth. Jupiter as Lagna Lord gives natural wisdom, fortune, and great teachers.",
            "Capricorn":   "Makara Lagna (Ruled by Saturn) — Disciplined, ambitious, deeply responsible. Life shaped by slow and steady climbs to authority and recognition. Saturn's influence means delays early in life but enduring success after 36.",
            "Aquarius":    "Kumbha Lagna (Ruled by Saturn) — Humanitarian, scientifically unconventional, socially aware. Life shaped by group work, reform, and universal vision. Saturn as Lagna Lord gives enormous capacity for systemic thinking.",
            "Pisces":      "Meena Lagna (Ruled by Jupiter) — Compassionate, spiritually inclined, deeply imaginative. Life shaped by empathy, spiritual seeking, and artistic sensitivity. Jupiter as Lagna Lord blesses with wisdom and divine grace.",
        }
        lagna_lord_house = self.planets.get(self.lagna_lord, {}).get("house", "?")
        desc = descriptions.get(self.lagna, "")
        if desc:
            return [{"type":"lagna","title":f"Lagna: {self.lagna} (Lord: {self.lagna_lord} in {self._ordinal(lagna_lord_house)} House)",
                     "description": desc + f"\n\nLagna Lord {self.lagna_lord} is placed in the {self._ordinal(lagna_lord_house)} house — {HOUSE_SIGNIFICATIONS.get(lagna_lord_house,'')}."}]
        return []

    # ─────────────────────────────────────────────
    # 2. Planet placements (all planets × all houses)
    # ─────────────────────────────────────────────
    def check_placements(self):
        results = []
        for p_name, p_data in self.planets.items():
            house = p_data["house"]
            sign  = p_data["sign"]
            nak   = p_data.get("nakshatra","")
            nl    = p_data.get("nakshatra_lord","")
            retro = p_data.get("retrograde", False)

            desc = None
            if p_name in PLANET_IN_HOUSE and house in PLANET_IN_HOUSE[p_name]:
                desc = PLANET_IN_HOUSE[p_name][house]
            elif (p_name, house) in EXTENDED_PLACEMENTS:
                desc = EXTENDED_PLACEMENTS[(p_name, house)]

            if desc:
                retro_note = " (Currently Retrograde — results are internalised, delayed or intensified.)" if retro else ""
                nak_note   = f"\n\n📍 Nakshatra Layer: {p_name} in {nak} (Nakshatra Lord: {nl}) — {NAK_LORD_QUALITY.get(nl,'')}."
                results.append({
                    "type": "placement",
                    "title": f"{p_name} in {self._ordinal(house)} House ({sign}){' ℞' if retro else ''}",
                    "description": desc + retro_note + nak_note
                })
        return results

    # ─────────────────────────────────────────────
    # 3. Sign dignities
    # ─────────────────────────────────────────────
    def check_sign_dignities(self):
        results = []
        for p_name, p_data in self.planets.items():
            sign = p_data["sign"]
            if p_name in PLANET_IN_SIGN and sign in PLANET_IN_SIGN[p_name]:
                results.append({
                    "type":  "dignity",
                    "title": f"{p_name} in {sign} — Classical Dignity",
                    "description": PLANET_IN_SIGN[p_name][sign]
                })
        return results

    # ─────────────────────────────────────────────
    # 4. Nakshatra
    # ─────────────────────────────────────────────
    def check_nakshatra_interpretations(self):
        results = []
        for p_name, p_data in self.planets.items():
            nak  = p_data.get("nakshatra","")
            pada = p_data.get("pada", 1)
            deg  = p_data.get("degree", 0)
            if nak in NAKSHATRA_INTERPRETATIONS:
                info = NAKSHATRA_INTERPRETATIONS[nak]
                results.append({
                    "type":  "nakshatra",
                    "title": f"{p_name} in {nak} — Pada {pada} ({deg}°)",
                    "description":
                        f"Presiding Deity: {info['deity']}\n"
                        f"Symbol: {info['symbol']}\n\n"
                        f"{info['quality']}\n\n"
                        f"Pada {pada} of {nak} adds the energy of "
                        f"{['Aries','Taurus','Gemini','Cancer'][pada-1]} — "
                        f"{'pioneering fire' if pada==1 else 'earthy stability' if pada==2 else 'communicative air' if pada==3 else 'deeply emotional water'}."
                })
        return results

    # ─────────────────────────────────────────────
    # 5. House lord strengths
    # ─────────────────────────────────────────────
    def check_house_lord_strengths(self):
        results = []
        important_houses = [1, 2, 4, 5, 7, 9, 10, 11]
        for h in important_houses:
            lord_name = self.house_lords.get(str(h), "")
            if not lord_name or lord_name not in self.planets:
                continue
            lord_data  = self.planets[lord_name]
            lord_house = lord_data["house"]
            lord_sign  = lord_data["sign"]
            in_dusthana = lord_house in DUSTHANA_HOUSES
            in_kendra   = lord_house in KENDRA_HOUSES
            in_trikona  = lord_house in TRIKONA_HOUSES

            if in_kendra or in_trikona:
                strength = "Strong (Kendra/Trikona placement)"
                color    = "positive"
            elif in_dusthana:
                strength = "Weakened (Dusthana — 6th/8th/12th placement)"
                color    = "negative"
            else:
                strength = "Moderate"
                color    = "neutral"

            results.append({
                "type":  "house_lord",
                "title": f"{self._ordinal(h)} House Lord: {lord_name} in {self._ordinal(lord_house)} House ({lord_sign}) — {strength}",
                "description": (
                    f"The {self._ordinal(h)} house governs: {HOUSE_SIGNIFICATIONS[h]}.\n\n"
                    f"Its ruler {lord_name} sits in the {self._ordinal(lord_house)} house ({lord_sign}), "
                    f"meaning the affairs of the {self._ordinal(h)} house are directed toward the themes of the "
                    f"{self._ordinal(lord_house)} house ({HOUSE_SIGNIFICATIONS[lord_house]}).\n\n"
                    f"Assessment: {strength}."
                )
            })
        return results

    # ─────────────────────────────────────────────
    # 6. Doshas
    # ─────────────────────────────────────────────
    def check_doshas(self):
        results = []

        # Manglik
        mars = self.planets.get("Mars")
        if mars and mars["house"] in [1,4,7,8,12]:
            r = "\n• ".join(DOSHA_REMEDIES.get("Manglik Dosha",[]))
            results.append({"type":"dosha","title":f"⚠️ Manglik Dosha — Mars in {self._ordinal(mars['house'])} House",
                "description":f"Mars in the {mars['house']}th house activates Kuja Dosha. Marriage and partnerships face friction, aggression, or turbulence unless both partners are Manglik or proper remedies are performed.\n\n✅ Remedies:\n• {r}"})

        # Kemadruma
        moon_h = self.planets.get("Moon",{}).get("house",0)
        if moon_h:
            h2  = (moon_h % 12) + 1
            h12 = ((moon_h-2) % 12) + 1
            adj = [p for n,p in self.planets.items() if n not in ["Moon","Sun","Rahu","Ketu"] and p["house"] in [h2,h12]]
            if not adj:
                r = "\n• ".join(DOSHA_REMEDIES.get("Kemadruma Dosha",[]))
                results.append({"type":"dosha","title":"⚠️ Kemadruma Dosha — Moon Isolated",
                    "description":f"No benefic flanks the Moon. Emotional isolation and mental struggles in early life.\n\n✅ Remedies:\n• {r}"})

        # Sade Sati
        moon_si = SIGNS.index(self.planets.get("Moon",{}).get("sign","Aries"))
        sat_si  = SIGNS.index(self.planets.get("Saturn",{}).get("sign","Aries"))
        if (sat_si - moon_si) % 12 in [0,1,11]:
            r = "\n• ".join(DOSHA_REMEDIES.get("Sade Sati Phase Active",[]))
            results.append({"type":"sadesati","title":"🪐 Sade Sati — Saturn's 7.5-Year Trial Active",
                "description":f"Saturn transits within one sign of your natal Moon. Karmic reckoning, delays, and restructuring are the themes. Emerges with immense strength.\n\n✅ Remedies:\n• {r}"})

        # Pitra Dosha (Sun or Rahu in 9th or afflicted)
        sun_h  = self.planets.get("Sun",{}).get("house",0)
        rahu_h = self.planets.get("Rahu",{}).get("house",0)
        if sun_h == 9 or rahu_h == 9:
            results.append({"type":"dosha","title":"⚠️ Pitra Dosha — Ancestral Karmic Debt",
                "description":"Sun or Rahu in the 9th house indicates karmic debt to ancestors (Pitru Dosha). Difficulties with father or paternal lineage. Remedy: Perform Shraddha (ancestral rites) on Amavasya, donate food to the poor on Sundays, and chant the Aditya Hridayam."})

        # Grahan Dosha (Sun/Moon with Rahu/Ketu)
        for lum in ["Sun","Moon"]:
            lum_h = self.planets.get(lum,{}).get("house",0)
            for node in ["Rahu","Ketu"]:
                node_h = self.planets.get(node,{}).get("house",0)
                if lum_h and lum_h == node_h:
                    results.append({"type":"dosha","title":f"⚠️ Grahan Dosha — {lum} conjunct {node}",
                        "description":f"{lum} and {node} in the same house creates a shadow eclipse effect on the {lum}'s karaka (significations). Life lessons around ego/mind (depending on luminary) and karmic obsession/release cycles. Remedy: Chant {lum} mantras daily and donate accordingly."})

        return results

    # ─────────────────────────────────────────────
    # 7. Classic Yogas
    # ─────────────────────────────────────────────
    def check_yogas(self):
        results = []
        moon_h = self.planets.get("Moon",{}).get("house",-1)
        jup_h  = self.planets.get("Jupiter",{}).get("house",-1)
        sun_h  = self.planets.get("Sun",{}).get("house",-1)
        mer_h  = self.planets.get("Mercury",{}).get("house",-1)
        ven_h  = self.planets.get("Venus",{}).get("house",-1)

        if moon_h != -1 and jup_h != -1 and (jup_h-moon_h)%12 in [0,3,6,9]:
            results.append({"type":"yoga","title":"✨ Gajakesari Yoga — Elephant-Lion Power",
                "description":YOGA_DESCRIPTIONS["Gajakesari Yoga"]})

        if sun_h != -1 and mer_h != -1 and sun_h == mer_h:
            results.append({"type":"yoga","title":"✨ Budha-Aditya Yoga — Sun + Mercury Brilliance",
                "description":YOGA_DESCRIPTIONS["Budha-Aditya Yoga"]})

        # Chandra-Mangala Yoga
        mars_h = self.planets.get("Mars",{}).get("house",-1)
        if moon_h != -1 and mars_h != -1 and moon_h == mars_h:
            results.append({"type":"yoga","title":"✨ Chandra-Mangala Yoga — Wealth through Courage",
                "description":"Moon and Mars together create this wealth-producing yoga. Emotional courage drives financial gains. Skilled in buying, selling, real estate, and entrepreneurship. Income comes through bold decisions and emotional intelligence."})

        # Amala Yoga
        for pl in ["Jupiter","Venus","Moon"]:
            if self.planets.get(pl,{}).get("house") == 10:
                results.append({"type":"yoga","title":f"✨ Amala Yoga — Natural Benefic ({pl}) in 10th House",
                    "description":f"{pl} in the 10th house forms Amala Yoga — a blameless, highly ethical career that earns lasting fame and respect. The native becomes known for virtue and integrity in their profession."})
                break

        # Adhi Yoga
        bens_in_6_7_8 = [p for n,p in self.planets.items() if n in NATURAL_BENEFICS and p["house"] in [6,7,8]]
        if len(bens_in_6_7_8) >= 2:
            results.append({"type":"yoga","title":"✨ Adhi Yoga — Ministers / Leaders Yoga",
                "description":"Two or more natural benefics (Jupiter, Venus, Moon, Mercury) occupy the 6th, 7th, and 8th houses from the Moon. This creates Adhi Yoga, producing leaders, ministers, and highly respected individuals who command authority."})

        return results

    # ─────────────────────────────────────────────
    # 8. Raj Yogas (Kendra-Trikona lords together)
    # ─────────────────────────────────────────────
    def check_raj_yogas(self):
        results = []
        asc_idx = SIGNS.index(self.lagna)

        kendra_lords   = {SIGN_LORDS[SIGNS[(asc_idx+h-1)%12]] for h in KENDRA_HOUSES}
        trikona_lords  = {SIGN_LORDS[SIGNS[(asc_idx+h-1)%12]] for h in TRIKONA_HOUSES}

        # Find intersections
        raj_planets = kendra_lords & trikona_lords
        for p_name in raj_planets:
            p = self.planets.get(p_name)
            if p and (p["house"] in KENDRA_HOUSES or p["house"] in TRIKONA_HOUSES):
                results.append({"type":"raj_yoga","title":f"👑 Raj Yoga — {p_name} (Lord of Kendra & Trikona)",
                    "description":f"{p_name} rules both a Kendra house and a Trikona house from your Lagna, making it a supreme Raj Yoga karaka. Placed in the {self._ordinal(p['house'])} house ({p['sign']}), it bestows extraordinary career success, authority, social recognition, and wealth — especially during its Mahadasha and Antardasha periods."})

        # Check if Kendra lord and Trikona lord are conjunct
        for kl in kendra_lords:
            for tl in trikona_lords:
                if kl != tl and kl in self.planets and tl in self.planets:
                    kp, tp = self.planets[kl], self.planets[tl]
                    if kp["house"] == tp["house"]:
                        results.append({"type":"raj_yoga","title":f"👑 Powerful Raj Yoga — {kl} + {tl} Conjunction",
                            "description":f"Lord of a Kendra ({kl}) and lord of a Trikona ({tl}) are conjoined in the {self._ordinal(kp['house'])} house. This is a supreme Raj Yoga granting royal authority, political power, professional eminence, and prosperity — especially active during either planet's major or sub periods."})

        return results

    # ─────────────────────────────────────────────
    # 9. Dhana Yogas (wealth)
    # ─────────────────────────────────────────────
    def check_dhana_yogas(self):
        results = []
        asc_idx  = SIGNS.index(self.lagna)
        lord2    = SIGN_LORDS[SIGNS[(asc_idx+1)%12]]
        lord11   = SIGN_LORDS[SIGNS[(asc_idx+10)%12]]
        lord5    = SIGN_LORDS[SIGNS[(asc_idx+4)%12]]
        lord9    = SIGN_LORDS[SIGNS[(asc_idx+8)%12]]

        # 2nd + 11th lords together or in each other's houses
        if lord2 in self.planets and lord11 in self.planets:
            h2, h11 = self.planets[lord2]["house"], self.planets[lord11]["house"]
            if h2 == h11 or (h2 in [2,11] and h11 in [2,11]):
                results.append({"type":"yoga","title":"💰 Dhana Yoga — 2nd & 11th Lords Linked",
                    "description":f"The lords of the 2nd house (wealth) and 11th house (gains), {lord2} and {lord11}, are strongly linked. This forms a classic Dhana Yoga indicating multiple income streams, accumulated wealth, and financial prosperity — especially during their Dasha periods."})

        # 5th + 9th lords together
        if lord5 in self.planets and lord9 in self.planets:
            h5, h9 = self.planets[lord5]["house"], self.planets[lord9]["house"]
            if h5 == h9:
                results.append({"type":"yoga","title":"💰 Lakshmi Yoga — 5th & 9th Lords Conjunct",
                    "description":f"The lords of the 5th (intellect/purva punya) and 9th (fortune/dharma) houses are together: {lord5} and {lord9}. This is the powerful Lakshmi Yoga — extraordinary fortune, wealth, and divine grace. The Goddess of Prosperity is believed to bless such a chart abundantly."})

        # Jupiter in 2nd or 11th
        jup = self.planets.get("Jupiter")
        if jup and jup["house"] in [2, 5, 9, 11]:
            results.append({"type":"yoga","title":f"💰 Guru Dhana Yoga — Jupiter in {self._ordinal(jup['house'])} House",
                "description":f"Jupiter, the natural significator of wealth and wisdom, in the {self._ordinal(jup['house'])} house is an immensely auspicious Dhana Yoga. Wealth accumulates through ethical means, teaching, law, finance, or spiritual guidance. Jupiter's blessing ensures financial expansion over time."})

        return results

    # ─────────────────────────────────────────────
    # 10. Pancha Mahapurusha Yogas
    # ─────────────────────────────────────────────
    def check_pancha_mahapurusha(self):
        results = []
        rules = {
            "Jupiter": ("Hamsa",   ["Sagittarius","Pisces","Cancer"],   "grace, divine knowledge, spiritual wisdom, and a brilliant, prosperous life"),
            "Mars":    ("Ruchaka", ["Aries","Scorpio","Capricorn"],      "physical courage, athletic prowess, military leadership, and competitive invincibility"),
            "Mercury": ("Bhadra",  ["Gemini","Virgo"],                   "extraordinary intellect, mastery of communication, business acumen, and scholarly distinction"),
            "Venus":   ("Malavya", ["Taurus","Libra","Pisces"],          "beauty, luxury, artistic fame, harmonious marriage, and sensual enjoyment of life's finest pleasures"),
            "Saturn":  ("Sasha",   ["Capricorn","Aquarius","Libra"],     "enduring authority, administrative mastery, discipline, and commanding respect at the very top of the chosen field"),
        }
        for planet, (yoga_name, signs, quality) in rules.items():
            p = self.planets.get(planet)
            if p and p["house"] in KENDRA_HOUSES and p["sign"] in signs:
                results.append({"type":"yoga","title":f"🌟 {yoga_name} Yoga (Pancha Mahapurusha) — {planet} in {p['sign']}",
                    "description":f"One of the celebrated Five Great Planetary Yogas (Pancha Mahapurusha). {planet} in a Kendra ({self._ordinal(p['house'])} house) in its own sign or exaltation ({p['sign']}) produces {yoga_name} Yoga — conferring {quality}."})
        return results

    # ─────────────────────────────────────────────
    # 11. Viparita Raja Yoga
    # ─────────────────────────────────────────────
    def check_viparita_raj_yoga(self):
        results = []
        asc_idx = SIGNS.index(self.lagna)
        dusthana_lords = {
            6:  SIGN_LORDS[SIGNS[(asc_idx+5)%12]],
            8:  SIGN_LORDS[SIGNS[(asc_idx+7)%12]],
            12: SIGN_LORDS[SIGNS[(asc_idx+11)%12]],
        }
        for h, lord in dusthana_lords.items():
            p = self.planets.get(lord)
            if p and p["house"] in [6,8,12] and p["house"] != h:
                results.append({"type":"yoga","title":f"⚡ Viparita Raja Yoga — {lord} (Lord of {h}th) in {self._ordinal(p['house'])} House",
                    "description":f"The lord of the {h}th house (a Dusthana) is placed in another Dusthana — this paradox creates Viparita Raja Yoga. Through adversity, sudden reversals, and others' defeat or misfortune, the native rises dramatically. Fame and success come unexpectedly — especially after periods of great struggle."})
        return results

    # ─────────────────────────────────────────────
    # 12. Dasha report
    # ─────────────────────────────────────────────
    def get_dasha_report(self):
        d = self.dasha_detail
        if not d or d.get("mahadasha") == "Unknown":
            return []

        maha  = d.get("mahadasha","")
        antar = d.get("antardasha","")
        m_end = d.get("mahadasha_end","")
        a_end = d.get("antardasha_end","")

        maha_planet  = self.planets.get(maha, {})
        antar_planet = self.planets.get(antar, {})

        maha_desc = (f"{maha} is placed in the {self._ordinal(maha_planet.get('house','?'))} house in {maha_planet.get('sign','')}. "
                     f"Its natural karaka significations dominate this period. "
                     f"House themes activated: {HOUSE_SIGNIFICATIONS.get(maha_planet.get('house',0),'')}."
                     if maha_planet else "")

        antar_desc = (f"Sub-period lord {antar} sits in the {self._ordinal(antar_planet.get('house','?'))} house ({antar_planet.get('sign','')}), "
                      f"focusing the Mahadasha energy onto: {HOUSE_SIGNIFICATIONS.get(antar_planet.get('house',0),'')}."
                      if antar_planet else "")

        full = [{"type":"dasha","title":f"🕰️ Current Period: {maha} Mahadasha / {antar} Antardasha",
            "description":
                f"You are currently running:\n"
                f"• Mahadasha (Major Period): {maha} — until {m_end}\n"
                f"• Antardasha (Sub-Period):  {antar} — until {a_end}\n\n"
                f"{maha_desc}\n\n{antar_desc}\n\n"
                f"The combined energy of {maha} + {antar} shapes all key life events — career, relationships, health, and finances — during this window."}]

        if self.dasha_timeline:
            tl_text = "\n".join([f"• {t['mahadasha']} Mahadasha: {t['start']} → {t['end']} ({t['years']} yrs)"
                                  for t in self.dasha_timeline])
            full.append({"type":"dasha","title":"📅 Full Vimshottari Dasha Timeline (120-Year Cycle)",
                "description": f"Your complete Mahadasha sequence from birth:\n\n{tl_text}"})

        return full

    # ─────────────────────────────────────────────
    # 13. Gemstones
    # ─────────────────────────────────────────────
    def get_gemstones_and_remedies(self):
        remedies = []
        lagna_planet_map = {
            "Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
            "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars",
            "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"
        }
        planet = lagna_planet_map.get(self.lagna)
        if planet and planet in GEMSTONE_GUIDE:
            g = GEMSTONE_GUIDE[planet]
            remedies.append({"type":"gemstone","title":f"💎 Primary Lagna Gemstone — {g['gem']} (Strengthens {planet})",
                "description":(f"As a {self.lagna} Ascendant, your ruling planet is {planet}.\n\n"
                                f"Primary Stone:  {g['gem']}\n"
                                f"Substitute:     {g['substitute']}\n"
                                f"Metal:          {g['metal']}\n"
                                f"Finger:         {g['finger']}\n"
                                f"Wear on:        {g['day']}\n"
                                f"Weight:         {g['weight']}\n\n"
                                f"Always consult a qualified Jyotisha before wearing gemstones. The stone must be natural, unheated, and energised with the appropriate mantra.")})

        for pn in ["Jupiter","Venus","Mercury","Moon"]:
            p = self.planets.get(pn)
            if p and p["house"] in [1,4,5,7,9,10,11] and pn in GEMSTONE_GUIDE:
                g = GEMSTONE_GUIDE[pn]
                remedies.append({"type":"gemstone","title":f"💎 Supportive Gemstone — {g['gem']} (Amplifies {pn})",
                    "description":(f"{pn} is well-placed in the {self._ordinal(p['house'])} house in {p['sign']}.\n\n"
                                   f"Stone:      {g['gem']}\n"
                                   f"Substitute: {g['substitute']}\n"
                                   f"Metal:      {g['metal']}\n"
                                   f"Finger:     {g['finger']}\n"
                                   f"Wear on:    {g['day']}\n"
                                   f"Weight:     {g['weight']}")})
                break
        return remedies

    # ─────────────────────────────────────────────
    # 14. Karmic axis
    # ─────────────────────────────────────────────
    def get_karmic_axis(self):
        rahu = self.planets.get("Rahu")
        ketu = self.planets.get("Ketu")
        if not rahu or not ketu:
            return []
        ri = NAKSHATRA_INTERPRETATIONS.get(rahu.get("nakshatra",""), {})
        ki = NAKSHATRA_INTERPRETATIONS.get(ketu.get("nakshatra",""), {})
        return [{"type":"karmic","title":f"🔮 Karmic Axis — Rahu in {rahu['sign']} (H{rahu['house']}) / Ketu in {ketu['sign']} (H{ketu['house']})",
            "description":(
                f"RAHU — Soul's North Node (Current Lifetime Obsession & Desire)\n"
                f"Rahu in {rahu['sign']} / {rahu.get('nakshatra','')} / {self._ordinal(rahu['house'])} House\n"
                f"{ri.get('quality','')}\n\n"
                f"Your soul is hungry for the qualities of {rahu['sign']}. This is new karmic territory — unfamiliar but magnetic. "
                f"Mastery here brings extraordinary worldly success and karmic evolution.\n\n"
                f"KETU — Soul's South Node (Past-Life Mastery & Release)\n"
                f"Ketu in {ketu['sign']} / {ketu.get('nakshatra','')} / {self._ordinal(ketu['house'])} House\n"
                f"{ki.get('quality','')}\n\n"
                f"You already mastered the qualities of {ketu['sign']} in past lives. These gifts emerge effortlessly — "
                f"but over-attachment to them blocks your evolutionary growth toward Rahu's path.\n\n"
                f"🙏 Remedies:\n"
                f"• Rahu: Worship Goddess Durga, donate coconuts/blankets, chant 'Om Raam Rahave Namah' 108×\n"
                f"• Ketu: Worship Ganesha, feed street dogs, chant 'Om Sraam Sreem Sraum Sah Ketave Namah' 108×"
            )}]

    # ─────────────────────────────────────────────
    # 15. Special combinations
    # ─────────────────────────────────────────────
    def check_special_combinations(self):
        results = []

        # Parivartana Yoga (mutual exchange)
        planet_list = list(self.planets.items())
        for i, (n1, p1) in enumerate(planet_list):
            for n2, p2 in planet_list[i+1:]:
                if n1 in ["Rahu","Ketu"] or n2 in ["Rahu","Ketu"]:
                    continue
                # n1 in sign ruled by n2, and n2 in sign ruled by n1
                asc_idx = SIGNS.index(self.lagna)
                sign1_lord = SIGN_LORDS.get(p1["sign"],"")
                sign2_lord = SIGN_LORDS.get(p2["sign"],"")
                if sign1_lord == n2 and sign2_lord == n1:
                    results.append({"type":"yoga","title":f"🔄 Parivartana Yoga — {n1} ⇄ {n2} (Mutual Exchange)",
                        "description":f"{n1} is in {n2}'s sign and {n2} is in {n1}'s sign. This mutual exchange (Parivartana) gives both planets significant strength as if they were in their own signs. The houses they rule exchange energy, activating both sets of house themes powerfully during either planet's Dasha."})

        # Vargottama (same sign in D1 and D9 — simplified: degree in last 3.33° or first 3.33°)
        for p_name, p_data in self.planets.items():
            deg = p_data.get("degree", 0)
            if deg <= 3.33 or deg >= 26.67:
                results.append({"type":"dignity","title":f"⭐ Vargottama Position — {p_name} at {deg}° in {p_data['sign']}",
                    "description":f"{p_name} is near the boundary of its sign, indicating a Vargottama-like quality (same sign in the D1 and D9 Navamsa charts in classical calculation). Vargottama planets are exceptionally strong and deliver pure, unadulterated results of their sign placement throughout the lifetime."})

        return results

    def _ordinal(self, n):
        if not isinstance(n, int):
            return str(n)
        suffix = {1:"st",2:"nd",3:"rd"}.get(n if n < 20 else n % 10, "th")
        return f"{n}{suffix}"
