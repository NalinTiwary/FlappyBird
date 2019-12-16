import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

pygame.init()
pygame.font.init()

width=500
height=800
font = pygame.font.SysFont("comicsans", 50)
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy Bird")

char=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
pipe=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
bg=pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")),(width,height))
base=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

class Bird:
    anitime=5
    rvel=15
    maxr=17

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick=0
        self.vel=0
        self.height=self.y
        self.imgcount=0
        self.img=char[0]

    def jump(self):
        self.vel=-10
        self.tick=0
        self.height=self.y

    def move(self):
        self.tick+=1
        s=self.vel*self.tick+(1.5*self.tick**2)

        if s>=16:
            s=16
        elif s<0:
            s-=2

        self.y+=s

        if s<0:
            if self.tilt<self.maxr:
                self.tilt=self.maxr
        else:
            if self.tilt>-90:
                self.tilt-=self.rvel

    def draw(self,win):
        self.imgcount += 1

        if self.imgcount <= self.anitime:
            self.img = char[0]
        elif self.imgcount <= self.anitime*2:
            self.img = char[1]
        elif self.imgcount <= self.anitime*3:
            self.img = char[2]
        elif self.imgcount <= self.anitime*4:
            self.img = char[1]
        elif self.imgcount == self.anitime*4 + 1:
            self.img = char[0]
            self.imgcount = 0

        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center = (self.img).get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe():
    gap = 220
    vel = 4
    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.ptop = pygame.transform.flip(pipe, False, True)
        self.pbottom = pipe

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.ptop.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.ptop, (self.x, self.top))
        win.blit(self.pbottom, (self.x, self.bottom))

    def collision(self,bird):
        bmask = bird.mask()
        tmask = pygame.mask.from_surface(self.ptop)
        btmask = pygame.mask.from_surface(self.pbottom)
        toff = (self.x - bird.x, self.top - round(bird.y))
        boff = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bmask.overlap(btmask, boff)
        t_point = bmask.overlap(tmask,toff)

        if b_point or t_point:
            return True

        return False

class Base:
    vel=4
    width=base.get_width()

    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.width

    def move(self):
        self.x1-=self.vel
        self.x2-=self.vel

        if self.x1+self.width<0:
            self.x1=self.x2+self.width

        elif self.x2+self.width<0:
            self.x2=self.x1+self.width

    def draw(self,win):
        win.blit(base,(self.x1,self.y))
        win.blit(base,(self.x2,self.y))

def draw_win(win,bird,pipes,base,score):
    win.blit(bg,(0,0))

    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)

    score = font.render("Score: " + str(score),1,(255,255,255))
    win.blit(score, (width - score.get_width() - 15, 10))


    pygame.display.update()

def over(win,base,score):
    win.blit(bg,(0,0))
    base.draw(win)
    score = font.render("Score: " + str(score),1,(255,255,255))
    win.blit(score, (width - score.get_width() - 15, 10))
    win.blit(font.render("Game Over",3,(255,255,255)), (200,400))

    pygame.display.update()

def main():
    bird=Bird(230,250)
    pipes=[Pipe(850)]
    base=Base(730)
    clock = pygame.time.Clock()
    score=0
    flag=True

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            if pipe.x + pipe.ptop.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            pipes.append(Pipe(width))

        for r in rem:
            pipes.remove(r)

        if pipe.collision(bird):
            flag=False

        keys=pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and flag:
            bird.jump()
        bird.move()
        base.move()
        if bird.y>=700:
            run=False
        draw_win(win,bird,pipes,base,score)

    while not(run):
        over(win,base,score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

main()
