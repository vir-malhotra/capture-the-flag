import time
import random
import os
add_library('minim')

#defining global variables
RES_X = 800
RES_Y = 400
PLAYER_X = RES_X/40
PLAYER_Y = PLAYER_X
SCORE_LIMIT = 3
path = os.getcwd()

#game class
class Game:
    def __init__(self):
        self.capt = False
        self.p1_score = 0
        self.p2_score = 0
        self.winner = None
        self.p1_imt = 1
        self.p2_imt = 1
        
        self.map = random.randint(1,2)
        self.obstacles = []
        if self.map == 1:
            for i in map1:
                obstacle = Obstacles(i[0], i[1], i[2], i[3])
                self.obstacles.append(obstacle)
        elif self.map == 2:
            for i in map2:
                obstacle = Obstacles(i[0], i[1], i[2], i[3])
                self.obstacles.append(obstacle)
                
    def game_over(self):
        if self.p1_score == SCORE_LIMIT or self.p2_score == SCORE_LIMIT:
            game_over.rewind()
            game_over.play()
            background(0,0,0)
            textSize(45)
            textAlign(CENTER, CENTER)
            if self.p1_score == SCORE_LIMIT:
                self.winner = 'Red'
                fill(255,0,0)
            elif self.p2_score == SCORE_LIMIT:
                self.winner = 'Blue'
                fill(0,0,255)
            text('The winner is ' + self.winner, RES_X/2, RES_Y/2)
            textSize(15)
            text('click mouse to restart', RES_X/2, RES_Y/2+40)
            
            
            
        
    def score(self):
        fill(0,0,0)
        textSize(15)
        textAlign(CENTER, BOTTOM)
        text(str(self.p1_score), 50,30)
        text(str(self.p2_score), RES_X-50,30)

    #defining a scoring function to activate the power up every alternate round
    def scored(self):
        global flag_1, flag_2, player_1, player_2, power
        points.rewind()
        points.play()
        player_2 = Player('blue')
        player_1 = Player('red')
        flag_1 = Flag('red')
        flag_2 = Flag('blue')
        if (self.p1_score + self.p2_score) % 2 == 0:
            power = PowerUp()
        
        
    def display(self):
        if self.capt == True:
            self.scored()
            self.capt = False
        self.score()
        flag_1.display()
        flag_2.display()
        if player_1.ghost == False:
            player_1.death(player_2)
        if player_2.ghost == False:
            player_2.death(player_1)
        player_2.display()
        player_1.display()
        if self.winner == None:
            for obstacle in self.obstacles:
                obstacle.display()
        power.display()
        self.game_over()

#class for both power ups    
class PowerUp:
    def __init__(self):
        #initializing the class with coordinates of four points at which the power ups randomly appear
        self.p1x = RES_X/2 - 125
        self.p2x = RES_X/2 + 125
        self.p1y = RES_Y/2 - 150
        self.p2y = RES_Y/2 + 150
        self.points = [self.p1x, self.p2x, self.p1y, self.p2y]
        self.randx = random.randint(0,1)
        self.randy = random.randint(2,3)
        self.speed = loadImage(path + "/images/" + "flash.png")
        power_up = None
    
    #setting up an immunity power up that can be activated once throughout the game    
    def ghost(self):
        if key == 'q' and player_1.ghost == False and game.p1_imt !=0:
            power_up.rewind()
            power_up.play()
            game.p1_imt -= 1
            player_1.ghost = True

        
        if key == 'p' and player_2.ghost == False and game.p2_imt !=0:
            power_up.rewind()
            power_up.play()
            game.p2_imt -= 1
            player_2.ghost = True
    
    #defining a flash power up that appears every alternate round and slows down the opponent
    def speed_up(self):
        if player_1.x >= self.points[self.randx] and player_1.x <= self.points[self.randx] + PLAYER_X*1.5 and player_1.y >= self.points[self.randy] and player_1.y <= self.points[self.randy] + PLAYER_Y*1.5:
            player_2.speed = 0.32
            power_up.rewind()
            power_up.play()
        
        if player_2.x >= self.points[self.randx] and player_2.x <= self.points[self.randx] + PLAYER_X*1.5 and player_2.y >= self.points[self.randy] and player_2.y <= self.points[self.randy] + PLAYER_Y*1.5:
            player_1.speed = 0.32
            power_up.rewind()
            power_up.play()
    
    def graphic(self, player):
        pass
    
    def display(self):
        self.ghost()
        if player_1.speed != 0.32 and player_2.speed != 0.32:
            if (game.p1_score + game.p2_score) % 2 == 1:
                self.speed_up()
                image(self.speed, self.points[self.randx], self.points[self.randy], PLAYER_X*2, PLAYER_Y*2)
    
        
