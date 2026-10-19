import json,sys,urllib.parse,urllib.request
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 6
u="https://api.openalex.org/works?search="+urllib.parse.quote(q)+f"&per-page={n}&mailto=quipu@example.org"
d=json.load(urllib.request.urlopen(u,timeout=60))
for w in d["results"]:
    ab=w.get("abstract_inverted_index")
    txt=""
    if ab:
        pos={}
        for word,idx in ab.items():
            for i in idx: pos[i]=word
        txt=" ".join(pos[i] for i in sorted(pos))[:400]
    print(f"{w['publication_year']} | {w['display_name'][:120]} | {w.get('doi')}")
    print("   ",txt.replace("\n"," "))
