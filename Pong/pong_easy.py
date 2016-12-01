#!/usr/bin/env python
#EASY VERSION 
import pygame
import random

class Paddle(pygame.sprite.Sprite):
    def __init__(self, xpos, ai=False):
        pygame.sprite.Sprite.__init__(self) #calling the base class for visible game objects
        self.xpos = xpos #sets the paddles position on the x axis
        self.ai = ai
        self.image =  pygame.Surface((10, 70)) #creates the paddle image
        self.rect = self.image.get_rect() #turns the image into a pygame rect object
        self.rect.topright = (xpos, 215) #starting point for your paddle
        self.image.fill(pygame.Color("white")) #fill the rectangle with White

    def update(self):

        if not self.ai: #if this is your paddle
            pos = pygame.mouse.get_pos() #gets the position of your mouse
            self.rect.topright = (self.xpos, pos[1]) #makes the paddles position whatever your mouses position
            #is on the y axis, the x axis stays the same
        else: #if this is the computers paddle
            global ai_speed #calls the global variable for the ai's speed
            if self.rect.center[1]-20 < ball.rect.center[1]: #if the paddle's y coordinate minus 20 is less than
            #the the ball's y coordinate
                dy = ai_speed + random.random()*ai_speed #the paddle will move up in line with the ball
            elif self.rect.center[1]+20 > ball.rect.center[1]: #if the paddle's y coordinate plys 20 is greater
            # than the the ball's y coordinate
                dy = -1*ai_speed - random.random()*ai_speed #the paddle will move down with the ball
            else:
                dy = 0 #else its position doesn't change
            print(dy)
            self.rect.center = (self.xpos-5, self.rect.center[1]+dy) # this is the code that actually moves 
            # the paddle it makes the paddle's y coordinate move plus the new dy which was calculated above

class Ball(pygame.sprite.Sprite):
    def __init__(self, paddles):
        pygame.sprite.Sprite.__init__(self) #calling the base class for visible game objects
        global ball_speed, bounce_sound #calls the global ball_speed variable and the bounce sound
        self.speed = ball_speed
        self.paddles = paddles
        self.pos_d = (random.choice([-1,1]), random.choice([-1,1]))
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.image.fill(pygame.Color("yellow"))
        

    def get_new_dy(self, paddle):
        new_dy = -(paddle.rect.center[1] - ball.rect.center[1])/20.0 #makes dy equal to the paddles y coordinate
        # minus the balls y coordinate divided by 20
        return new_dy

    def update(self):
        new_dx = self.pos_d[0] #the new_dx is equal to 1 or -1 randomly at first and then whatever it is updated to
        new_dy = self.pos_d[1] #the new_dy is equal to 1 or -1 randomly at first and then whatever it is updated to
        if self.rect.topright[1] >= 480: #if it hits the top of the screen aim it back down,bounce noise goes
            bounce_sound.play()
            new_dy = -new_dy
        elif self.rect.topright[1] <= 0: #if it hits the bottom of the screen aim it back up,bounce noise goes
            bounce_sound.play()
            new_dy = -new_dy
        elif self.rect.topright[0] <= 0: #if it hits the left side of the of the screen then the computer's 
        #score is increased the label is updated and it is checked if they won and then a new round is started 
            ai_score()
            new_round()
        elif self.rect.topright[0] >= 640: #if it hits the right side of the of the screen then the player's 
        #score is increased the label is updated and it is checked if they won and then a new round is started 
            player_score()
            new_round()
        #if the paddle collides with the paddle then the ball is aimed back the other x direction and runs
        #get_new_dy to get the new direction in the y direction
        for paddle in self.paddles: 
            if self.collision(paddle.rect):
                bounce_sound.play() #makes the bounce noise
                new_dx = -new_dx
                new_dy = self.get_new_dy(paddle)
                break

        self.pos_d = (new_dx, new_dy) #sets pos_d to the balls new postion
        self.rect.move_ip(new_dx*self.speed, new_dy*self.speed) #this is the code that actually moves the 
        # ball to the new postions multiplied by the ball speed
        
    def collision(self, target):
        return self.rect.colliderect(target) #returns True if there is a collision for the functions above

# updates the amount of wins the player and the computer have on the caption above
def update_caption():
    global player_wins, ai_wins
    pygame.display.set_caption("Pong - Player: " + str(player_wins) + "  -  Computer: " + str(ai_wins))

#checks if either the player of the computer have 5 wins, if they do then change the caption to say
# that they won and then start the game over
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

#updates the players score then updates the caption then checks win
def player_score():
    global player_wins
    player_wins += 1
    update_caption()
    check_win()
#updates the computers score then updates the caption then checks win
def ai_score():
    global ai_wins
    ai_wins += 1
    update_caption()
    check_win()
#initiates the player's and computer's paddle stating position, the ball, increases the ai's speed
def new_round():
    global player, computer, ball, allsprites, ai_speed
    player = Paddle(10)
    computer = Paddle(630, True)
    ball = Ball([player, computer])
    #ai_speed += 0.5
    allsprites = pygame.sprite.RenderPlain((player, computer, ball))
  



pygame.init() #initialize all imported pygame modules

bounce_sound = pygame.mixer.Sound('impact.wav')

ball_speed = 5 #5
ai_speed = 2 #4
player = Paddle(10)
computer = Paddle(630, True)
ball = Ball([player, computer])

player_wins = 0
ai_wins = 0

allsprites = pygame.sprite.RenderPlain((player, computer, ball)) #creates a group of sprites to manage

screen = pygame.display.set_mode((640,480)) #creates the screen

background = pygame.Surface(screen.get_size())
background = background.convert() #converts the backgrounf into a Surface object that is best for blitting
background.fill(pygame.Color("black"))

screen.blit(background, (0,0)) #draws the image of the background onto the screen
pygame.display.flip() #Updates the full display Surface to the screen
pygame.display.set_caption("Pong - Player: 0  -  Computer: 0") #sets the initial caption
pygame.mouse.set_visible(False) #makes the mouse invisible when it is on the screen 
clock = pygame.time.Clock() #creates the clock object to help keep the time

while 1:
    clock.tick(30) #updates the clock, the frames per second
    pygame.event.pump() #internally processes pygame event handlers
    allsprites.update() #calls the update function on all the sprites in the allsprites game
    screen.blit(background,(0,0)) #redraws the background on the screen
    allsprites.draw(screen) #draws all the sprites onto the screen 
    pygame.display.flip() #updates the surface on the screen
