#!/usr/bin/env python3
"""Full public-safety scan of everything that deploys."""
import os,re,json,struct,sys
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE=os.path.join(REPO,"public")
F=[]
def add(sev,where,what,detail=""): F.append((sev,where,what,detail))

# ---------- 1. exactly what deploys ----------
dep=[]
for dp,dns,fns in os.walk(SITE):
    for fn in fns: dep.append(os.path.relpath(os.path.join(dp,fn),SITE))
dep.sort()
notsite=[f for f in os.listdir(REPO) if f not in {"public",".git"}]

# ---------- 2. sensitive content ----------
PAT=[("HIGH","employer/program/award named",r"\b(jewish family service|jfs|k'?vod|tristate association|outstanding project in the field)\b"),
     ("HIGH","colleague or partner named",r"\b(june|ann|russ conrad|melissa sterling|kenwood|the summit|the seasons)\b"),
     ("HIGH","credential-shaped",r"(api[_-]?key|client[_-]secret|password\s*=|bearer\s+[A-Za-z0-9]{8}|ghp_|xox[baprs]-)"),
     ("HIGH","money figure",r"\$\s?\d[\d,]{2,}"),
     ("HIGH","phone or street address",r"(\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b|\b\d{1,5}\s+[A-Z][a-z]+\s+(Street|Avenue|Road|Drive)\b)"),
     ("MED","personal gmail exposed",r"yairwalton@gmail\.com"),
     ("MED","family name detail",r"(my wife,?\s+[A-Z][a-z]+|daughter,?\s+[A-Z][a-z]+)"),
     # brand guardrails
     ("HIGH","banned word (ownership/consulting)",r"\b(founder|founded|my program|my model|available for consulting|licensing|national replication)\b"),
     ("HIGH","banned word (pastor)",r"\b(pastor|pastoral)\b"),
     ("MED","em or en dash",r"[–—]")]
TEXT={".html",".md",".txt",".xml",".css",".json",".webmanifest",".js",".svg"}
for rel in dep:
    if os.path.splitext(rel)[1].lower() not in TEXT: continue
    b=open(os.path.join(SITE,rel),encoding="utf-8",errors="replace").read()
    for sev,what,pat in PAT:
        for m in re.finditer(pat,b,re.I):
            ln=b[:m.start()].count("\n")+1
            add(sev,f"{rel}:{ln}",what,b.splitlines()[ln-1].strip()[:90])

# ---------- 3. html comments are public ----------
for rel in [d for d in dep if d.endswith(".html")]:
    b=open(os.path.join(SITE,rel),encoding="utf-8").read()
    for m in re.finditer(r"<!--(.*?)-->",b,re.S):
        c=m.group(1)
        if re.search(r"\b(jfs|k'?vod|june|ann|employer|secret|password|internal|private)\b",c,re.I):
            add("HIGH",f"{rel}:{b[:m.start()].count(chr(10))+1}","sensitive HTML comment",c.strip()[:90])

# ---------- 4. image metadata ----------
for rel in dep:
    e=os.path.splitext(rel)[1].lower(); p=os.path.join(SITE,rel)
    if e==".webp":
        d=open(p,'rb').read(); i=12; ch=[]
        while i+8<=len(d):
            c=d[i:i+4].decode('ascii','replace'); sz=struct.unpack('<I',d[i+4:i+8])[0]
            ch.append(c); i+=8+sz+(sz&1)
        bad=[c for c in ch if c in {'EXIF','XMP ','ICCP'}]
        if bad: add("HIGH",rel,"image metadata present",str(bad))
    elif e==".png":
        d=open(p,'rb').read(); i=8; ch=[]
        while i+8<=len(d):
            sz=struct.unpack('>I',d[i:i+4])[0]; c=d[i+4:i+8].decode('ascii','replace')
            ch.append(c); i+=12+sz
            if c=='IEND': break
        bad=[c for c in ch if c in {'tEXt','iTXt','zTXt','eXIf','tIME'}]
        if bad: add("HIGH",rel,"image metadata present",str(bad))

# ---------- 5. the three copies must agree ----------
html=open(os.path.join(SITE,"index.html"),encoding="utf-8").read()
md=open(os.path.join(SITE,"index.md"),encoding="utf-8").read()
llms=open(os.path.join(SITE,"llms.txt"),encoding="utf-8").read()
for label,pat in [("reach figure",r"more than ([\d,]+) people"),
                  ("launch year",r"since (\d{4})"),
                  ("ordination year",r"Hebrew Union College in (\d{4})")]:
    vals={}
    for nm,txt in [("index.html",html),("index.md",md),("llms.txt",llms)]:
        m=re.search(pat,txt); vals[nm]=m.group(1) if m else None
    uniq={v for v in vals.values() if v}
    if len(uniq)>1: add("HIGH","content drift",f"{label} disagrees across copies",str(vals))
APPROVED={"reach":"1,200","launch":"2020"}
m=re.search(r"more than ([\d,]+) people",html)
if m and m.group(1)!=APPROVED["reach"]:
    add("HIGH","index.html","reach figure is not the approved public number",m.group(1))
m=re.search(r"more than [\d,]+ people\s+since (\d{4})",re.sub(r"\s+"," ",html))
if m and m.group(1)!=APPROVED["launch"]:
    add("HIGH","index.html","launch year is not the approved one",m.group(1))

# ---------- 6. structured data ----------
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',html,re.S):
    try: json.loads(m.group(1))
    except Exception as ex: add("HIGH","index.html","JSON-LD does not parse",str(ex)[:80])

# ---------- 7. every outbound destination ----------
dest=set()
for rel in [d for d in dep if d.endswith((".html",".md",".txt"))]:
    b=open(os.path.join(SITE,rel),encoding="utf-8").read()
    for u in re.findall(r'https?://[^\s"\'<>)]+',b): dest.add(u.split("/")[2])
    for e in re.findall(r'mailto:([^\s"\'<>?]+)',b): dest.add("mailto:"+e)

# ---------- 8. robots internal consistency (repo copy only) ----------
rb=open(os.path.join(SITE,"robots.txt"),encoding="utf-8").read()
g={};cur=[];prev=False
for raw in rb.splitlines():
    l=raw.split("#")[0].strip()
    if not l: continue
    k,_,v=l.partition(":");k=k.strip().lower();v=v.strip()
    if k=="sitemap": continue
    if k=="user-agent":
        if not prev: cur=[]
        cur.append(v); g.setdefault(v,[]); prev=True
    else:
        for u in cur: g[u].append((k,v))
        prev=False
for ua,r in g.items():
    if [v for k,v in r if k=="allow"] and [v for k,v in r if k=="disallow"]:
        add("HIGH","robots.txt",f"{ua} has both Allow and Disallow")

print("="*72)
print(f"DEPLOYED: {len(dep)} files in public/")
print(f"NOT DEPLOYED (repo root): {', '.join(sorted(notsite))}")
print(f"\nOUTBOUND DESTINATIONS ({len(dest)}):")
for d in sorted(dest): print(f"   {d}")
print("\nROBOTS GROUPS (repo copy):")
for ua,r in g.items():
    print(f"   {ua:<16}{[f'{k}:{v}' for k,v in r]}")
print("\n"+"="*72)
o={"HIGH":0,"MED":1,"LOW":2}
F.sort(key=lambda x:(o[x[0]],x[1]))
for sev,w,what,d in F: print(f"[{sev}] {w}\n      {what}\n      {d}\n")
print(f"{len([f for f in F if f[0]=='HIGH'])} high, {len([f for f in F if f[0]=='MED'])} med")
