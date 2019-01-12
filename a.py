#coding:utf-8
import random,time,pygame
from pygame.locals import *


pygame.init()
font=pygame.font.SysFont("Serif",40)
fonte=pygame.font.SysFont("Serif",20)
tex,tey=1000,750

afffps=True

clt=(0,0,0)

nbv=5 #(en plus du joueur)
cam=[0,0]
voitures=[]

bots=[]

finits=[]

trcvs=[]

cltrc1=(5,15,5) #herbe
cltrc2=(15,15,15) #frein

encour=True

obtcs=[]

tprf=60
dtpr=time.time()

####

taille_circuit=random.randint(4000,26000) #(px)

nbob=random.randint(int(taille_circuit/120),int(taille_circuit/110))

maps=["mp_1.png","mp_1.png"]
imgmape=pygame.transform.scale(pygame.image.load("images/"+random.choice(maps)),[tex,taille_circuit+tey*4])

voits=[]
voits.append( ["Pierson v1",120,20,200,50,"v1.png",1000,10] )
voits.append( ["chagear",180,10,150,60,"v2.png",1000,10] )
voits.append( ["camior",80,5,100,70,"v3.png",800,1] )
voits.append( ["formoula2",250,35,50,70,"v4.png",8000,2] )
voits.append( ["bugive",80,55,80,40,"v5.png",2800,4] )
voits.append( ["tournay",95,25,400,50,"v6.png",400,4] )
voits.append( ["givebue",75,75,75,75,"v7.png",8000,3] )

vcts=[]

for vc in voits:
    for x in range(vc[7]): vcts.append( voits.index(vc) )

#0=nom 1=vit_max(px/s) 2=acc(px/s en + par sec) 3=man(px/s de droite-gauche) 4=frein(en px/s) 5=img 6=prix ( en neuros ) 7=chance de l'avoir (1-10 )

obs=[]
obs.append( ["boost","boost.png",True,50,"boost_tch.png"] )
obs.append( ["unboost","unboost.png",True,-50,"unboost_tch.png"] )
obs.append( ["flaque","flaque.png",False,0,"flaque_tch.png"] )

#0=nom 1=img 2=pmd 3=+vitesse 4=image quand touche

otx,oty=100,100

####
class Obstacle():
    def __init__(self,x,y,tp):
        self.tp=tp
        ob=obs[tp]
        self.nom=ob[0]
        self.px=x
        self.py=y
        self.tx=otx
        self.ty=oty
        self.image_ptch=pygame.transform.scale(pygame.image.load("images/"+ob[1]),[self.tx,self.ty])
        self.image_tch=pygame.transform.scale(pygame.image.load("images/"+ob[4]),[self.tx,self.ty])
        self.image=self.image_ptch
        self.pmd=ob[2]
        self.vitplus=ob[3]
    def touch(self):
        tch=False
        re=pygame.Rect(self.px,self.py,self.tx,self.ty)
        for v in voitures:
            if re.colliderect(pygame.Rect(v.px,v.py,v.tx,v.ty)):
                tch=True
                if self.pmd:
                    v.vit+=self.vitplus
                else:
                    v.vit=0
                    v.py-=1
        if tch: self.image=self.image_tch
        else: self.image=self.image_ptch

