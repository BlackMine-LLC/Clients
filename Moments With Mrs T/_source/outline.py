import json,sys
src=sys.argv[1]
t=json.loads(open(src,encoding='utf-8').read())
root=t['result'][0]['data']
out=[]
def s(v): return json.dumps(v,ensure_ascii=False)
def walk(n,d):
    typ=n.get('type'); cls='.'.join(n.get('styleNames',[]) or [])
    if typ=='String':
        out.append('  '*d+'"'+n.get('textContent','')+'"'); return
    st=dict(n.get('settings',{}) or {})
    hid=st.get('visibility') is False
    for k in ['visibility','block']: st.pop(k,None)
    if st.get('tag') in ('div',) : st.pop('tag')
    extra=''
    if n.get('instanceDetails'): extra=' COMPONENT='+n['instanceDetails'].get('name','')
    for k in list(st):
        if st[k] in (None,'',[],{}): st.pop(k)
    line='  '*d+('[HIDDEN] ' if hid else '')+typ+('.'+cls if cls else '')+extra+((' '+s(st)) if st else '')
    if n.get('textContent') and typ!='String': line+=' "'+n['textContent']+'"'
    out.append(line)
    for c in n.get('children',[]) or []: walk(c,d+1)
walk(root,0)
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out))
print(len(out),'lines')
