# SNAKE for CASIO fx-CG100 (MicroPython 1.9.4 + casioplot)
# Arrows: steer   OK: pause   Left/Right on card: speed   AC: quit
from casioplot import *
from random import randint

# Key codes = row*10+col from the manual's keypad figure.
# ponytail: verify on device, change these numbers if a key does nothing
UP,LEFT,RIGHT,DOWN,OK=14,23,25,34,24
DIRS={UP:(0,-1),DOWN:(0,1),LEFT:(-1,0),RIGHT:(1,0)}

# No clock on the calc. getkey() is not a clock either: it returns faster while
# a key is held, so each step samples keys SLICES times and busy-waits between.
# ponytail: TICK is the calibration knob, raise it if the game is too fast
TICK=2000
SLICES=4

W=31    # board columns (tiles are 12x12 px)
H=14    # board rows
X0=6    # board top-left px
Y0=18

BG=((170,215,81),(162,209,73))
HUD=(74,117,44)
FRAME=(87,138,52)
BLUE=(78,124,246)
DARK=(25,35,80)
WHITE=(255,255,255)
CARD=(77,170,240)
R=(1,0)

def art(rows,cmap):
  return tuple((i,j,cmap[rows[j][i]]) for j in range(len(rows)) for i in range(len(rows[j])) if rows[j][i]!=".")

APPLE=art((
  "......s.ll..",
  "......sll...",
  "...rrrsrrr..",
  "..rrrrrrrrr.",
  ".rrwwrrrrrrr",
  ".rrwrrrrrrrr",
  ".rrrrrrrrrrr",
  ".rrrrrrrrrrr",
  ".rrrrrrrrrrr",
  "..rrrrrrrrr.",
  "...rrrrrrr..",
  "....rr.rr..."),
  {"r":(231,71,29),"w":(250,160,130),"s":(100,60,20),"l":(90,170,40)})
TROPHY=art((
  "gggggggggg",
  "g.gggggg.g",
  "g.gggggg.g",
  ".gggggggg.",
  "..gggggg..",
  "...gggg...",
  "....gg....",
  "....gg....",
  "...gggg...",
  "..gggggg.."),
  {"g":(250,195,40)})

# Snake pieces, precomputed so the game loop allocates nothing
# (MicroPython pauses to garbage-collect when the loop creates objects).
SQ=tuple((i,j) for j in range(1,11) for i in range(1,11))
STRIP={(1,0):tuple((11,j) for j in range(1,11)),(-1,0):tuple((0,j) for j in range(1,11)),
  (0,1):tuple((i,11) for i in range(1,11)),(0,-1):tuple((i,0) for i in range(1,11))}
OPP={(1,0):(-1,0),(-1,0):(1,0),(0,1):(0,-1),(0,-1):(0,1)}
DEL={1:(1,0),-1:(-1,0),W:(0,1),-W:(0,-1)}

def rot(d,u,v):
  # head is designed facing right (u = forward, v = across); turn it to face d
  if d==(1,0):
    return u,v
  if d==(-1,0):
    return 11-u,v
  if d==(0,1):
    return v,u
  return v,11-u

HEADPX={}
HEADFIX={}
for d in OPP:
  px=[]
  fix=[]
  for u in range(1,11):
    for v in range(1,11):
      x,y=rot(d,u,v)
      if u==10 and v in (1,10):
        fix.append((x,y))
        continue
      eye=6<=u<=9 and (1<=v<=4 or 7<=v<=10) and not (u in (6,9) and v in (1,4,7,10))
      pupil=8<=u<=9 and v in (2,3,8,9)
      col=DARK if pupil else (WHITE if eye else BLUE)
      px.append((x,y,col))
      if col!=BLUE:
        fix.append((x,y))
  HEADPX[d]=tuple(px)
  HEADFIX[d]=tuple(fix)
CARDCELLS=tuple(r*W+c for r in range(2,10) for c in range(8,23))

def cx(c):
  return X0+c%W*12
def cy(c):
  return Y0+c//W*12

def rect(x,y,w,h,col):
  sp=set_pixel
  for j in range(y,y+h):
    for i in range(x,x+w):
      sp(i,j,col)