class Voiture:
    def __init__(self,x,y,tp):
        self.tp=tp
        vv=voits[tp]
        self.nom=vv[0]
        self.vit_max=float(vv[1])
        self.vit=0.0
        self.acc=float(vv[2])
        self.man=vv[3]
        self.frein=vv[4]
        self.px=x
        self.py=y
        self.tx=100
        self.ty=100
        self.img=pygame.transform.scale(pygame.image.load("images/"+vv[5]),[self.tx,self.ty])
        self.dac=time.time()
        self.dbg=time.time()
        self.dfr=time.time()
        self.az=10
        self.finit=False
        self.pos=None
        self.dts=time.time()
        self.anim_f=["an_f_0.png","an_f_1.png","an_f_2.png","an_f_3.png","an_f_4.png","an_f_5.png","an_f_6.png","an_f_7.png"]
        self.et_an=0
        self.danim=time.time()
        self.classement=0
        self.vinh=35
        self.ee=2
        self.rs=[[self.px+self.ee,self.py+self.ee],[self.px+self.ee,self.py+self.ty-self.ee],[self.px+self.tx-self.ee,self.py+self.ee],[self.px+self.tx-self.ee,self.py+self.ty-self.ee]]
    def accel(self):
        if time.time()-self.dac >= 1/self.az:
            self.dac=time.time()
            if self.vit < self.vit_max:
                self.vit+=self.acc/self.az
    def recul(self):
        if time.time()-self.dac >= 1/self.az:
            self.dac=time.time()
            if self.vit > -self.vit_max:
                self.vit-=self.acc/self.az
    def tourner(self,aa):
        if time.time()-self.dbg >= 1/self.az:
            self.dbg=time.time()
            if aa==1: self.px+=self.man/self.az
            else: self.px-=self.man/self.az
    def trace1(self):
        self.rs=[[self.px+self.ee,self.py+self.ee],[self.px+self.ee,self.py+self.ty-self.ee],[self.px+self.tx-self.ee,self.py+self.ee],[self.px+self.tx-self.ee,self.py+self.ty-self.ee]]
        if self.rs[0][0] < 100 or self.rs[0][0] > 900: trcvs.append( [cltrc1,self.rs[0][0],self.rs[0][1],self.ee,1] )
        if self.rs[1][0] < 100 or self.rs[1][0] > 900: trcvs.append( [cltrc1,self.rs[1][0],self.rs[1][1],self.ee,1] )
        if self.rs[2][0] < 100 or self.rs[2][0] > 900: trcvs.append( [cltrc1,self.rs[2][0],self.rs[2][1],self.ee,1] )
        if self.rs[3][0] < 100 or self.rs[3][0] > 900: trcvs.append( [cltrc1,self.rs[3][0],self.rs[3][1],self.ee,1] )
    def trace2(self):
        self.rs=[[self.px+self.ee,self.py+self.ee],[self.px+self.ee,self.py+self.ty-self.ee],[self.px+self.tx-self.ee,self.py+self.ee],[self.px+self.tx-self.ee,self.py+self.ty-self.ee]]
        trcvs.append( [cltrc2,self.rs[0][0],self.rs[0][1],self.ee,1] )
        trcvs.append( [cltrc2,self.rs[1][0],self.rs[1][1],self.ee,1] )
        trcvs.append( [cltrc2,self.rs[2][0],self.rs[2][1],self.ee,1] )
        trcvs.append( [cltrc2,self.rs[3][0],self.rs[3][1],self.ee,1] )
    def freine(self):
        self.trace2()
        if time.time()-self.dfr > 1/self.az:
            self.dfr=time.time()
            self.vit-=self.frein/self.az
            if self.vit <=0:
                self.vit = 0
    def collide(self):
        sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
        r0=sr.topleft     #en haut à gauche
        r1=sr.topright    #en haut à droite
        r2=sr.midleft     #au milieu à gauche
        r3=sr.midright    #au milieu à droite
        r4=sr.bottomleft  #en bas à gauche
        r5=sr.bottomright #en bas à droite
        r6=sr.midtop      #au milieu en haut
        r7=sr.midbottom   #au milieur en bas
        for v in voitures:
            vr=pygame.Rect(v.px,v.py,v.tx,v.ty)
            if v!=self and sr.colliderect(vr):
                while vr.collidepoint(r0):
                    self.py+=1
                    self.px+=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r0=sr.topleft
                while vr.collidepoint(r1):
                    self.py+=1
                    self.px-=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r1=sr.topright
                while vr.collidepoint(r2):
                    self.px+=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r2=sr.midleft
                while vr.collidepoint(r3):
                    self.px-=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r3=sr.midright
                while vr.collidepoint(r4):
                    self.py-=1
                    self.px+=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r4=sr.bottomleft
                while vr.collidepoint(r5):  
                    self.py-=1
                    self.px-=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r5=sr.bottomright
                while vr.collidepoint(r6):
                    self.py+=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r6=sr.midtop
                while vr.collidepoint(r7):
                    self.py-=1
                    sr=pygame.Rect(self.px,self.py,self.tx,self.ty)
                    r7=sr.midbottom
            if self.px<0: self.px=1
            if self.px+self.tx>tex: self.px=tex-self.tx-1
            if self.py>0: self.py,self.vit=-1,0
            if self.py < -taille_circuit-2*tey : self.py , self.vit = -taille_circuit-2*tey + self.ty+1 , 0
            if self.px < 100 or self.px > 900:
                if self.vit > self.vinh: self.vit=self.vinh
                self.trace1()
    def anime(self):
        if time.time()-self.danim >= 1/self.az and  ( self.et_an<len(self.anim_f) or not self.finit ):
            self.danim=time.time()
            self.et_an+=1
            if self.et_an >= len(self.anim_f): self.et_an=0
    def ts(self):
        if time.time()-self.dts > 1/self.az:
            self.py-=self.vit/self.az
            ee=0.1
            if self.vit > self.vit_max: self.vit-=1
            if self.vit > 0:
                self.vit-=ee
            elif self.vit < 0:
                self.vit+=ee
            self.collide()
            self.anime()
            self.classement=calc_clas(self)

