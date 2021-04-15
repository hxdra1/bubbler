import pygame
from pygame.constants import (
    QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN)
import os
from random import randint
import sys
import time


class Settings:
    w_width = 1000
    w_height = 800
    w_border = 50
    pygame.display.set_caption("bubbler")
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    sound_path = os.path.join(file_path, "Sound" )

class Background(object):
    def __init__(self, filename):
        self.imageo = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(self.imageo, (Settings.w_width, Settings.w_height)).convert()
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.durchmesser = 40
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path,"blue2.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (self.durchmesser, self.durchmesser))
        self.rect = self.image.get_rect()
        self.rect.left = randint(Settings.w_border, Settings.w_width - Settings.w_border)
        self.rect.top = randint(Settings.w_border, Settings.w_height - (Settings.w_border * 2))
        self.cd = pygame.time.get_ticks()
        self.cds = 1400
        self.ran = pygame.time.get_ticks()
        self.o = 0 

    def update(self):
        self.scale()

    def cooldown_scale(self):
        if self.o < 500:
            self.o += 2
        if self.o >= 500:
            self.o += 0.2        
        return pygame.time.get_ticks() >= self.cd - self.o

    def scale(self):
        if self.cooldown_scale():
            self.durchmesser += randint(1, 4)
            c = self.rect.center
            self.image = pygame.transform.scale(self.image_orig, (self.durchmesser, self.durchmesser))
            self.rect = self.image.get_rect()
            self.rect.center = c
            self.cd = pygame.time.get_ticks() + self.cds
            if self.durchmesser > 70:    
                pygame.quit()
            if self.ran > 1000:
                self.cds -= 100


    def game_over(self, screen):
        if self.durchmesser > 75:
            self.font1 = pygame.font.SysFont("comicsans",20, True , True)
            self.text1 = self.font1.render(("GAME OVER"),1,(255, 255, 255))
            screen.blit(self.text1,(400, 400))

    def events(self):
        pass
 
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

class Score(object):
    def __init__(self):
        self.count = 0
        self.font = pygame.font.SysFont("comicsans",20, True , True)
        self.text = self.font.render("Score : "+str(self.count),1,(255, 255, 255))

    def show_score(self, screen):
        screen.blit(self.text,(10 ,10))

    def score_up(self):
        self.count += 3
        self.text = self.font.render("Score : "+str(self.count),1,(0,0,0))

class Cursor(object):
    def __init__(self):
        self.cursorx = pygame.image.load(os.path.join(Settings.image_path, "cursor.png")).convert_alpha()
        self.cursor  = pygame.transform.scale(self.cursorx, (50, 50))
        self.rect = self.cursor.get_rect()

    def drawmouse(self, screen):
        pygame.mouse.set_visible(False)
        screen.blit(self.cursor,(pygame.mouse.get_pos()))

class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.w_width, Settings.w_height))
        self.clock = pygame.time.Clock()
        self.runn = False
        self.score = Score()
        self.background = Background("background5.jpg")
        self.all_balls=pygame.sprite.Group()
        self.sound1 = pygame.mixer.Sound(os.path.join(Settings.sound_path, "click.wav"))
        self.sound2 = pygame.mixer.Sound(os.path.join(Settings.sound_path, "pop.wav"))
        self.music = pygame.mixer.music.load(os.path.join(Settings.sound_path, "musik.mp3"))
        self.ball_cd = pygame.time.get_ticks()
        self.ball_cds = 1000
        self.cursor = Cursor()
        self.k = 1
        self.ram = pygame.time.get_ticks()
        self.i = 0


    def run(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.runn = True
        self.pause = False
        

        while self.runn:
            self.clock.tick(60)
            self.watch_for_events()
                

            if not self.pause:
                self.draw()
                self.events()            
                self.all_balls.update()
                pygame.mixer.music.unpause()
                pygame.mouse.set_visible(False)

            if self.pause:
                pygame.mixer.music.pause()
                pygame.mouse.set_visible(False)


    def ball_cooldown(self):
        if self.i < 500:
            self.i += 1
        if self.i >= 500:
            self.i += 0.2

        return pygame.time.get_ticks() >= self.ball_cd - self.i
    
    def events(self):
        for i in range(1):
            if self.ball_cooldown():
                if len(self.all_balls)< self.k:
                    self.all_balls.add(Ball())
                    self.ball_cd = pygame.time.get_ticks() + self.ball_cds
                    self.k += 1
          

    def draw(self):
        self.background.draw(self.screen)
        self.all_balls.draw(self.screen)
        self.score.show_score(self.screen)
        self.cursor.drawmouse(self.screen)
        

        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.runn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause
            if not self.pause and event.type == MOUSEBUTTONDOWN:          
                for ball in self.all_balls: 
                    if ball.rect.collidepoint(event.pos):                   
                        self.sound2.play()
                        ball.kill()  
                        self.score.score_up()
                    


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOWS_POS'] = "50, 1100"
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    