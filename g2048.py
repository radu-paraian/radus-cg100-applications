# 2048 for CASIO fx-CG100 (MicroPython 1.9.4 + casioplot)
# Arrows: slide   OK: new game   other key: animation on/off   AC: quit
from casioplot import *
from random import randint

# Key codes = row*10+col from the manual's keypad figure.
UP,LEFT,RIGHT,DOWN,OK=14,23,25,34,24

# Slide speed: animation frames per board square a tile travels. Every frame
# costs about the same, so slides stay even. ponytail: set 1 if laggy, 3 for smoother
STEPS=2

X0=6    # board top-left px; 4 tiles of 40px with 4px gaps = 180px
Y0=6
PX=288  # centre x of the right-hand panel

WHITE=(255,255,255)
BOARD=(187,173,160)
DARKT=(119,110,101)
LIGHTT=(249,246,242)
LABEL=(238,228,218)
SUPER=(60,58,50)
EMPTY=(205,193,180)
COLORS={0:EMPTY,2:(238,228,218),4:(237,224,200),8:(242,177,121),
  16:(245,149,99),32:(246,124,95),64:(246,94,59),128:(237,207,114),
  256:(237,204,97),512:(237,200,80),1024:(237,197,63),2048:(237,194,46)}
FILL={c:(c,)*40 for c in list(COLORS.values())+[SUPER]}
INSET=tuple(2 if j in (0,39) else (1 if j in (1,38) else 0) for j in range(40))
# UNDER[m] = the 40 board colours across a strip at offset m (0..43) along a row/column
UNDER=tuple(tuple(BOARD if m>=40 or m<INSET[j] or m>=40-INSET[j] else EMPTY for j in range(40)) for m in range(44))
ROWS=[[r*4+c for c in range(4)] for r in range(4)]
COLS=[[r*4+c for r in range(4)] for c in range(4)]
LINES={LEFT:ROWS,RIGHT:[[l[3-k] for k in range(4)] for l in ROWS],
  UP:COLS,DOWN:[[l[3-k] for k in range(4)] for l in COLS]}

def measure(size):
  # the manual gives no font sizes, so measure ink of "8" and "88" once
  r=[]
  for s in ("8","88"):
    clear_screen()
    draw_string(0,0,s,(0,0,0),size)
    w=h=0
    for y in range(32):
      for x in range(64):
        p=get_pixel(x,y)
        if p and p[0]<128:
          w=max(w,x+1)
          h=max(h,y+1)
    r.append(w)
  return (size,r[0],r[1]-r[0],h)

FONTS=[measure(s) for s in ("large","medium","small")]

