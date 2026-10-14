import ast,sys
name,newfile=sys.argv[1],sys.argv[2]
src=open('build.py',encoding='utf-8').read(); lines=src.split('\n')
n=[x for x in ast.parse(src).body if isinstance(x,ast.FunctionDef) and x.name==name][0]
lines[n.lineno-1:n.end_lineno]=open(newfile,encoding='utf-8').read().rstrip('\n').split('\n')
open('build.py','w',encoding='utf-8').write('\n'.join(lines)); print('spliced',name)
