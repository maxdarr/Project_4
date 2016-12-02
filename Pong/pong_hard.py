#!/usr/bin/env python
#HARD VERSION - ONLY COMMENTED WHAT IS DIFFERENT FROM THE EASY VERSION
import pygame
import random
import sys
pygame.font.init()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, xpos, ai=False):
        pygame.sprite.Sprite.__init__(self) 
        self.xpos = xpos 
        self.ai = ai
        self.image =  pygame.Surface((10, 70)) 
        self.rect = self.image.get_rect() 
        self.rect.topright = (xpos, 215) 
        self.image.fill(pygame.Color("white")) 

    def update(self):

        if not self.ai: 
            self.image = pygame.Surface((10,45))
            self.rect = self.image.get_rect()
            self.image.fill(pygame.Color("white"))
            pos = pygame.mouse.get_pos() 
            self.rect.topright = (self.xpos, pos[1]) 
        else: 
            global ai_speed 
            if self.rect.center[1]-20 < ball.rect.center[1]: 
                dy = ai_speed + random.random()*ai_speed 
            elif self.rect.center[1]+20 > ball.rect.center[1]: 
                dy = -1*ai_speed - random.random()*ai_speed 
            else:
                dy = 0 
            print(dy)
            self.rect.center = (self.xpos-5, self.rect.center[1]+dy)

class Ball(pygame.sprite.Sprite):
    def __init__(self, paddles):
        pygame.sprite.Sprite.__init__(self) 
        global ball_speed, bounce_sound
        self.speed = ball_speed
        self.paddles = paddles
        self.pos_d = (random.choice([-1,1]), random.choice([-1,1]))
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.image.fill(pygame.Color("yellow"))
        self.coll_counter = 0
        

    def get_new_dy(self, paddle):
        new_dy = -(paddle.rect.center[1] - ball.rect.center[1])/20.0 
        return new_dy

    def update(self):
        new_dx = self.pos_d[0] 
        new_dy = self.pos_d[1] 
        if self.rect.topright[1] >= 480:
            bounce_sound.play() 
            new_dy = -new_dy
        elif self.rect.topright[1] <= 0: 
            bounce_sound.play()
            new_dy = -new_dy
        elif self.rect.topright[0] <= 0: 
            edge_hit.play()
            ai_score()
            new_round()
        elif self.rect.topright[0] >= 640: 
            edge_hit.play()
            player_score()
            new_round()
        
        for paddle in self.paddles: 
            if self.collision(paddle.rect):
                bounce_sound.play()
                new_dx = -new_dx
                new_dy = self.get_new_dy(paddle)
                self.speed += 1
                #speed_block.create_block()
                break

        self.pos_d = (new_dx, new_dy) 
        self.rect.move_ip(new_dx*self.speed, new_dy*self.speed)
        
    def collision(self, target):
        return self.rect.colliderect(target) 

class speed_block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global ball_speed
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect()
        self.xpos = 320
        self.ypos = random.randint(120,220)
        self.rect.center = (self.xpos, self.ypos)
        self.image.fill(pygame.Color("red"))


    def update(self):
        global ball_speed
        if self.collision(ball.rect):
            speed_sound.play()
            ball.speed += 15
            

    def collision(self, target):
        return self.rect.colliderect(target)


class speed_block2(speed_block):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global ball_speed
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect()
        self.xpos = 320
        self.ypos = random.randint(260,360)
        self.rect.center = (self.xpos, self.ypos)
        self.image.fill(pygame.Color("red"))





def update_caption():
    global player_wins, ai_wins
    pygame.display.set_caption("Pong - Player: " + str(player_wins) + "  -  Computer: " + str(ai_wins))


def check_win():
    global player_wins, ai_wins, ai_speed
    if player_wins == 5:
        pygame.display.set_caption("You win!")
        player_wins = 0
        ai_wins = 0
        ai_speed = 3
        new_round()
    elif ai_wins == 5:
        pygame.display.set_caption("Computer wins!")
        player_wins = 0
        ai_wins = 0
        ai_speed = 3
        new_round()

def player_score():
    global player_wins
    player_wins += 1
    update_caption()
    check_win()

def ai_score():
    global ai_wins
    ai_wins += 1
    update_caption()
    check_win()

def new_round():
    global player, computer, ball, allsprites, ai_speed, speed_block1, speed_block_2, ball_speed
    player = Paddle(10)
    computer = Paddle(630, True)
    ball = Ball([player, computer])
    ai_speed += 0.5
    speed_block1 = speed_block()
    speed_block_2 = speed_block2()
    ball_speed = 5
    allsprites = pygame.sprite.RenderPlain((player, computer, ball, speed_block1, speed_block_2))
  


pygame.init() 

bounce_sound = pygame.mixer.Sound('impact.wav')
edge_hit = pygame.mixer.Sound('edge_hit.wav')
speed_sound = pygame.mixer.Sound('Speed.wav')

ball_speed = 5 
ai_speed = 6 #moved up from 2
player = Paddle(10)
computer = Paddle(630, True)
ball = Ball([player, computer])
speed_block1 = speed_block()
speed_block_2 = speed_block2()

player_wins = 0
ai_wins = 0

allsprites = pygame.sprite.RenderPlain((player, computer, ball, speed_block1, speed_block_2)) 
screen = pygame.display.set_mode((640,480)) 

background = pygame.Surface(screen.get_size())
background = background.convert() 
background.fill(pygame.Color("black"))

screen.blit(background, (0,0)) 
pygame.display.flip() 
pygame.display.set_caption("Pong - Player: 0  -  Computer: 0") 
pygame.mouse.set_visible(False) 
clock = pygame.time.Clock() 

while 1:
    clock.tick(50) 
    pygame.event.pump() 
    allsprites.update()
    #speed_block.update() 
    screen.blit(background,(0,0)) 
    allsprites.draw(screen) 
    pygame.display.flip() 