def text(cx,cy,s,col,maxw,f=0):
  # draw s centred on (cx,cy) in the largest font (from FONTS[f]) that fits maxw
  while f<2 and FONTS[f][1]+(len(s)-1)*FONTS[f][2]>maxw:
    f+=1
  size,ink,adv,h=FONTS[f]
  w=ink+(len(s)-1)*adv
  draw_string(cx-w//2,cy-h//2,s,col,size)

def rrect(x,y,w,h,col):
  sp=set_pixel
  for j in range(h):
    a=2 if j in (0,h-1) else (1 if j in (1,h-2) else 0)
    for i in range(x+a,x+w-a):
      sp(i,y+j,col)

def cx(i):
  return X0+4+i%4*44
def cy(i):
  return Y0+4+i//4*44

def cell(i,v):
  sp=set_pixel
  x=cx(i)
  y=cy(i)
  col=COLORS.get(v,SUPER)
  for j in range(40):
    a=INSET[j]
    for k in range(x+a,x+40-a):
      sp(k,y+j,col)
    for k in range(a):
      sp(x+k,y+j,BOARD)
      sp(x+39-k,y+j,BOARD)
  if v:
    text(x+20,y+20,str(v),DARKT if v<8 else LIGHTT,36)

def strip(t0,t1,c,h,fill,org):
  # paint along-range [t0,t1) of a 40px row (h) or column strip at across c with
  # fill (40 colours); fill=None restores the board (org = board origin on that axis)
  sp=set_pixel
  for t in range(t0,t1):
    cs=fill or UNDER[(t-org)%44]
    j=c
    if h:
      for k in cs:
        sp(t,j,k)
        j+=1
    else:
      for k in cs:
        sp(j,t,k)
        j+=1

def edge(t,c,h,org,col,u):
  # repaint the rounded-corner pixels of strip column t, at offset u in its tile
  sp=set_pixel
  un=UNDER[(t-org)%44]
  for j in ((0,1,38,39) if u in (0,39) else (0,39)):
    k=col or un[j]
    if h:
      sp(t,c+j,k)
    else:
      sp(c+j,t,k)

def slide(mv):
  # everything per tile is computed once here so the frames allocate (almost) nothing
  n=len(mv)
  fr=1
  T=[]
  for k in range(n):
    a,z,v=mv[k]
    h=a//4==z//4
    d=abs(z-a)//(1 if h else 4)
    fr=max(fr,d*STEPS)
    col=COLORS.get(v,SUPER)
    T.append((h,1 if z>a else -1,X0+4 if h else Y0+4,cx(a) if h else cy(a),
      cy(a) if h else cx(a),d*44,col,FILL[col],str(v),DARKT if v<8 else LIGHTT,
      k+1<n and mv[k+1][1]==z))
  pos=[0]*n
  for f in range(1,fr+1):
    for k in range(n):
      h,sg,org,A,c,dist,col,fill,s,tc,pt=T[k]
      p0=A+sg*pos[k]
      pos[k]=dist*f//fr
      p1=A+sg*pos[k]
      text(p0+20 if h else c+20,c+20 if h else p0+20,s,col,36)
      # trail = old body minus new body, lead = new body minus old body
      if sg>0:
        t0,t1,l0,l1=p0,min(p1,p0+40),max(p0+40,p1),p1+40
      else:
        t0,t1,l0,l1=max(p1+40,p0),p0+40,p1,min(p0,p1+40)
      if pt:
        # merge partner slides in behind: don't erase the part it now covers
        q=T[k+1][3]+sg*(T[k+1][5]*f//fr)
        strip(t0,min(t1,q),c,h,None,org)
        strip(max(t0,q+40),t1,c,h,None,org)
      else:
        strip(t0,t1,c,h,None,org)
      strip(l0,l1,c,h,fill,org)
      # keep corners round: fill old edge columns now inside the tile, then cut
      # the new edge columns (not the back one if the merge partner is behind it)
      for u in (0,1,38,39):
        if p1<=p0+u<p1+40:
          edge(p0+u,c,h,org,col,u)
      for u in (0,1,38,39):
        if not (pt and (u<2)==(sg>0)):
          edge(p1+u,c,h,org,None,u)
      text(p1+20 if h else c+20,c+20 if h else p1+20,s,tc,36)
    show_screen()

def move(b,d):
  # returns new board, points gained, tile moves (from,to,value), merge cells
  nb=b[:]
  gain=0
  mv=[]
  mg=[]
  for line in LINES[d]:
    t=[p for p in range(4) if b[line[p]]]
    for p in range(4):
      nb[line[p]]=0
    out=0
    k=0
    while k<len(t):
      p=t[k]
      v=b[line[p]]
      if p!=out:
        mv.append((line[p],line[out],v))
      if k+1<len(t) and b[line[t[k+1]]]==v:
        mv.append((line[t[k+1]],line[out],v))
        mg.append(line[out])
        nb[line[out]]=v*2
        gain+=v*2
        k+=2
      else:
        nb[line[out]]=v
        k+=1
      out+=1
  return nb,gain,mv,mg

def spawn(b):
  empty=[i for i in range(16) if not b[i]]
  i=empty[randint(0,len(empty)-1)]
  b[i]=4 if randint(1,10)==1 else 2
  return i

def stuck(b):
  return all(move(b,d)[0]==b for d in LINES)

def waitkey():
  # wait for release, then a fresh press; randint stirs the RNG with human timing
  while getkey():
    pass
  k=0
  while not k:
    k=getkey()
    randint(0,1)
  return k

def setnum(x,old,new):
  text(x,70,str(old),BOARD,80)
  text(x,70,str(new),WHITE,80)

msgtxt=""

def msg(s,col=DARKT):
  global msgtxt
  text(PX,170,msgtxt,WHITE,184,1)
  text(PX,170,s,col,184,1)
  msgtxt=s

clear_screen()
rrect(X0,Y0,180,180,BOARD)
text(PX,20,"2048",DARKT,184)
for x,label in ((240,"SCORE"),(336,"BEST")):
  rrect(x-44,40,88,44,BOARD)
  text(x,50,label,LABEL,80,2)
  text(x,70,"0",WHITE,80)
for y,t in ((104,"Arrows: slide tiles"),(122,"OK: new game"),(140,"AC: quit")):
  text(PX,y,t,DARKT,184,1)
best=0
score=0
anim=True
while True:
  b=[0]*16
  spawn(b)
  spawn(b)
  for i in range(16):
    cell(i,b[i])
  setnum(240,score,0)
  score=0
  msg("")
  won=False
  while True:
    show_screen()
    k=waitkey()
    if k==OK:
      msg("New game? Press OK")
      show_screen()
      if waitkey()==OK:
        break
      msg("")
      continue
    if k not in LINES:
      anim=not anim
      msg("Animation "+("on" if anim else "off"))
      continue
    nb,gain,mv,mg=move(b,k)
    if nb==b:
      continue
    if anim:
      slide(mv)
      for i in mg:
        cell(i,nb[i])
    else:
      for i in range(16):
        if nb[i]!=b[i]:
          cell(i,nb[i])
    b=nb
    if gain:
      setnum(240,score,score+gain)
      score+=gain
      if score>best:
        setnum(336,best,score)
        best=score
    show_screen()
    # new tile appears after the slide, like the original
    i=spawn(b)
    if anim:
      rrect(cx(i)+10,cy(i)+10,20,20,COLORS[b[i]])
      show_screen()
    cell(i,b[i])
    if msgtxt.startswith("Animation"):
      msg("")
    if not won and 2048 in b:
      won=True
      msg("You win! Keep going",(237,194,46))
    if stuck(b):
      msg("Game over! OK: again",(246,94,59))
      show_screen()
      while waitkey()!=OK:
        pass
      break