class Player:
    def __init__(self, colour):
        self.c = colour
        self.ghost = False
        self.speed = 0.6
        
        if self.c == 'red':
            self.x = PLAYER_X*3
        elif self.c == 'blue':
            self.x = RES_X - PLAYER_X*4
        self.y = RES_Y/2 - PLAYER_Y/2
        
        self.dir = {'Left' : False, 'Right' : False, 'Up' : False, 'Down' : False}
        self.vx = 0
        self.vy = 0
        
        
        
    def keycontrol(self, keytype, criteria, a, b, c, d):
        #if timer is active then lock key presses for 0.3 seconds
        if keytype == a:
            self.dir['Left'] = criteria
        elif keytype == b:
            self.dir['Right'] = criteria
        elif keytype == c:
            self.dir['Up'] = criteria
        elif keytype == d:
            self.dir['Down'] = criteria  
            

        
    def velocity(self):
        if self.dir['Right'] == True:
            self.vx = self.speed
        elif self.dir['Left'] == True:
            self.vx = -self.speed
        else:
            self.vx *= 0.995
            
        if self.dir['Up'] == True:
            self.vy = -self.speed
        elif self.dir['Down'] == True:
            self.vy = self.speed
        else:
            self.vy *= 0.995
            
        
        if self.y <= 1 or self.y >= RES_Y - PLAYER_Y:
            self.vy = self.vy * -1
            bump.rewind()
            bump.play()
            #start timer
                
        if self.x <= 1 or self.x >= RES_X - PLAYER_X:
            self.vx = self.vx * -1
            bump.rewind()
            bump.play()
            #start timer

        #setting up the bumping mechanics by reversing the y velocity for the top and bottom, and reversing the x velocity for the sides,
        #leaving a 1 pixel gap on the edges of each where the sprite can get stuck to make player movement more challenging
        for obstacle in game.obstacles:
            if self.x >= obstacle.x - 20 and self.x <= obstacle.x + obstacle.w and self.y >= obstacle.y - 20 and self.y <= obstacle.y + obstacle.h and self.y + 4 > obstacle.y + obstacle.h:
                self.vy = self.vy * -1
                bump.rewind()
                bump.play()
                #if timer is active then lock key presses for 0.3 seconds
                
            if self.x >= obstacle.x - 20 and self.x <= obstacle.x + obstacle.w and self.y >= obstacle.y - 20 and self.y <= obstacle.y + obstacle.h and self.y + 16 < obstacle.y:
                self.vy = self.vy * -1
                bump.rewind()
                bump.play()
                #if timer is active then lock key presses for 0.3 seconds
    
            if self.x >= obstacle.x - 20 and self.x <= obstacle.x + obstacle.w and self.y >= obstacle.y - 20 and self.y <= obstacle.y + obstacle.h and self.x + 4 > obstacle.x + obstacle.w:
                self.vx = self.vx * -1
                bump.rewind()
                bump.play()
                #if timer is active then lock key presses for 0.3 seconds
                
            if self.x >= obstacle.x - 20 and self.x <= obstacle.x + obstacle.w and self.y >= obstacle.y - 20 and self.y <= obstacle.y + obstacle.h and self.x + 16 < obstacle.x:
                self.vx = self.vx * -1
                bump.rewind()
                bump.play()
                #if timer is active then lock key presses for 0.3 seconds
                
        self.x += self.vx
        self.y += self.vy
        
        
            
        
            
    def death(self, other):
        if other.x <= (self.x + PLAYER_X) and (other.x + PLAYER_X) >= self.x and other.y <= (self.y + PLAYER_Y*1.5) and (other.y + PLAYER_Y*1.5) >= self.y:
            if self.c == 'red' and self.x > RES_X/2:
                self.x = PLAYER_X*3
                self.y = RES_Y/2 - PLAYER_Y/2
            if self.c == 'blue' and self.x < RES_X/2:
                self.x = RES_X - PLAYER_X*4
                self.y = RES_Y/2 - PLAYER_Y/2 
            death.rewind()
            death.play()

        
        
        
    def display(self):
        self.velocity()
        strokeWeight(3)
        if self.c == 'red':
            fill(255,0,0)
        if self.c == 'blue':
            fill(0,0,255)
        if self.ghost == False:
            rect(self.x, self.y, PLAYER_X, PLAYER_Y)
        elif self.ghost == True:
            ellipse(self.x + PLAYER_X/2, self.y + PLAYER_Y/2, PLAYER_X, PLAYER_Y)
        strokeWeight(1)
    
        
        
        
