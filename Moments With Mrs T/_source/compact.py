import json,sys
t=json.loads(open(sys.argv[1],encoding='utf-8').read())
root=t['result'][0]['data']
out=[]
def txt(n):
    if n.get('type')=='String': return n.get('textContent','')
    if n.get('type')=='' : return ' / '
    return ''.join(txt(c) for c in n.get('children',[]) or [])
TEXTY={'Heading','Paragraph','Link','Block','ListItem','Span','RichText','Blockquote','FormButton','FormBlockLabel','TextBlock','NavbarLink','Strong','Emphasis','Superscript','Subscript'}
def walk(n,d,hidden=False):
    typ=n.get('type'); st=n.get('settings',{}) or {}
    hid=hidden or st.get('visibility') is False
    cls=','.join(n.get('styleNames',[]) or [])
    pre=('  '*d)+('[H]' if hid else '')
    if typ=='ComponentInstance': out.append(pre+'<<'+n['instanceDetails']['name']+'>>'); return
    if typ in ('Section',) or (typ=='Block' and st.get('tag') in ('section','header','footer')):
        out.append(pre+'=== SECTION '+cls+' '+json.dumps(n.get('attributes',{})))
    if typ=='Image': out.append(pre+'IMG '+str(st.get('assetId'))+' alt='+str(st.get('altText','')) + ' ['+cls+']'); return
    if typ=='Video' or typ=='BackgroundVideoWrapper': out.append(pre+typ+' '+json.dumps(st)[:300])
    if typ in ('HtmlEmbed',): out.append(pre+'EMBED ['+cls+'] '+json.dumps(st)[:300]); return
    if typ=='DOM' and st.get('tag') in ('svg','path'): return
    if typ=='DOM' and st.get('tag')=='img': a=dict(n.get('attributes',{})); a['src']=a.get('src','')[:40]; out.append(pre+'DOMIMG '+json.dumps(a)); return
    if typ=='DOM' and st.get('tag')=='iframe': out.append(pre+'IFRAME '+json.dumps(n.get('attributes',{}))); return
    if typ and typ.startswith('Form'): 
        out.append(pre+typ+' ['+cls+'] '+json.dumps({k:v for k,v in st.items() if k not in('visibility',)})[:250]+' '+json.dumps(n.get('attributes',{}))[:200])
    if typ.startswith('Dynamo'): out.append(pre+typ+' '+json.dumps({k:v for k,v in st.items() if k!='visibility'})[:300])
    link=st.get('link')
    kids=n.get('children',[]) or []
    INL=('String','','Span','Strong','Emphasis','Emphasized','Superscript','Subscript','Link','LineBreak','Italic','Bold')
    def inl(c): return c.get('type') in INL and all(inl(k) for k in c.get('children',[]) or [])
    simple=kids and all(inl(c) for c in kids)
    if simple:
        tag=st.get('tag') or typ
        s=pre+tag+(' ['+cls+']' if cls else '')+(' LINK='+json.dumps(link) if link else '')+': '+txt(n).strip()
        out.append(s); return
    if link: out.append(pre+'LINK '+typ+' ['+cls+'] '+json.dumps(link))
    for c in kids: walk(c,d+1,hid)
walk(root,0)
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out))