class Player():
    def __init__(self):
        self.nom=""
        self.age=0
        self.tchs=[]  # 0=acc 1=frein 2=tourner gauche 3=tourner droite
        self.vbcs=0
        self.camvoit=voitures[0]

def calc_clas(vt):
    clas=[]
    vvv=0
    while len(clas)<len(voitures) :
        lpp=random.choice(voitures)
        while lpp in clas: lpp=random.choice(voitures)
        for v in voitures:
            if not v in clas and v.py<=lpp.py: v=lpp
        clas.append(lpp)
    return clas.index(vt)+1

taillercy=200
taillercx=60
posrcx=tex-80
posrcy=50


def aff():
    fenetre.fill((0,0,0))
    fenetre.blit(imgmape,[0+cam[0],-taille_circuit-tex*2+cam[1]])
    fenetre.blit(pygame.transform.scale(pygame.image.load("images/ligne.png"),[tex,75]),[0+cam[0],-100+cam[1]])
    fenetre.blit(pygame.transform.scale(pygame.image.load("images/ligne.png"),[tex,75]),[0+cam[0],-taille_circuit+cam[1]])
    for t in trcvs:
        if t[2]+cam[1] > 0 and t[2]+cam[1] < tey:
            pygame.draw.rect(fenetre,t[0],(t[1]+cam[0],t[2]+cam[1],t[3],t[4]),0)
    pygame.draw.rect(fenetre,(250,250,250),(posrcx,posrcy,taillercx,taillercy),5)
    pygame.draw.rect(fenetre,(200,200,200),(posrcx+int(cam[0]/tex*taillercx),posrcy+taillercy-int(cam[1]/taille_circuit*taillercy),int(taillercx),int(tey/taille_circuit*taillercy)),2)
    for o in obtcs:
        if cam[0]+o.px < tex and cam[0]+o.px > 0 and cam[1]+o.py < tey+o.ty and cam[1]+o.py >0-o.ty :
            fenetre.blit(o.image,[o.px+cam[0],o.py+cam[1]])
    for v in voitures:
        if cam[0]+v.px < tex and cam[0]+v.px > 0 and cam[1]+v.py < tey+v.ty and cam[1]+v.py >0-v.ty :
            fenetre.blit( pygame.transform.scale(pygame.image.load("images/"+v.anim_f[v.et_an]),[v.tx,v.ty]) , [v.px+cam[0],v.py+v.ty+cam[1]])
            fenetre.blit(v.img,[v.px+cam[0],v.py+cam[1]])
            fenetre.blit( fonte.render(v.pos.nom,20,clt),[v.px+cam[0],v.py+v.ty+5+cam[1]])
            if v.finit: fenetre.blit(pygame.transform.scale(pygame.image.load("images/cp.png"),[v.tx,v.ty]),[v.px+cam[0],v.py+cam[1]])
        pygame.draw.circle(fenetre,v.pos.cl,(posrcx+int(v.px/tex*taillercx),posrcy+taillercy+int(v.py/taille_circuit*taillercy)),3)
    #stats
    fenetre.blit( font.render(str(p1.vselec.vit)[:6]+" px/s",20,clt), [20,20] )
    fenetre.blit( fonte.render(str(-p1.vselec.py)[:6]+" px parcourus",20,clt), [20,60] )
    fenetre.blit( fonte.render("classement : "+str(p1.vselec.classement)[:6]+"/"+str(len(voitures)),20,clt), [20,90] )
    if len(finits) > 0: fenetre.blit( font.render("temps restant : "+str(tprf)+" sec ",40,clt),[tex/2-50,50])
    pygame.display.update()

