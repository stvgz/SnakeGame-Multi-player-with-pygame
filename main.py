import pygame,sys,random
from pygame.locals import *

pygame.init()
###
############## basic settings ############
# Size
WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
WINDOW_WIDTH_MID = WINDOWWIDTH/2
WINDOW_HEIGHT_MID = WINDOWHEIGHT/2
MIDPOSITION = (WINDOW_WIDTH_MID,WINDOW_HEIGHT_MID)
MIDPOSITION_X=MIDPOSITION[0]
MIDPOSITION_Y=MIDPOSITION[1]
HEADSIZE=20
HEADSIZE_Half=HEADSIZE/2
BODYSIZE=20
BODYSIZE_Half=BODYSIZE/2

# Direction and States
UP='UP'
DOWN='DOWN'
LEFT='LEFT'
RIGHT='RIGHT'
DIRECTIONS=[UP,DOWN,LEFT,RIGHT]

Runing='Runing'
Pause='Pause'
State=Runing

DEAD='DEAD'
LIVE='LIVE'
WAIT='WAIT'

# colors
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
LIGHTRED     = (242,   42,  7)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
LIGHTGREEN   =  (28,231,28)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (255, 255,   0)
DARKGRAY     = ( 40,  40,  40)
AQUA         = (   0, 255, 255)
PURPLE       = (128,    0, 128)
LIGHTPURPLE  = (99,11,186)

BGColor = BLACK
FoodcolorNormal=AQUA
FoodcolorSuper=YELLOW
FoodcolorPoision=LIGHTRED
FoodcolorFast=LIGHTGREEN
FoodcolorSlow=LIGHTPURPLE

ScoreFont=pygame.font.SysFont('arial',50)
DeadFont=pygame.font.SysFont('comic sans MS',25)

# Icons
ICON_P1_Head = pygame.image.load('images\\ICON_P1_Head.jpg')
ICON_P1_Body = pygame.image.load('images\\Blue_20x20.bmp')
ICON_P2_Head = pygame.image.load('images\\ICON_P2_Head.png')
ICON_P2_Body = pygame.image.load('images\\Red_20x20.bmp')
ICON_P3_Head = pygame.image.load('images\\ICON_P3_Head.png')
ICON_P3_Body = pygame.image.load('images\\Green_20x20.bmp')
HELP = pygame.image.load('images\\Help.bmp')

############## basic game settings ############3
Playerlist=[]
STARTSPEED =1
Foodlist=[]
Normal='Normal'
Super='Super'
Poision='Poision'
Fast='Fast'
Slow='Slow'
Typelistfood=[Normal,Super,Poision,Fast,Slow]
TimeToAddFood=0
TypePossibility=[60,10,10,10,10]
TypeDict=dict(zip(Typelistfood,TypePossibility))


############ game settings ########3

SELFCRUSH=True
FIGHTMODE=True
WeightToSpeedDelay=2

# Foodlist: 0 Type 1 postionx, 2 Y, 3, drawsize,4,weight, 5 lifetime,5,6,7,8,9 placeholder

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def terminate():
    pygame.quit()
    sys.exit()

def directiontoxy(direction):
    if direction ==UP:
        return 0,-1
    if direction == DOWN:
        return 0,1
    if direction ==LEFT:
        return -1,0
    if direction == RIGHT:
        return 1,0

def Startgame(Player=1,Food=10):
    for i in range(Food):
        food_more(1)

########### functions about food ##############3
def foodrefuel(Qty=1):
    for i in range(Qty):
        Foodlist.append(getrandomfood())

def getrandomfood():
    foodtype = getrandomfoodtype()
    x=random.randint(0,WINDOWWIDTH-BODYSIZE)
    y=random.randint(0,WINDOWHEIGHT-BODYSIZE)
    weight=1

    drawsize = BODYSIZE + (weight - 1) * 0.3
    lifetime=1000
    if foodtype==Super:
        weight=5
        drawsize=drawsize*2
        lifetime=5
    if foodtype==Normal:
        weight=random.randint(1, 2)

    food=[foodtype,x,y,drawsize,weight,lifetime,0,0,0,0,0,0]
    return food

