import re,os,glob
pages={}
for f in glob.glob('**/*.html',recursive=True):
    url='/'+f.replace(os.sep,'/')[:-5]; url={'/index':'/'}.get(url,url); pages[url]=open(f,encoding='utf-8').read()
bad=set()
for u,h in pages.items():
    for m in re.findall(r'(?:href|src)="(/[^"#?]*)',h):
        p=m.rstrip('/') or '/'
        if p in pages or os.path.exists('.'+m): continue
        bad.add((u,m))
    if 'lorem' in h.lower(): bad.add((u,'LOREM'))
    if h.count('<h1')!=1: bad.add((u,'h1 count %d'%h.count('<h1')))
print('pages',len(pages)); print('problems',sorted(bad) or 'none')