def bb():
    global encour,tprf,dtpr
    cond=True
    for v in voitures:
        v.ts()
        if v.py<=-taille_circuit:
            ye=False
            for ff in finits:
                if ff[1]==v: ye=True
            if not ye: finits.append([len(finits),v])
            v.finit=True
            v.freine()
        if v.vit > 0 or not v.finit: cond=False
    for o in obtcs: o.touch()
    if len(finits) > 0 and time.time()-dtpr >= 1:
        dtpr=time.time()
        tprf-=1
    if cond or tprf <= 0:
        encour=False
    
        
            

def bot():
    for b in bots:
        if random.randint(1,1) == 1 and not b.vselec.finit:
            b.vselec.accel()
            aa=random.randint(1,4)
            if aa<=2: b.vselec.tourner(1)
            elif aa<=4: b. vselec.tourner(2)
            if b.vselec.vit < 0 :
                ee=random.randint(0,10)
                if ee==1: b.vselec.freine()

def begin():
    global voitures,bots
    xx,yy=150,0
    for x in range(nbv+1): voitures.append( Voiture(xx+120*x,yy,random.choice(vcts) ) )

    player1=Player()
    player1.nom="nathan"
    player1.tchs=[K_UP,K_SPACE,K_LEFT,K_RIGHT,K_DOWN]
    player1.vselec=voitures[0]
    player1.vselec.pos=player1
    player1.cl=(0,250,0)
    
    for x in range(nbv):
        pp=Player()
        pp.nom="bot"+str(x)
        pp.vselec=voitures[x+1]
        pp.vselec.pos=pp
        pp.cl=(250,0,0)
        bots.append( pp )
    
    for x in range(nbob): obtcs.append( Obstacle(random.randint(100,900),random.randint(-taille_circuit,-300),random.randint(0,len(obs)-1)) )
    return player1

def azer():
    fenetre.fill((50,150,150))
    fenetre.blit(fonte.render("taille de circuit : "+str(taille_circuit),20,clt),[100,100])
    xx,yy=100,200
    for v in voitures:
        fenetre.blit(fonte.render(v.pos.nom,20,clt),[xx,yy])
        fenetre.blit(pygame.transform.scale(v.img,[100,100]),[xx,yy+30])
        xx+=110
    pygame.display.update()
    aa=True
    while aa:
        for event in pygame.event.get():
            if event.type==QUIT: aa=False
            elif event.type==KEYDOWN: aa=False

####

fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("TITRE")
pygame.key.set_repeat(40,30)

p1=begin()
azer()

while encour:
    tt=time.time()
    aff()
    bb()
    bot()
    for event in pygame.event.get():
        if event.type==QUIT: encour=False
        elif event.type==KEYDOWN:
            if event.key==K_q: encour=False
            if not p1.vselec.finit:
                if event.key==p1.tchs[0]   : p1.vselec.accel()
                elif event.key==p1.tchs[1] : p1.vselec.freine()
                elif event.key==p1.tchs[2] : p1.vselec.tourner(2)
                elif event.key==p1.tchs[3] : p1.vselec.tourner(1)
                elif event.key==p1.tchs[4] : p1.vselec.recul()
            if event.key==K_n:
                p1.vbcs+=1
                if p1.vbcs >= len(voitures): p1.vbcs=1
    if not p1.vselec.finit or p1.vselec.vit > 0: cam=[0,tey/2-p1.vselec.py]
    else:
        vv=voitures[p1.vbcs]
        cam=[0,tey/2-vv.py]
    if afffps:
        fps=int(1/(time.time()-tt))
        fenetre.blit(fonte.render("fps : "+str(fps),20,clt),[tex-100,10])
        pygame.display.update()

####

pygame.draw.rect(fenetre,(105,125,186),(100,100,tex-200,tey-200),0)
pygame.draw.rect(fenetre,(250,250,250),(100,100,tex-200,tey-200),5)
fenetre.blit(font.render("Résultats",40,(250,150,150)),[350,150])
xx,yy=300,300
pos=1

for v in voitures:
    if not v.finit:
        finits.append( ["non classé",v] )

for v in finits:
    fenetre.blit(fonte.render(str(v[0])+" : "+str(v[1].pos.nom),20,clt),[xx,yy])
    yy+=40
fenetre.blit(fonte.render("press any key to continue",20,clt),[tex/2,tey-50])
pygame.display.update()

encour2=True
while encour2:
    for event in pygame.event.get():
        if event.type==QUIT: encour2=False
        elif event.type==KEYDOWN:
            if event.key==K_q: encour2=False
            encour2=False
















