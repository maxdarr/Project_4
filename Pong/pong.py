#!/usr/bin/env python
import pygame
import random
pygame.font.init()

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=(255, 255, 255), pos_x=0, pos_y=0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
 
    def is_mouse_selection(self, posx, posy):
        #pos = pygame.mouse.get_pos()
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False
 
 
class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font=None, font_size=30,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.funcs = funcs
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item)#, '/home/nebelhom/.fonts/SHOWG.TTF')
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            mpos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(posx=mpos[0],posy=mpos[1]):
                            self.funcs[item.text]()
            # Redraw the background
            self.screen.fill(self.bg_color)
 
            for item in self.items:
                pos = pygame.mouse.get_pos()

                if item.is_mouse_selection(posx=pos[0],posy=pos[1]):
                    item.set_font_color((255, 0, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)
 
            pygame.display.flip()
 
 
if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
 
    menu_items = ('EASY', 'HARD')
    def hard():
        print("HARD")
    def easy():
        print("EASY")
    funcs = {'EASY': easy, 'HARD': hard}
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, xpos, ai=False):
        pygame.sprite.Sprite.__init__(self) #calling the base class for visible game objects
        self.xpos = xpos #sets the paddles position on the x axis
        self.ai = ai
        self.image =  pygame.Surface((10, 70)) #creates the paddle image
        self.rect = self.image.get_rect() #turns the image into a pygame rect object
        self.rect.topright = (xpos, 215)
        self.image.fill(pygame.Color("white"))

    def update(self):
        if not self.ai:
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
        global ball_speed
        self.speed = ball_speed
        self.paddles = paddles
        self.pos_d = (random.choice([-1,1]), random.choice([-1,1]))
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.image.fill(pygame.Color("white"))

    def get_new_dy(self, paddle):
        new_dy = -(paddle.rect.center[1] - ball.rect.center[1])/20.0
        return new_dy

    def update(self):
        new_dx = self.pos_d[0]
        new_dy = self.pos_d[1]
        if self.rect.topright[1] >= 480:
            new_dy = -new_dy
        elif self.rect.topright[1] <= 0:
            new_dy = -new_dy
        elif self.rect.topright[0] <= 0:
            ai_score()
            new_round()
        elif self.rect.topright[0] >= 640:
            player_score()
            new_round()
        
            
        for paddle in self.paddles:
            if self.collision(paddle.rect):
                new_dx = -new_dx
                new_dy = self.get_new_dy(paddle)
                break

        self.pos_d = (new_dx, new_dy)
        self.rect.move_ip(new_dx*self.speed, new_dy*self.speed)
        
    def collision(self, target):
        return self.rect.colliderect(target)

def update_caption():
    global player_wins, ai_wins
    pygame.display.set_caption("Pong - Player: " + str(player_wins) + "  -  Computer: " + str(ai_wins))

def check_win():
    global player_wins, ai_wins, ai_speed
    if player_wins == 5:
        pygame.display.set_caption("Player wins!")
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
    global player, computer, ball, allsprites, ai_speed
    player = Paddle(10)
    computer = Paddle(630, True)
    ball = Ball([player, computer])
    ai_speed += 0.5
    allsprites = pygame.sprite.RenderPlain((player, computer, ball))
  



pygame.init()

ball_speed = 5 #5
ai_speed = 5 #4
player = Paddle(10)
computer = Paddle(630, True)
ball = Ball([player, computer])

player_wins = 0
ai_wins = 0

allsprites = pygame.sprite.RenderPlain((player, computer, ball))

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
    clock.tick(30)
    pygame.event.pump()
    allsprites.update()
    screen.blit(background,(0,0))
    allsprites.draw(screen)
    pygame.display.flip()
