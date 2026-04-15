from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import openai
import base64

from astro_engine import AstroEngine
from rules import AstroRulesEngine

app = FastAPI(title="Astrology Super App Engine API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = None
if os.getenv("OPENAI_API_KEY"):
    client = openai.OpenAI()

# Initialize engine globally to limit overhead
engine = AstroEngine()

# --- Models ---
class ChatRequest(BaseModel):
    message: str
    user_id: str
    chart_context: dict

class ChatResponse(BaseModel):
    reply: str
    sources: List[str]

class ChartRequest(BaseModel):
    date_of_birth: str # YYYY-MM-DD
    time_of_birth: str # HH:MM
    latitude: float
    longitude: float

class MatchRequest(BaseModel):
    boy_dob: str
    boy_tob: str
    boy_lat: float
    boy_lon: float
    girl_dob: str
    girl_tob: str
    girl_lat: float
    girl_lon: float

# --- Endpoints ---

@app.post("/match")
def match_kundali(req: MatchRequest):
    boy  = engine.calculate_chart(req.boy_dob,  req.boy_tob,  req.boy_lat,  req.boy_lon)
    girl = engine.calculate_chart(req.girl_dob, req.girl_tob, req.girl_lat, req.girl_lon)

    boy_moon  = next(p for p in boy["planets"]  if p["name"] == "Moon")
    girl_moon = next(p for p in girl["planets"] if p["name"] == "Moon")
    boy_mars  = next((p for p in boy["planets"]  if p["name"] == "Mars"), None)
    girl_mars = next((p for p in girl["planets"] if p["name"] == "Mars"), None)
    boy_venus = next((p for p in boy["planets"]  if p["name"] == "Venus"), None)
    girl_venus= next((p for p in girl["planets"] if p["name"] == "Venus"), None)
    boy_jup   = next((p for p in boy["planets"]  if p["name"] == "Jupiter"), None)
    girl_jup  = next((p for p in girl["planets"] if p["name"] == "Jupiter"), None)

    score_data = engine.calculate_compatibility(boy_moon["nakshatra"], girl_moon["nakshatra"])

    # ── Guna descriptions
    GUNA_DESCRIPTIONS = {
        "Varna (Spiritual)": {
            "full": "Varna tests the spiritual compatibility and ego levels of the couple. It reflects whether both partners operate at the same evolutionary level of consciousness and whether their spiritual orientations align harmoniously.",
            "max": 1
        },
        "Vashya (Dominance)": {
            "full": "Vashya indicates the natural magnetic attraction and control between the couple. It shows who naturally leads in the relationship and whether the couple exercises a positive, complementary influence on each other.",
            "max": 2
        },
        "Tara (Health/Trust)": {
            "full": "Tara Koota checks the health, well-being, and destiny compatibility of the couple. A high Tara score indicates that the couple's stars are in mutual harmony and that they will support each other's health and longevity.",
            "max": 3
        },
        "Yoni (Sexual)": {
            "full": "Yoni Koota assesses sexual compatibility, physical intimacy, and biological affinity. Each Nakshatra is assigned an animal symbol — matching or compatible animals indicate a deeply fulfilling and harmonious sexual and physical bond.",
            "max": 4
        },
        "Graha Maitri (Mental)": {
            "full": "Graha Maitri tests the mental compatibility and friendship between the couple based on their Moon sign lords. It indicates whether the couple will be intellectual companions, share common worldviews, and maintain mental harmony over the long term.",
            "max": 5
        },
        "Gana (Nature)": {
            "full": "Gana Koota classifies each person's fundamental nature as Deva (divine), Manushya (human), or Rakshasa (fierce). Compatible Ganas ensure that the couple's fundamental temperaments are in harmony — reducing conflict and increasing mutual understanding.",
            "max": 6
        },
        "Bhakoot (Love)": {
            "full": "Bhakoot is one of the most important Kootas, contributing 7 points. It tests the love, emotional bonding, health of the family, and prosperous growth of the couple. Certain Bhakoot combinations can indicate emotional distance or health challenges.",
            "max": 7
        },
        "Nadi (Health/Genes)": {
            "full": "Nadi is the most important Koota (8 points) and tests biological and genetic compatibility. Same Nadi between partners is classically considered a major defect (Nadi Dosha) that can affect health, progeny, and overall life harmony. Different Nadis indicate healthy genetic diversity.",
            "max": 8
        },
    }

    guna_breakdown = score_data["guna_breakdown"]
    guna_detailed = {}
    for guna_name, desc_data in GUNA_DESCRIPTIONS.items():
        short_key = guna_name.split(" ")[0]  # e.g., "Varna"
        score_key = next((k for k in guna_breakdown if k.startswith(short_key)), None)
        if score_key:
            raw = guna_breakdown[score_key]
            sc  = raw["score"] if isinstance(raw, dict) else raw
            mx  = desc_data["max"]
            pct = round((sc / mx) * 100)
            guna_detailed[guna_name] = {
                "score": sc, "max": mx, "percent": pct,
                "status": "Excellent" if pct >= 75 else "Good" if pct >= 50 else "Moderate" if pct >= 25 else "Poor",
                "description": desc_data["full"]
            }

    # ── Manglik compatibility
    boy_manglik  = boy_mars  and boy_mars["house"]  in [1,4,7,8,12]
    girl_manglik = girl_mars and girl_mars["house"] in [1,4,7,8,12]
    manglik_status = (
        "✅ Both partners are Manglik — the Doshas cancel each other out. Marriage is highly auspicious."
        if boy_manglik and girl_manglik else
        "⚠️ Boy is Manglik but Girl is not — Manglik Dosha is present. Kumbh Vivah ritual or matching with another Manglik is recommended before marriage."
        if boy_manglik else
        "⚠️ Girl is Manglik but Boy is not — Manglik Dosha is present. Kumbh Vivah ritual or matching with another Manglik is recommended before marriage."
        if girl_manglik else
        "✅ Neither partner is Manglik — no Kuja Dosha concerns. Marriage is free from this challenge."
    )

    # ── Rajju / Life-span compatibility (simplified)
    RAJJU_GROUPS = {
        "Siro (Head)": ["Mrigashira","Chitra","Dhanishta"],
        "Kantha (Neck)": ["Rohini","Ardra","Hasta","Swati","Shatabhisha"],
        "Udara (Belly)": ["Kritika","Punarvasu","Uttara Phalguni","Vishakha","Uttara Ashadha"],
        "Nabhi (Navel)": ["Bharani","Pushya","Purva Phalguni","Anuradha","Purva Ashadha","Shravana"],
        "Pada (Feet)": ["Ashwini","Ashlesha","Magha","Jyeshtha","Mula","Revati"],
        "Free": ["Krittika","Uttara Bhadrapada","Purva Bhadrapada"]
    }
    boy_rajju = girl_rajju = "Unknown"
    for rname, naks in RAJJU_GROUPS.items():
        if boy_moon["nakshatra"] in naks:  boy_rajju = rname
        if girl_moon["nakshatra"] in naks: girl_rajju = rname

    rajju_ok = boy_rajju != girl_rajju
    rajju_report = (
        f"✅ Good Rajju match — Boy's Rajju ({boy_rajju}) and Girl's Rajju ({girl_rajju}) are different. This indicates longevity, health, and prosperity for the couple."
        if rajju_ok else
        f"⚠️ Rajju Dosha present — Both partners share the same Rajju ({boy_rajju}). Classical texts advise performing Rajju Shanti puja before marriage to mitigate potential health and longevity concerns."
    )

    # ── Venus-Jupiter compatibility (love & wisdom)
    ven_jup_report = []
    if boy_venus and girl_jup:
        if boy_venus["sign"] == girl_jup["sign"] or abs(boy_venus["house"] - girl_jup["house"]) in [0,6]:
            ven_jup_report.append("Boy's Venus aligns with Girl's Jupiter — strong spiritual love, mutual respect, and wisdom in the relationship.")
    if girl_venus and boy_jup:
        if girl_venus["sign"] == boy_jup["sign"] or abs(girl_venus["house"] - boy_jup["house"]) in [0,6]:
            ven_jup_report.append("Girl's Venus aligns with Boy's Jupiter — the relationship is blessed with grace, expansion, and deep philosophical companionship.")

    # ── Moon sign relationship
    SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
    boy_moon_idx  = SIGNS.index(boy_moon["sign"])  if boy_moon["sign"] in SIGNS else 0
    girl_moon_idx = SIGNS.index(girl_moon["sign"]) if girl_moon["sign"] in SIGNS else 0
    moon_diff = abs(boy_moon_idx - girl_moon_idx)
    moon_rel = (
        "🌕 Same Moon Sign — deeply emotional understanding, similar needs, but may amplify each other's moods."
        if moon_diff == 0 else
        "💞 Trine Moon signs (120°) — natural harmony, shared values, excellent emotional resonance."
        if moon_diff in [4,8] else
        "🤝 Sextile Moon signs (60°) — friendly, supportive, easy communication and emotional compatibility."
        if moon_diff in [2,10] else
        "⚡ Square Moon signs (90°) — dynamic tension that can fuel passion but requires conscious communication."
        if moon_diff in [3,9] else
        "🌑 Opposition Moon signs (180°) — strong magnetic attraction through differences; growth through balancing opposite emotional styles."
        if moon_diff == 6 else
        "🌙 Adjacent Moon signs — some adjustment required; different emotional rhythms that can complement over time."
    )

    # ── Life report predictions
    total = score_data["score"]
    life_report = {
        "Overall_Compatibility": (
            f"With a Guna Milan score of {total}/36, this match is rated '{score_data['status']}'. "
            + ("The cosmic forces are powerfully aligned for this couple. This is a rare, deeply auspicious union blessed by the stars. Both partners will uplift each other spiritually, materially, and emotionally throughout their lives."
               if total >= 28 else
               "This is a harmonious and compatible union with strong natural affinity. The couple will enjoy mutual growth, understanding, and happiness. Minor differences will be easily resolved with love and communication."
               if total >= 22 else
               "This is a moderately compatible match. While there are genuine areas of harmony, some differences in emotional style and temperament require conscious effort and mutual understanding."
               if total >= 18 else
               "This match faces significant karmic challenges. Strong remedies and conscious effort are required to build a lasting, harmonious relationship. Consult a qualified astrologer before proceeding.")
        ),
        "Love_and_Romance": (
            f"The Moon signs of {boy_moon['sign']} (Boy) and {girl_moon['sign']} (Girl) create a {score_data['status'].lower()} romantic foundation. "
            + moon_rel +
            (" Venus and Jupiter alignments further bless this union with deep romantic compatibility. " if ven_jup_report else " ") +
            "The couple's shared emotional wavelength determines their capacity for deep intimacy and lasting romance."
        ),
        "Marriage_and_Partnership": (
            f"{'This is a spiritually blessed marriage.' if total >= 25 else 'This marriage will require consistent effort and mutual compromise.'} "
            f"The 7th house dynamics of both charts indicate "
            f"{'a devoted, spiritually aware, and educated partner who brings wisdom into the marriage. Jupiter energy in the 7th is a powerful marital blessing.' if boy_jup and boy_jup['house'] == 7 else ''} "
            f"{'Mars in the 7th creates an energetic, passionate but potentially argumentative dynamic that must be consciously channelled.' if boy_mars and boy_mars['house'] == 7 else ''} "
            f"The couple is advised to respect each other's independence while building a shared vision for their home and family life."
        ),
        "Children_and_Family": (
            f"Jupiter's placement in both charts indicates the potential for {'blessed, intelligent children with strong dharmic merit' if (boy_jup and boy_jup['house'] in [5,9]) or (girl_jup and girl_jup['house'] in [5,9]) else 'children who may arrive after some delay but will be deeply loved and cared for'}. "
            f"The 5th house strength in both charts suggests "
            f"{'a creative, intellectually gifted family environment' if total >= 22 else 'some challenges in starting a family that can be addressed through Santana Gopala mantra and astrological remedies'}. "
            "Family harmony is strongly supported by maintaining open communication and honouring each other's emotional needs."
        ),
        "Career_and_Finance": (
            f"The combined chart energy suggests financial stability {'that grows strongly after the first 5 years of marriage' if total >= 22 else 'that requires careful budgeting and financial planning together'}. "
            f"Boy's {boy['lagna']} Lagna and Girl's {girl['lagna']} Lagna create a {'mutually supportive' if total >= 18 else 'potentially competitive'} professional dynamic. "
            f"Saturn's placement in both charts determines the pace and solidity of financial growth — steady discipline and shared financial goals will be the foundation of prosperity."
        ),
        "Health_and_Longevity": (
            f"{rajju_report} "
            f"The Nadi Koota score of {guna_detailed.get('Nadi (Health/Genes)',{}).get('score','N/A')}/8 indicates "
            f"{'excellent genetic compatibility, good health prospects for the couple and their children' if guna_detailed.get('Nadi (Health/Genes)',{}).get('score',0) >= 6 else 'moderate health compatibility — both partners should maintain individual wellness practices and support each other proactively'}."
        ),
        "Spiritual_Compatibility": (
            f"Varna Koota ({guna_detailed.get('Varna (Spiritual)',{}).get('score','?')}/1) and Gana Koota ({guna_detailed.get('Gana (Nature)',{}).get('score','?')}/6) together reflect the spiritual alignment of this couple. "
            + ("The spiritual paths of both partners are deeply harmonious. Together they will grow in wisdom and devotion, creating a spiritually rich home." if total >= 22 else
               "Some differences in spiritual inclination exist. The couple can bridge these through shared religious practices, pilgrimage, and mutual respect for each other's beliefs.")
        ),
        "Remedies_and_Recommendations": (
            ("This highly auspicious match requires no major remedies. Perform a Sapta-Padi (seven steps) ceremony with full Vedic rites for an auspicious beginning. Recite the Vivah Sukta and perform Lakshmi-Narayana puja on the wedding day." if total >= 28 else "") +
            (manglik_status) + "\n\n" +
            ("Recommended remedies for sustained harmony:\n"
             "• Recite Lalita Sahasranama together on Fridays\n"
             "• Perform Satyanarayan Puja on full moon days\n"
             "• Offer yellow flowers to Lord Vishnu on Thursdays\n"
             "• Keep a Shri Yantra in the home for prosperity\n"
             "• Both partners wear their respective Lagna gemstones after energisation")
        ),
    }

    return {
        "boy":  {"lagna": boy["lagna"],  "moon_sign": boy_moon["sign"],  "moon_nak": boy_moon["nakshatra"],  "lagna_lord": boy.get("lagna_lord",""),  "current_dasha": boy.get("current_dasha",""), "manglik": boy_manglik,  "rajju": boy_rajju},
        "girl": {"lagna": girl["lagna"], "moon_sign": girl_moon["sign"], "moon_nak": girl_moon["nakshatra"], "lagna_lord": girl.get("lagna_lord",""), "current_dasha": girl.get("current_dasha",""), "manglik": girl_manglik, "rajju": girl_rajju},
        "match": {
            "score":  total,
            "max":    36,
            "status": score_data["status"],
            "guna_detailed": guna_detailed,
            "manglik_report": manglik_status,
            "rajju_report":   rajju_report,
            "moon_relationship": moon_rel,
            "venus_jupiter": ven_jup_report,
            "life_report": life_report,
        }
    }


@app.get("/panchang")
def get_panchang(date: str, lat: float, lon: float):
    return engine.get_panchang(date, lat, lon)

@app.post("/dasha-timeline")
def get_dasha_timeline(req: ChartRequest):
    try:
        chart = engine.calculate_chart(req.date_of_birth, req.time_of_birth, req.latitude, req.longitude)
        return {
            "dasha_timeline": chart["dasha_timeline"],
            "dasha_detail":   chart["dasha_detail"],
            "moon_sign":      next(p["sign"] for p in chart["planets"] if p["name"] == "Moon"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict-palm")
async def predict_palm(file: UploadFile = File(...)):
    contents = await file.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a master Palmist specializing in Vedic palmistry (Samudrika Shastra). Analyze the uploaded image of the palm. Identify mount strength, the life line, heart line, head line, and fate line. Provide an accurate and comforting prediction structured in simple paragraphs."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please read my palm and tell me my future."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=600
            )
            prediction = response.choices[0].message.content
            return {"prediction": prediction}
        except Exception as e:
            return {"prediction": f"(Vision AI Error) Looks like your palm lines are too mystic for me right now. Error: {str(e)}"}
            
    # Mock fallback
    return {
        "prediction": "I see a strong Life Line indicating exceptional vitality. Your Head Line slopes down towards the mounts, showing deep creativity. The Heart Line is very distinct, signifying passionate relationships and deep empathy. Financially, your Fate Line becomes very strong in your mid-30s."
    }

@app.post("/generate-chart")
def generate_chart(req: ChartRequest):
    try:
        # Step 1: Calculate Swiss Ephemeris data
        chart_data = engine.calculate_chart(req.date_of_birth, req.time_of_birth, req.latitude, req.longitude)
        
        # Step 2: Apply Rules Engine
        rules = AstroRulesEngine(chart_data)
        insights = rules.analyze()
        
        chart_data["insights"] = insights
        return chart_data
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/chat", response_model=ChatResponse)
def ai_astrologer_chat(req: ChatRequest):
    # Step 3 & 4: AI Interpretation Layer
    # We construct a prompt passing the structured rules
    
    chart = req.chart_context
    insights = chart.get("insights", [])
    
    insight_texts = [f"{i['title']}: {i['description']}" for i in insights]
    context_block = "\n".join(insight_texts)
    
    import os
    dataset_context = ""
    dataset_path = os.path.join(os.path.dirname(__file__), "vedic_astra_dataset.md")
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset_context = f.read()

    prompt = f"""
    You are a traditional Vedic astrologer. Use the following core Vedic Astrology dataset as your foundational knowledge base:
    <vedic_dataset>
    {dataset_context}
    </vedic_dataset>
    
    Explain the following structured astrology insights in a natural, authoritative, and personalized way based on the user's question.
    User Question: {req.message}
    
    Chart Insights to weave in:
    {context_block}
    
    Do not hallucinate. Provide comforting yet honest Vedic guidance strictly aligned with the provided dataset.
    """
    
    # In production, call `openai.ChatCompletion.create(...)`
    # We will return the mocked synthesized response for now 
    # to guarantee it works out-of-the-box without keys.
    
    prompt_used_indicator = "Insights used: " + ", ".join([i['title'] for i in insights])
    
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a traditional Vedic astrologer."},
                    {"role": "user", "content": prompt}
                ]
            )
            simulated_ai_reply = response.choices[0].message.content
        except Exception as e:
            simulated_ai_reply = f"(AI Error) {str(e)}"
    else:
        simulated_ai_reply = f"(AI Generated) Namaste. Looking at your chart... {prompt_used_indicator}. " + \
                             "Your question was: '" + req.message + "'. The celestial bodies indicate that patience is key right now. " + \
                             "The transits bring focus to the houses activated in your chart."

    return ChatResponse(
        reply=simulated_ai_reply,
        sources=[i['title'] for i in insights]
    )

@app.get("/daily-prediction")
def get_daily_prediction(lagna: str):
    if client:
        prompt = f"""
        Provide a short daily Vedic astrology prediction for a person with Lagna (Ascendant) in {lagna}.
        Output only a valid JSON object with the following keys: "Career", "Love", "Finance", "Health".
        Values should be short 1-2 sentence predictions.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception:
            pass # Fall back to mock
            
    # Step 5: Daily Prediction Engine mock
    return {
        "Career": f"Since your ascendant is {lagna}, focus on steady gains today. Avoid taking risky leaps.",
        "Love": "Venus is favorably positioned. Meaningful conversations will foster deep bonds.",
        "Finance": "Unexpected expenses could arise. Rely on your budget.",
        "Health": "Maintain hydration and do not ignore signs of fatigue."
    }
