#coding:utf-8
#-*-coding:utf8-*-
#qpy:pygame
import pygame,os,time
from pygame.locals import *

caracs="#"
diresave="dos/"
nfs='stats.nath'
nfp='params.nath'
if not diresave[:-1] in os.listdir():
    os.mkdir(diresave)

pygame.init()
TITRE="SimpleRace"
font=pygame.font.SysFont("Serif",20)
smenu=1
encour=True

class Joueur:
    def __init__(self):
        self.nom=""
        self.age=0
        self.smenu=2

def load():
    do=os.listdir(diresave)
    cc=caracs
    if not nfp in do:
        f=open(diresave+nfp,"w")
        f.write("1000"+cc+"750"+cc+"window"+cc+"0")
        f.close() 
    if not nfs in do:
        f=open(diresave+nfs,"w")
        f.write("player"+cc+"0"+cc+"0")
        f.close()
    fp=open(diresave+nfp,'r').read().split(caracs)
    fs=open(diresave+nfs,'r').read().split(caracs)
    j=Joueur()
    #params
    if len(fp)>0:j.tex=int(fp[0])
    else: j.p_tex=1000
    if len(fp)>1:j.tey=int(fp[1])
    else: j.p_tey=750
    if len(fp)>2:j.p_os=fp[2]
    else: j.p_os='windows'
    if len(fp)>3: j.p_vlp=int(fp[3])
    else: j.p_vlp=0
    #stats
    if len(fs)>0:j.p_nom=fs[0]
    else: j.p_nom="player"
    if len(fs)>1:j.p_age=int(fs[1])
    else: j.p_age=0
    if len(fs)>2:j.p_timep=int(fs[2])
    else: j.p_timep=0
    return j

def save(j):
    txp=str(j.tex)+caracs+str(j.tey)+caracs+j.p_os+caracs+str(j.p_vlp)
    txs=j.nom+caracs+str(j.age)+caracs+str(j.p_timep)
    f=open(nfp,'w')
    f.write(txp)
    f.close()
    f=open(nfs,'w')
    f.write(txs)
    f.close()

j=load()

def rx(x): return int(x/1000*j.tex)
def ry(y): return int(y/750*j.tey)

def button(text,x,y,tx,ty,cl,cl2,clt):
    tb=rx(3)
    x,y,tx,ty=rx(x),ry(y),rx(tx),ry(ty)
    b=pygame.draw.rect(fenetre,cl,(x,y,tx,ty),0)
    pygame.draw.rect(fenetre,cl2,(x,y,tx,ty),tb)
    fenetre.blit(pygame.transform.scale(font.render(text,20,clt),[tx-2*(tb+1),ty-2*(tb+1)]),[x+tb+1,y+tb+1])
    return b

def txt(txt,x,y): fenetre.blit(font.render(txt,20,clt),[rx(x),ry(y)])

def image(img,x,y,tx,ty): fenetre.blit(pygame.transform.scale(pygame.image.load("images/"+img),[rx(tx),ry(ty)]),[rx(x),ry(y)])

cf=(100,100,110)
clf=cf
clt=(0,0,0)
clb=(0,0,0)
tbs=(50,50,50)
tb=5

def aff(j):
    buttons=[]
    for x in range(11): buttons.append(0)
    fenetre.fill( cf )
    tbm1,tbm2,tbm3=clb,clb,clb
    if j.smenu==1: tbm1=tbs
    elif j.smenu==2: tbm2=tbs
    elif j.smenu==3: tbm3=tbs
    buttons[0]=button('cars',0,0,j.tex/3,100,(100,50,50),tbm1,clt)
    buttons[1]=button('home',j.tex/3,0,j.tex/3,100,(100,50,50),tbm2,clt)
    buttons[2]=button('settings',j.tex/3*2,0,j.tex/3,100,(100,50,50),tbm3,clt)
    if j.smenu==2: #home
        buttons[3]=button('play',450,400,100,50,(100,50,50),clb,clt)
    if j.smenu==3: #settings
        clp=[(250,0,0),(250,0,0),(250,0,0),(250,0,0)]
        clp[j.p_vlp]=(0,250,0)
        n=(0,0,0)
        txt("commande pour lancer : ",10,100)
        buttons[4]=button("os.system('python a.py')",100,120,200,70,clp[0],n,clt)    
        buttons[5]=button("os.system('python3 a.py')",300,120,200,70,clp[1],n,clt)    
        buttons[6]=button("subprocess.call('python a.py')",500,120,200,70,clp[2],n,clt)    
        buttons[7]=button("subprocess.call('python3 a.py')",700,120,200,70,clp[3],n,clt)    
        txt("résolution de l'ecran : "+str(j.tex)+" x "+str(j.tey),20,300)
        buttons[8]=button("augmenter la résolution",300,280,100,75,(100,40,130),n,clt)
        buttons[9]=button("reduire la resolution",500,280,100,75,(100,40,130),n,clt)
        if j.p_os=="windows": txb="Windows"
        else: txb="Linux"
        txt("Système d'exploitation : ",20,350)
        buttons[10]=button(txb,100,330,100,75,(30,145,132),clb,clt)
    pygame.display.update()
    return buttons

def wfc():
    fenetre.blit(font.render("Cliquez si votre parte est finie",20,(150,0,0)),[5,tey/2])
    cc=False
    while not cc:
        for event in pygame.event.get():
            if event.type==QUIT: encour,cc=False,True
            elif event.type==KEYDOWN:
                if event.key==K_q: encour,cc=False,True
            elif event.type==MOUSEBUTTONUP: cc=True

##

fenetre=pygame.display.set_mode([j.tex,j.tey])
pygame.display.set_caption(TITRE)

rr=10

while encour:
    buttons=aff(j)
    tt=time.time()
    for event in pygame.event.get():
        if event.type==QUIT:
            encour=False
        elif event.type==KEYDOWN:
            if event.key==K_q:
                encour=False
        elif event.type==MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            rpos=pygame.Rect(pos[0],pos[1],1,1)
            for b in buttons:
                try:
                    if rpos.colliderect(b):
                        ib=buttons.index(b)
                        if ib==0: j.smenu=1
                        if ib==1: j.smenu=2
                        if ib==2: j.smenu=3 
                        if ib==3:
                            if j.p_vlp==0: os.system("python a.py")
                            elif j.p_vlp==1: os.system("python3 a.py")
                            elif j.p_vlp==2:
                                import subprocess
                                subprocess.call("python a.py")
                            elif j.p_vlp==3:
                                import subprocess
                                subprocess.call("python3 a.py")
                            wfc()
                        if ib==4: j.p_vlp=0
                        if ib==5: j.p_vlp=1
                        if ib==6: j.p_vlp=2
                        if ib==7: j.p_vlp=3
                        if ib==8:
                            j.trx+=rr
                            j.ty+=rr/(1000/750)
                            fenetre=pygame.display.set_mode([j.tex,j.tey])
                        if ib==9:
                            j.trx-=rr
                            j.ty-=rr/(1000/750)
                            fenetre=pygame.display.set_mode([j.tex,j.tey])
                except: pass
    ttt=time.time()-tt
    pygame.draw.rect(fenetre,clf,(0,j.tey-35,100,35),0)
    fps=str(ttt/1.0)[:5]
    fenetre.blit(font.render("fps : "+fps,20,clt),[1,j.tey-30])
    j.p_timep+=ttt
    save(j)
                        
   




