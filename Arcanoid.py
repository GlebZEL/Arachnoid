import pygame
import sys
from random import randint
from time import sleep
pygame.init()
clock = pygame.time.Clock()  # создаем игровой таймер
FPS = 40
window = pygame.display.set_mode((950, 950))
wf=(4,150,93)
window.fill(wf)  # заливка цвета фона

monsters=[]
n=9
game_play=True


class Area():
    def __init__(self,x,y,width,height,color=None):
        self.rect=pygame.Rect( x,y,width,height)
        self.fill_color=wf
        if color:
            self.fill_color=color

    def n_color(self,newcolor):
        self.fill_color=newcolor
    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)
    def outline(self, frame_color, thickness):
        pygame.draw.rect(window, frame_color, self.rect, thickness)
    
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
    
    def colliderect(self,rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__ (self, filename, x=0, y=0,width=10,height=10):
        super().__init__(x=x,y=y,width=width,height=height,color=None)
        self.image=pygame.transform.scale(pygame.image.load(filename),(width,height))

    def paint(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

    #def hit(self,width,height):
    #    self.image = pygame.transform.scale(pygame.image.load("bum.png"),(10,10))

class Label(Area):
    def set_text(self, text, fsize=12, text_color=(255,255,255)) :
        self.text=pygame.font.SysFont('segoeprint', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))

ball=Picture('ball.png',370,400,50,50)
platform=Picture('platform.png',340,500,200,75)

step_x=2
step_y=2

monsters=[]
n=11

for i in range(4):
    start_xray=80+(35*i)
    start_yray=80+(70*i)
    for z in range(n):
        monster=Picture('monster.png',start_xray,start_yray,50,50)
        monsters.append(monster)
        start_xray+=70
    n-=1

move_right=False
move_left=False

while True:
    if game_play:
        platform.fill()
        ball.fill()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                    move_right=True
                elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
                    move_left=True
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                    move_right=False
                elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
                    move_left=False
            elif event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        ball.rect.x-=step_x
        ball.rect.y+=step_y
            
        if move_right:
            platform.rect.x+=3
        if move_left:
            platform.rect.x-=3
        ball.paint()
        platform.paint()
        for g in monsters:
            g.paint()
            if g.rect.colliderect(ball.rect):
                #bum=pygame.image.load("bum.png")
                #g.image=bum
                #g.hit()
                monsters.remove(g)
                g.fill()
                step_y*=-1
        
        if ball.colliderect(platform):
            step_x=step_x*1
            step_y=step_y*(-1)
        
        if ball.rect.x==950 or ball.rect.x==0:
            step_x=step_x*-1
            step_y=step_y*1
        
        if ball.rect.y<=0:
            step_x=step_x*1
            step_y=step_y*(-1)

        if ball.rect.y>550:
            time_text=Label(250,150,50,50,wf)
            time_text.set_text("YOU ARE LOSER",120,(166,0,0))
            time_text.draw(20,20)
            game_play=False

        if len(monsters)==0:
            time_text=Label(150,150,50,50,wf)
            time_text.set_text("YOU WIN",120,(166,0,0))
            time_text.draw(20,20)
            game_play=False
    else:
        game_play=False

    pygame.display.update()

    clock.tick(FPS)