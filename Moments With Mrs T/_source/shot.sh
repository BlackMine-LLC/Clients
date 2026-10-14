#!/bin/bash
# usage: shot.sh <path> <width> <name>
P="C:/Users/Latre/AppData/Local/Temp/claude/mrst-chrome-$RANDOM"
OUTW="C:/Users/Latre/BlackMine-Studio/Moments With Mrs. T/_source/shots/$3.png"
timeout 60 "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --user-data-dir="$P" --no-first-run --disable-gpu --hide-scrollbars --virtual-time-budget=5000 --window-size=$2,${4:-12000} --screenshot="$OUTW" "http://localhost:4321$1" >/dev/null 2>&1
PYTHONUTF8=1 python - "$3" "$2" <<'PY'
import sys; from PIL import Image
n,w=sys.argv[1],int(sys.argv[2]); im=Image.open(f'_source/shots/{n}.png').convert('RGB')
px=im.load(); h=im.size[1]
# trim trailing blank rows (body bg after footer)
y=h-1
while y>0 and px[w//2,y]==px[w//2,h-1] and px[10,y]==px[10,h-1]: y-=1
im=im.crop((0,0,w,y+1)); h=im.size[1]
seg=1800 if w>800 else 1400
k=0
for t in range(0,h,seg):
    c=im.crop((0,t,w,min(h,t+seg))); s=760/w if w>800 else 1
    c.resize((int(w*s),int(c.size[1]*s))).save(f'_source/shots/{n}-{k}.jpg',quality=78); k+=1
print(n,'height',h,'parts',k)
PY
