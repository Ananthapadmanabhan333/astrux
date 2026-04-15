import urllib.request, json

data = json.dumps({
    'date_of_birth': '1995-10-24',
    'time_of_birth': '14:30',
    'latitude': 28.6139,
    'longitude': 77.2090
}).encode()

req = urllib.request.Request(
    'http://127.0.0.1:8000/generate-chart',
    data=data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=8) as r:
        parsed = json.loads(r.read().decode())
        print(f"SUCCESS — Insights: {len(parsed.get('insights',[]))}")
        print(f"Dasha Detail: {parsed.get('dasha_detail','')}")
        print(f"Timeline entries: {len(parsed.get('dasha_timeline',[]))}")
        print(f"House Lords: {parsed.get('house_lords','')}")
        print()
        for i in parsed.get('insights', []):
            print(f"  [{i['type']:12}] {i['title'][:80]}")
except urllib.error.HTTPError as e:
    print('FAIL:', e.read().decode())
except Exception as e:
    print('ERROR:', e)
