from astro_engine import AstroEngine
from rules import AstroRulesEngine

e = AstroEngine()
chart = e.calculate_chart('1995-10-24', '14:30', 28.6139, 77.2090)
r = AstroRulesEngine(chart)
insights = r.analyze()
print(f'Total insights generated: {len(insights)}')
print()
for i in insights:
    t = i["type"].upper()
    title = i["title"]
    desc = i["description"][:120]
    print(f'[{t:12}] {title}')
    print(f'               {desc}...')
    print()
