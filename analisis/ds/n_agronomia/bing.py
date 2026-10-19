import sys,re,html,urllib.parse,subprocess
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 4
u="https://www.bing.com/search?q="+urllib.parse.quote(q)
t=subprocess.run(["curl","-s","-m","30","-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64)",u],capture_output=True).stdout.decode('utf-8','replace')
for b in re.findall(r'<li class="b_algo".*?</li>',t,re.S)[:n]:
    s=html.unescape(re.sub('<[^>]+>',' ',b)); print("*",' '.join(s.split())[:300])