def tile(c):
  rect(cx(c),cy(c),12,12,BG[(c%W+c//W)%2])

def paint(c,pts,col):
  sp=set_pixel
  x=cx(c)
  y=cy(c)
  for i,j in pts:
    sp(x+i,y+j,col)

def draw(x,y,pts):
  sp=set_pixel
  for i,j,col in pts:
    sp(x+i,y+j,col)

def link(a,b,d):
  paint(a,STRIP[d],BLUE)
  paint(b,STRIP[OPP[d]],BLUE)

def snake(body,d):
  for k in range(len(body)-1):
    paint(body[k],SQ,BLUE)
    link(body[k],body[k+1],DEL[body[k+1]-body[k]])
  draw(cx(body[-1]),cy(body[-1]),HEADPX[d])

def deadeyes(c,d):
  paint(c,HEADFIX[d],BLUE)
  for v0 in (1,7):
    for k in range(4):
      for v in (v0+k,v0+3-k):
        i,j=rot(d,6+k,v)
        set_pixel(cx(c)+i,cy(c)+j,DARK)

def place(occ):
  while True:
    c=randint(0,W*H-1)
    if c not in occ:
      return c

def waitkey():
  # wait for release, then a fresh press; randint stirs the RNG with human timing
  while getkey():
    pass
  k=0
  while not k:
    k=getkey()
    randint(0,1)
  return k

def card(msg,score,best,lvl):
  x=102
  y=42
  for j in range(96):
    a=2 if j in (0,95) else (1 if j in (1,94) else 0)
    rect(x+a,y+j,180-2*a,1,CARD)
  draw_string(x+12,y+6,msg,WHITE,"large")
  draw(x+12,y+33,APPLE)
  draw_string(x+28,y+33,str(score),WHITE)
  draw(x+92,y+34,TROPHY)
  draw_string(x+108,y+33,str(best),WHITE)
  draw_string(x+12,y+76,"OK: play",WHITE)
  while True:
    s="Speed < "+str(lvl)+" >"
    draw_string(x+12,y+55,s,DARK)
    show_screen()
    k=waitkey()
    draw_string(x+12,y+55,s,CARD)
    if k==LEFT and lvl>1:
      lvl-=1
    elif k==RIGHT and lvl<9:
      lvl+=1
    elif k not in DIRS:
      return lvl

def play(lvl):
  m=H//2*W
  body=[m+2,m+3,m+4,m+5]
  occ=set(body)
  food=m+W-8
  snake(body,R)
  draw(cx(food),cy(food),APPLE)
  show_screen()
  d=R
  while True:
    k=waitkey()
    if k in DIRS and k!=LEFT:
      d=DIRS[k]
      break
  hd=body[-1]
  hdir=R
  score=0
  q=[]
  last=k
  wait=int(TICK*1.6**(9-lvl))
  while True:
    # wait out the step while collecting turns (max 2 queued, no reversing)
    i=SLICES
    while i:
      i-=1
      j=wait
      while j:
        j-=1
      k=getkey()
      if k!=last:
        last=k
        if k in DIRS:
          p=q[-1] if q else d
          v=DIRS[k]
          if len(q)<2 and v!=p and v!=OPP[p]:
            q.append(v)
        elif k==OK:
          draw_string(300,3,"PAUSED",WHITE)
          show_screen()
          while waitkey()!=OK:
            pass
          draw_string(300,3,"PAUSED",HUD)
          show_screen()
          last=OK
    if q:
      d=q.pop(0)
    hx=hd%W+d[0]
    hy=hd//W+d[1]
    c=hy*W+hx
    grow=c==food
    if not grow:
      t=body.pop(0)
      occ.remove(t)
      # erase only the old tail's snake pixels, not the whole tile
      nt=body[0]
      g=BG[(t%W+t//W)%2]
      paint(t,SQ,g)
      paint(t,STRIP[DEL[nt-t]],g)
      paint(nt,STRIP[DEL[t-nt]],BG[(nt%W+nt//W)%2])
    if hx<0 or hx>=W or hy<0 or hy>=H or c in occ:
      deadeyes(hd,hdir)
      show_screen()
      return score,body,food,"GAME OVER"
    paint(hd,HEADFIX[hdir],BLUE)
    if grow:
      tile(c)
    draw(cx(c),cy(c),HEADPX[d])
    link(hd,c,d)
    body.append(c)
    occ.add(c)
    hd=c
    hdir=d
    if grow:
      draw_string(22,3,str(score),HUD)
      score+=1
      draw_string(22,3,str(score),WHITE)
      if len(body)==W*H:
        show_screen()
        return score,body,food,"YOU WIN!"
      food=place(occ)
      draw(cx(food),cy(food),APPLE)
    show_screen()

clear_screen()
rect(0,0,384,18,HUD)
rect(0,18,6,174,FRAME)
rect(378,18,6,174,FRAME)
rect(6,186,372,6,FRAME)
for c in range(W*H):
  tile(c)
draw(6,3,APPLE)
draw(80,4,TROPHY)
draw_string(22,3,"0",WHITE)
draw_string(96,3,"0",WHITE)
best=0
lvl=6
score=0
msg="SNAKE"
dirty=[]
while True:
  lvl=card(msg,score,best,lvl)
  for c in set(CARDCELLS+tuple(dirty)):
    tile(c)
  draw_string(22,3,str(score),HUD)
  draw_string(22,3,"0",WHITE)
  score,body,food,msg=play(lvl)
  dirty=body+[food]
  if score>best:
    draw_string(96,3,str(best),HUD)
    best=score
    draw_string(96,3,str(best),WHITE)
