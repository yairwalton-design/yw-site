import os, re, json, sys
REPO='/home/user/yw-site'
# the site lives in public/ once the build output directory is set; before that
# it was the repo root. follow whichever layout is actually present.
ROOT=os.path.join(REPO,'public') if os.path.isdir(os.path.join(REPO,'public')) else REPO
os.chdir(ROOT)
TOOLDIR=os.path.join(REPO,'tools')
issues=[]
def bad(f,msg): issues.append(f'{f}: {msg}')

PAGES=[f for f in os.listdir('.') if f.endswith('.html')]
TOOLS=[os.path.join(TOOLDIR,f) for f in os.listdir(TOOLDIR) if f.endswith('.html')] if os.path.isdir(TOOLDIR) else []
LINKED={'index.html','subscribe.html'}          # in the sitemap / nav
UNLINKED={'press.html','soon.html','404.html'}  # deliberately parked

for f in sorted(PAGES):
    t=open(f,encoding='utf-8').read()
    # --- head essentials ---
    if not t.lstrip().lower().startswith('<!doctype html>'): bad(f,'missing doctype')
    if '<html lang="en">' not in t: bad(f,'missing lang')
    if not re.search(r'<title>[^<]+</title>', t): bad(f,'missing/empty title')
    if 'name="viewport"' not in t: bad(f,'missing viewport')
    if 'name="description"' not in t: bad(f,'missing meta description')
    d=re.search(r'name="description" content="([^"]*)"',t)
    if d and not (50 <= len(d.group(1)) <= 165): bad(f,f'description length {len(d.group(1))} (want 50-165)')
    if f in LINKED and 'rel="canonical"' not in t: bad(f,'missing canonical')
    if f in UNLINKED and 'noindex' not in t: bad(f,'parked page missing noindex')
    if f in LINKED and 'noindex' in t: bad(f,'public page is set to noindex, it will not be found')
    if f in LINKED and 'content="index' not in t: bad(f,'public page does not explicitly ask to be indexed')
    # --- social ---
    if f in LINKED:
        for tag in ['og:title','og:description','og:url','og:image','og:image:width','og:image:height']:
            if f'property="{tag}"' not in t: bad(f,f'missing {tag}')
        for m in re.finditer(r'(?:og:image|twitter:image)" content="([^"]+)"',t):
            if not m.group(1).startswith('https://'): bad(f,f'social image not absolute: {m.group(1)}')
    # --- dashes / banned ---
    if '—' in t or '–' in t: bad(f,'contains em or en dash')
    body=re.sub(r'<head>.*?</head>','',t,flags=re.S)
    low=re.sub(r'<[^>]+>',' ',body).lower()
    for b in ['founder','founded','my program','my model','i built','pastoral','book a call','hire me']:
        if b in low: bad(f,f'banned phrase: {b}')
    # --- images ---
    for img in re.finditer(r'<img\b[^>]*>', t):
        tag=img.group(0)
        if 'alt=' not in tag: bad(f,'img without alt')
        if 'width=' not in tag or 'height=' not in tag: bad(f,'img without width/height (layout shift)')
    # --- local refs exist ---
    for m in re.finditer(r'(?:href|src)="([^"#:]+?)"', t):
        u=m.group(1)
        if u.startswith('//') or u.startswith('data:') or u.startswith('mailto:'): continue
        p=u.lstrip('/') or 'index.html'   # "/" is the site root
        if not os.path.exists(p): bad(f,f'broken local ref: {u}')
    # --- srcset ---
    for m in re.finditer(r'srcset="([^"]+)"', t):
        for part in m.group(1).split(','):
            u=part.strip().split(' ')[0]
            if u and not os.path.exists(u.lstrip('/')): bad(f,f'broken srcset ref: {u}')
    # --- in-page anchors resolve ---
    ids=set(re.findall(r'id="([^"]+)"',t))
    for m in re.finditer(r'href="#([^"]+)"',t):
        if m.group(1) not in ids: bad(f,f'dead anchor #{m.group(1)}')
    # --- cross-page anchors ---
    for m in re.finditer(r'href="/#([^"]+)"',t):
        idx=open('index.html',encoding='utf-8').read()
        if f'id="{m.group(1)}"' not in idx: bad(f,f'dead cross-page anchor /#{m.group(1)}')
    # --- headings ---
    if len(re.findall(r'<h1',t))!=1: bad(f,f'{len(re.findall(r"<h1",t))} h1 tags (want 1)')
    # --- JSON-LD ---
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
        try: json.loads(m.group(1))
        except Exception as e: bad(f,f'invalid JSON-LD: {e}')

# --- CSS refs ---
css=open('styles.css',encoding='utf-8').read()
for m in re.finditer(r"url\('([^']+)'\)", css):
    if not os.path.exists(m.group(1)): bad('styles.css',f'missing font: {m.group(1)}')
# classes used in HTML but absent from CSS
used=set()
for f in PAGES:
    for m in re.finditer(r'class="([^"]+)"', open(f,encoding='utf-8').read()):
        used.update(m.group(1).split())
inline_css=''.join(re.findall(r'<style>(.*?)</style>', ''.join(open(f,encoding='utf-8').read() for f in PAGES), re.S))
allcss=css+inline_css
for c in sorted(used):
    if not re.search(r'[.\w-]*\.'+re.escape(c)+r'[\s,{:.>]', allcss): bad('styles.css',f'class used but not styled: .{c}')

# --- sitemap vs pages ---
sm=open('sitemap.xml',encoding='utf-8').read()
for f in LINKED:
    slug='' if f=='index.html' else f
    if slug not in sm and f!='index.html': bad('sitemap.xml',f'linked page missing: {f}')
for f in UNLINKED:
    if f in sm: bad('sitemap.xml',f'parked page should not be listed: {f}')

# --- orphan assets ---
refs=set()
for f in PAGES+TOOLS+['styles.css','site.webmanifest']:
    txt=open(f,encoding='utf-8').read()
    refs.update(re.findall(r'assets/[\w./-]+', txt))
for dirpath,_,files in os.walk('assets'):
    for fn in files:
        p=os.path.join(dirpath,fn)
        if p not in refs: bad('assets',f'unreferenced file: {p}')

for f in TOOLS:
    t=open(f,encoding='utf-8').read()
    for m in re.finditer(r'(?:href|src)="(\.\./[^"#:]+)"', t):
        ref=m.group(1)
        # resolve relative to the file that contains it, not to the site root
        target=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(f)), ref))
        if not os.path.exists(target): bad(f, f'broken ref: {ref} -> {target}')

print(f'{len(issues)} issue(s)')
for i in issues: print('  -',i)