def getrandomfoodtype():
    newlist=[]
    for type in TypeDict:
        for index in range(TypeDict[type]):
            newlist.append(type)
    return random.choice(newlist)

def drawfood(foodlist):
    for food in foodlist:
        type=food[0]
        x=food[1]
        y=food[2]
        weight=food[4]
        drawsize=food[3]
        if type==Normal:
            foodrect=pygame.Rect(x,y,drawsize,drawsize)
            pygame.draw.rect(DISPLAYSURF,FoodcolorNormal,foodrect)
        if type==Super:
            foodrect=pygame.Rect(x,y,drawsize,drawsize)
            pygame.draw.rect(DISPLAYSURF, FoodcolorSuper, foodrect)
        if type==Fast:
            foodrect=pygame.Rect(x,y,drawsize,drawsize)
            pygame.draw.rect(DISPLAYSURF, FoodcolorFast, foodrect)
        if type==Slow:
            foodrect=pygame.Rect(x,y,drawsize,drawsize)
            pygame.draw.rect(DISPLAYSURF, FoodcolorSlow, foodrect)
        if type==Poision:
            foodrect=pygame.Rect(x,y,drawsize,drawsize)
            pygame.draw.rect(DISPLAYSURF, FoodcolorPoision, foodrect)

def foodcollision(foodlist,player):
    foodlistcopy=foodlist.copy()
    index=0
    for food in foodlistcopy:
        type=food[0]
        foodx,foody,size,weight=food[1],food[2],food[3],food[4]
        foodrect=pygame.Rect(foodx,foody,size,size)

        headrect=player.headrect

        IsCollision=pygame.Rect.colliderect(foodrect,headrect)  # if collision

        if IsCollision==True:
            foodlist.pop(index)  # delete crushed
            player.changelenth(weight)  # change lenth
            foodrefuel(1)

            index -= 1

            ## other affect ###
            if type==Normal or type==Super:
                player.score =player.score+ weight  # add score

                player.speedupcount+=weight
                if player.speedupcount>=player.counttoupspeed:
                    player.counttoupspeed+=WeightToSpeedDelay
                    player.Speedup()
                    player.speedupcount=0

            if type==Poision:
                player.score=player.score-5
                player.changelenth(-5)

            if type==Slow:
                player.speed-=0.5

            if type==Fast:
                player.speed+=0.5
                player.score+=2
        index+=1

def food_more(Qty=3):
    for i in range(Qty):
        Foodlist.append(getrandomfood())

def food_less(Qty=3):
    for i in range(Qty):
        if len(Foodlist)>=1:
            Foodlist.pop()

def timeaddfood():
    global TimeToAddFood
    TimeToAddFood+=1
    min=1
    if TimeToAddFood>=FPS*60*min:
        food_more()
        TimeToAddFood=0

def deadanimation(player):
    x=player.headrect.left
    y=player.headrect.top
    deadrender=DeadFont.render('So sad to lose you.:D',True,WHITE)
    DISPLAYSURF.blit(deadrender,(x,y))

def showhelp():
    global State
    State=Pause
    DISPLAYSURF.blit(HELP,(300,100))

def playercrush():
    for p1 in Playerlist:
        p1head=p1.headrect
        for p2 in Playerlist:
            if p1!=p2:
                for body in p2.bodylist:
                    x=body[0]
                    y=body[1]
                    bodyrect=pygame.Rect((x,y),(BODYSIZE,BODYSIZE))
                    if pygame.Rect.colliderect(p1head,bodyrect) and p2.status!=DEAD and p1.status!=DEAD:
                        p1.status=DEAD
                        p2.score+=10


def debuginfo(location=None):
    index=1
    for player in Playerlist:
        print('---------------debug information----------------------------')
        if location!=None:
            print('@ %s'%location)
        print('P%s'%index)
        print('Head:%s '%player.headposition)
        print('Speed %s' %player.speed)
        print('Lenth %s' %player.lenth)
        print('Bodylist: %s '%player.bodylist)
        index+=1