class Flag:
    def __init__(self, colour):
        self.c = colour
        self.capt = False
        
        if self.c == 'red':
            self.x = PLAYER_X*1
        elif self.c == 'blue':
            self.x = RES_X - PLAYER_X*2
        self.y = RES_Y/2 - PLAYER_Y/2
        
        
    def capture(self, other):
        if self.c != other.c and other.x <= (self.x + PLAYER_X*2) and (other.x + PLAYER_X*2) >= self.x and (other.y + PLAYER_Y*2) >= self.y and other.y <= (self.y + PLAYER_Y*2):
            self.x = other.x
            self.y = other.y - PLAYER_Y
            self.capt = True
            
    def scored(self):

        if self.capt == True and self.c == 'red' and self.x >= (RES_X - PLAYER_X * 2) and self.y >= (RES_Y/2 - PLAYER_Y * 2) and self.y <= (RES_Y/2 + PLAYER_Y):
            game.capt = True
            game.p2_score +=1
            
        if self.capt == True and self.c == 'blue' and self.x <= (PLAYER_X * 2) and self.y >= (RES_Y/2 - PLAYER_Y * 2) and self.y <= (RES_Y/2 + PLAYER_Y):
            game.capt = True
            game.p1_score +=1
            
   
    def display(self):
        self.scored()
        
        self.capture(player_2)
        self.capture(player_1)
        
        if self.c == 'red':
            fill(255,0,0)
            rect(PLAYER_X - 10, RES_Y/2 - PLAYER_Y/2 - 5, PLAYER_X + 15, PLAYER_Y*1.5 + 5)
        if self.c == 'blue':
            fill(0,0,255)
            rect(RES_X - PLAYER_X*2 - 10, RES_Y/2 - PLAYER_Y/2 - 5, PLAYER_X + 15, PLAYER_Y*1.5 + 5)
        line(self.x, self.y, self.x, self.y + PLAYER_Y*1.5)
        triangle(self.x, self.y, self.x, self.y + PLAYER_Y, self.x + PLAYER_X, self.y + PLAYER_Y/2)

#defining an obstacle class for the maps        
class Obstacles:
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def display(self):
        fill(0)
        rect(self.x, self.y, self.w, self.h)
        
map1 = [[RES_X/2 - 50, 0, 100, 100], [RES_X/2-50, RES_Y-100, 100, 100], [RES_X/2 - 50, RES_Y/2 - 25, 100, 50], [RES_X/2 - 200, 0, 35, 125], [RES_X/2 - 200, RES_Y-125, 35, 125], [RES_X/2 + 165, 0, 35, 125], [RES_X/2+165, RES_Y-125, 35, 125]]
map2 = [[RES_X/2 - 50, 75, 100, 100], [RES_X/2 - 50, RES_Y - 175, 100, 100], [RES_X/4 - 25, 50, 50, 50], [RES_X/4 - 25, RES_Y/2 - 25, 50, 50],[RES_X/4 - 25, RES_Y-100, 50, 50], [RES_X*3/4 - 25, 50, 50, 50], [RES_X*3/4 - 25, RES_Y/2 - 25, 50, 50],[RES_X*3/4 - 25, RES_Y-100, 50, 50]]      


def setup():
    size(RES_X, RES_Y)
    background(0,0,0)
    global bump, death, points, game_over, power_up, bgmusic
    minim = Minim(this)
    bump = minim.loadFile("bump.mp3")
    death = minim.loadFile("death.mp3")
    points = minim.loadFile("point_scored.mp3")
    game_over = minim.loadFile("end_game.mp3")
    power_up =  minim.loadFile("power_up.mp3")
    bgmusic = minim.loadFile("bgmusic.mp3")
    bgmusic.setGain(-20)
    bgmusic.rewind()
    bgmusic.play()
    
    
def draw():
    frameRate(250)
    if game.map == 1:
        fill(255,0,0)
        rect(0,0, RES_X/2, RES_Y)
        fill(0,0,255)
        rect(RES_X/2,0, RES_X/2, RES_Y)
    elif game.map == 2:
        fill(164, 42, 4)
        rect(0,0, RES_X/2, RES_Y)
        fill(65, 105, 225)
        rect(RES_X/2,0, RES_X/2, RES_Y)
        

    game.display()
            
    
    
    
def keyPressed():
    player_1.keycontrol(key, True, 'a', 'd', 'w', 's')
    player_2.keycontrol(keyCode, True, LEFT, RIGHT, UP, DOWN)

        
def keyReleased():
    player_1.keycontrol(key, False, 'a', 'd', 'w', 's')
    player_2.keycontrol(keyCode, False, LEFT, RIGHT, UP, DOWN)


def mouseClicked():
    if game.winner != None:
        global game, power, player_2, player_1, flag_1, flag_2
        game = Game()
        power = PowerUp()
        player_2 = Player('blue')
        player_1 = Player('red')
    
        flag_1 = Flag('red')
        flag_2 = Flag('blue')


game = Game()
power = PowerUp()
player_2 = Player('blue')
player_1 = Player('red')

flag_1 = Flag('red')
flag_2 = Flag('blue')
