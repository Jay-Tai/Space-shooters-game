#Import modules
import os
import random
import turtle

#Setup turtle
turtle.fd(0)
turtle.speed(0)
turtle.bgpic("space_background.png")
turtle.ht()
turtle.setundobuffer(1)
turtle.title("Peak Chaos")
turtle.tracer(3)

#Defining the player
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx,starty)
        self.speed=1

    def move(self):
        self.fd(self.speed)
        if self.xcor()>290:
            self.setx(290)
            self.lt(60)
        if self.xcor()<-290:
            self.setx(-290)
            self.lt(60)
        if self.ycor()>290:
            self.sety(290)
            self.lt(60)
        if self.ycor()<-290:
            self.sety(-290)
            self.lt(60)

    
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.85,stretch_len=1.1,outline=None)
        self.speed=4
        self.lives=3
    def collisiondetection(self,other):
        if (self.xcor()>=(other.xcor()-20)) and \
        (self.xcor()<=(other.xcor()+20)) and \
        (self.ycor()<=(other.ycor()+20)) and \
        (self.ycor()>=(other.ycor()-20)):
            return True
        else:
            return False
        
    
#Making turning functions
    def turnleft(self):
        self.lt(45)
    def turnright(self):
        self.rt(45)
    def decelerate(self):
        self.speed-=1
    def acelerate(self):
        self.speed+=1

#Classifying the game
class Game():
    def __init__(self):
        self.level=1
        self.score=0
        self.state="playing"
        self.pen=turtle.Turtle()
        self.lives=3
    def showscore(self):
        self.pen.undo()
        msg="Score:%s" %(self.score)
        self.pen.penup()
        self.pen.goto(-275,310)
        self.pen.write(msg,font=("Arial",15,"normal"))
    
    def drawborder(self):
        #Drawing the border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.setheading(random.randint(0,360))
        self.speed=10

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed=20
        self.status="ready"
        self.shapesize(stretch_wid=0.3,stretch_len=0.4,outline=None)
        self.goto(10000000,10000000)
    def fire(self):
        if self.status=="ready":
            os.system("afplay pew.mp3&")
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status="firing"
    def move(self):
        if self.status=="firing":
            self.fd(self.speed)
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.status = "ready"
            self.goto(10000000,10000000)
    def collisiondetection(self,other):
        if (self.xcor()>=(other.xcor()-20)) and \
        (self.xcor()<=(other.xcor()+20)) and \
        (self.ycor()<=(other.ycor()+20)) and \
        (self.ycor()>=(other.ycor()-20)):
            return True
        else:
            return False

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.setheading(random.randint(0,360))
        self.speed = 6
        def collisiondetection(self,other):
            if (self.xcor()>=(other.xcor()-20)) and \
            (self.xcor()<=(other.xcor()+20)) and \
            (self.ycor()<=(other.ycor()+20)) and \
            (self.ycor()>=(other.ycor()-20)):
                return True
            else:
                return False

#Creating the game object
game=Game()

#Creating the border
game.drawborder()

#Showing the score
game.showscore()

#Creating the sprites
player=Player("triangle","white", 0,0)
#enemy=Enemy("circle","red",100,100)
missile=Missile("triangle","yellow",player.xcor(),player.ycor())
#ally=Ally("square","green",0,0)

enemies=[]
allies=[]
for i in range(3):
    enemies.append(Enemy("circle","red",100,100))
    allies.append(Ally("square","green",0,0))

#Setting up Keyboard bindings
turtle.onkey(player.turnleft,"Left")
turtle.onkey(player.turnright,"Right")
turtle.onkey(player.acelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire,"p")
turtle.listen()

#Making the main loop
while True:
    player.move()
    for enemy in enemies:
        enemy.move()
        if player.collisiondetection(enemy):
            x=random.randint(-250,250)
            y=random.randint(-250,250)
            enemy.goto(x,y)
            game.score-=50
            game.showscore()
        
        if missile.collisiondetection(enemy):
            x=random.randint(-250,250)
            y=random.randint(-250,250)
            enemy.goto(x,y)
            missile.goto(1000,1000)
            game.score+=100
            game.showscore()
    missile.move()
    for ally in allies:
        ally.move()
    
        if missile.collisiondetection(ally):
            x=random.randint(-250,250)
            y=random.randint(-250,250)
            ally.goto(x,y)
            missile.goto(1000,1000)
            game.score-=150
            game.showscore()