class Snake():
    ######### start status  ############
    def __init__(self,iconhead=ICON_P1_Head,iconbody=ICON_P1_Body):
        self.status=LIVE
        self.HEADICON=iconhead
        self.BODYICON=iconbody
        self.score=0
        self.headposition = MIDPOSITION

        self.headrect=pygame.Rect(self.headposition,(HEADSIZE,HEADSIZE))
        self.lenth=5
        self.speed = STARTSPEED
        self.speedupcount=0
        self.counttoupspeed=1
        self.moveinterval=20  # move every 20 frame, change to change speed
        self.counttomove=0
        # self.bodyrectlist=[]
        self.bodylist=[]
        self.direction = random.choice(DIRECTIONS)
        self.Moveevent = pygame.time.set_timer(USEREVENT, 200//self.speed)

        for i in range(1,self.lenth+1):
            x,y=directiontoxy(self.direction)
            headcenter=self.headrect.center
            centerdistancex=x*(BODYSIZE)*i*-1
            centerdistancey=y*(BODYSIZE)*i*-1
            bodycenter=(headcenter[0]+centerdistancex,headcenter[1]+centerdistancey)
            bodyleft=bodycenter[0]-BODYSIZE_Half
            bodytop=bodycenter[1]-BODYSIZE_Half
            bodysegment=[bodyleft,bodytop]
            self.bodylist.append(bodysegment)

    def reset(self):  # the same as init, but without icon change
        self.status = LIVE
        self.score = 0
        self.headposition = MIDPOSITION

        self.headrect = pygame.Rect(self.headposition, (HEADSIZE, HEADSIZE))
        self.lenth = 5
        self.speed = STARTSPEED
        self.speedupcount = 0
        self.counttoupspeed = 1
        self.moveinterval = 20
        self.counttomove = 0
        # self.bodyrectlist=[]
        self.bodylist = []
        self.direction = random.choice(DIRECTIONS)
        self.Moveevent = pygame.time.set_timer(USEREVENT, 200 // self.speed)

        for i in range(1, self.lenth + 1):
            x, y = directiontoxy(self.direction)
            headcenter = self.headrect.center
            centerdistancex = x * (BODYSIZE) * i * -1
            centerdistancey = y * (BODYSIZE) * i * -1
            bodycenter = (headcenter[0] + centerdistancex, headcenter[1] + centerdistancey)
            bodyleft = bodycenter[0] - BODYSIZE_Half
            bodytop = bodycenter[1] - BODYSIZE_Half
            bodysegment = [bodyleft, bodytop]
            self.bodylist.append(bodysegment)

    def movehead(self):
        if self.status==LIVE:
            self.counttomove+= self.speed
            if self.counttomove>=self.moveinterval:
                self.counttomove=0

            ########## move head #############
                top= self.headrect.top
                left=self.headrect.left

                self.bodylist[0] = [left, top]
                x, y = directiontoxy(self.direction)
                top = top + y *BODYSIZE
                left = left+ x *BODYSIZE
                self.headposition = [left, top]
                self.headrect = pygame.Rect((left, top), (HEADSIZE, HEADSIZE))

                ################# move other segment ###### replace 2nd segment with 1st segment

                lastsegment=self.lenth-1
                while lastsegment!=0:
                    self.bodylist[lastsegment]=self.bodylist[lastsegment-1]
                    lastsegment-=1

    def changedirection(self,movedirection):
        self.direction=movedirection

    def draw(self,surface):

        for index in range(self.lenth):
            positionx=self.bodylist[index][0]
            positiony=self.bodylist[index][1]
            rect=pygame.Rect(positionx,positiony,BODYSIZE,BODYSIZE)
            surface.blit(self.BODYICON,rect)
        surface.blit(self.HEADICON, self.headrect)

    def drawscore(self,surface,position):
        self.scoreboardrender = ScoreFont.render('Score: ' + str(self.score), True, WHITE)
        surface.blit(self.scoreboardrender,position)

    def Speedup(self,factor=0.1):
        self.speed=self.speed+factor

    def changelenth(self,changeqty):
        assert type(changeqty)==int
        if changeqty>=1:
            self.lenth+=changeqty
            for i in range(changeqty):
                self.bodylist.append(self.bodylist[-1])

        if changeqty<=-1:
            self.lenth+=changeqty
            for i in range(abs(changeqty)):
                self.bodylist.pop()




    def hitwall(self):

        x = self.headrect.left
        y = self.headrect.top
        if x < 0 or x > WINDOWWIDTH or y < 0 or y > WINDOWHEIGHT - HEADSIZE:
            self.status=DEAD

    def selfcrush(self):
        for body in self.bodylist:
            bodyposition=(body[0],body[1])
            bodyrect=pygame.Rect(bodyposition,(BODYSIZE,BODYSIZE))
            if pygame.Rect.colliderect(self.headrect,bodyrect)==True:
                self.status=DEAD

def main():

    global FPS,FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT,State
    ######### system settings
    FPS=60
    FPSCLOCK = pygame.time.Clock()

    ###### Game settings ###########
    StartFOOD=15

    ##### display ######
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('---snake--- Press SPACE to get HELP ')
    BASICFONTSIZE = 100
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    DISPLAYSURF.fill(BGColor)



    ############################### Game start  #######################

    P1=Snake(ICON_P1_Head,ICON_P1_Body)
    Playerlist.append(P1)
    Startgame(StartFOOD)

    while True:
        while State==Pause:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_p or event.key==K_SPACE:
                        State=Runing
            checkForQuit()

        while State==Runing:

            checkForQuit()
            DISPLAYSURF.fill(BGColor)

            drawfood(Foodlist)
            timeaddfood()
            playerscoreindex=0

            for player in Playerlist:
                player.draw(DISPLAYSURF)
                scoreboardposition=(0,playerscoreindex*60)
                player.drawscore(DISPLAYSURF,scoreboardposition)
                foodcollision(Foodlist,player)
                player.movehead()
                player.hitwall()
                player.selfcrush()
    
                if player.status==DEAD:
                    deadanimation(player)
                playerscoreindex+=1

            playercrush()

            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_SPACE:
                        showhelp()
                    if event.key==K_0:
                        food_more()
                    if event.key==K_9:
                        food_less()

                    if event.key==K_UP and P1.direction!=DOWN:
                        P1.direction= UP
                    if event.key==K_DOWN and P1.direction!=UP:
                        P1.direction=DOWN
                    if event.key==K_LEFT and P1.direction!=RIGHT:
                        P1.direction=LEFT
                    if event.key==K_RIGHT and P1.direction!=LEFT:
                        P1.direction=RIGHT
                    if event.key==K_F1:
                        P1.reset()
                    if event.key==K_p:
                        State=Pause

                    if event.key==K_2 and len(Playerlist)<2:
                        P2=Snake(ICON_P2_Head,ICON_P2_Body)
                        food_more(5)
                        Playerlist.append(P2)

                    if len(Playerlist)>=2:
                        if event.key == K_w and P2.direction != DOWN:
                            P2.direction = UP
                        if event.key == K_s and P2.direction != UP:
                            P2.direction = DOWN
                        if event.key == K_a and P2.direction != RIGHT:
                            P2.direction = LEFT
                        if event.key == K_d and P2.direction != LEFT:
                            P2.direction = RIGHT
                        if event.key == K_F2:
                            P2.reset()
                            
                    if event.key == K_3 and len(Playerlist)<3:
                        P3 = Snake(ICON_P3_Head, ICON_P3_Body)
                        Playerlist.append(P3)
                    if len(Playerlist) >= 3:
                        if event.key == K_u and P3.direction != DOWN:
                            P3.direction = UP
                        if event.key == K_j and P3.direction != UP:
                            P3.direction = DOWN
                        if event.key == K_h and P3.direction != RIGHT:
                            P3.direction = LEFT
                        if event.key == K_k and P3.direction != LEFT:
                            P3.direction = RIGHT
                        if event.key == K_F3:
                            P3.reset()

            ######### at the end of while True loop, update the screen and FPS
            pygame.display.update()
            FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()