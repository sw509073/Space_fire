import pygame
import turtle
import os
import math
import random
#pygame.init()


#Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

EXPLOSION_SPEED=4


#Register the shapes
wn.register_shape("invader.gif")
wn.register_shape("player.gif")

class Explosion(pygame.sprite.Sprite):
	def __init__(self,x,y,scale):
		pygame.sprite.Sprite.__init__(self)
		self.images=[]
		self.frame_index=0
		for i in range(1,6):
			img=pygame.image.load(f'/Users/satvikwazir/Desktop/Game/Space Invaders/explosion/exp{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.image=self.images[self.frame_index]
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.counter=0
	
	def update(self):
		EXPLOSION_SPEED=4
		self.counter+=1
		if self.counter>=EXPLOSION_SPEED:
			self.counter=0
			self.frame_index+=1
		if self.frame_index>=len(self.images):
			self.kill()
		else:
			self.image=self.images[self.frame_index]

explosion_group=pygame.sprite.Group()


#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(600)
	border_pen.lt(90)
border_pen.hideturtle()	

#Set the score to 0
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_pen.write("Score:0", align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player.speed = 0

enemy_hit=0

#Choose a number of enemies
number_of_enemies = 30
#Create an empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
	#Create the enemy
	enemies.append(turtle.Turtle())

enemy_start_x=-200
enemy_start_y=250
enemy_number=0

for enemy in enemies:
	enemy.color("red")
	enemy.shape("invader.gif")
	enemy.penup()
	enemy.speed(0)
	x = enemy_start_x+(50*enemy_number)
	y = enemy_start_y
	enemy.setposition(x, y)
	enemy_number+=1
	if enemy_number==10:
		enemy_start_y-=50
		enemy_number=0

enemyspeed = 0.5


#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 40

#Define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"


#Move the player left and right
def play_sound(sound_file,time=0):
	os.system("afplay {}&".format(sound_file))
	if time>0:
		turtle.ontimer(lambda: play_sound(sound_file,time),t=int(time*1000))

def move_left():
	player.speed=-10
	
def move_right():
	player.speed=10

def player_move():
	x = player.xcor()
	x += player.speed
	if x>290:
		x=290	
	if x<-290:
		x=-290
	player.setx(x)
	
def fire_bullet():
	#Declare bulletstate as a global if it needs changed
	global bulletstate
	if bulletstate == "ready":
		play_sound("laser.wav")
		bulletstate = "fire"
		#Move the bullet to the just above the player
		x = player.xcor()
		y = player.ycor() + 10
		bullet.setposition(x, y)
		bullet.showturtle()

def isCollision(t1, t2):
	distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
	if distance < 20:
		return True
	else:
		return False
#Create keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

#play_sound("bgm.mp3",119)

#Main game loop
while True:
	wn.update()
	
	player_move()

	explosion_group.update()
	explosion_group.draw(wn)
	
	for enemy in enemies:
		#Move the enemy
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)

		#Move the enemy back and down
		if enemy.xcor() > 280:
			#Move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			#Change enemy direction
			enemyspeed *= -1
		
		if enemy.xcor() < -280:
			#Move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			#Change enemy direction
			enemyspeed *= -1
			
		#Check for a collision between the bullet and the enemy
		if isCollision(bullet, enemy):
			play_sound("explosion.wav")
			#Reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			#Reset the enemy
			enemy.setposition(0,100000)
			#explosion=Explosion(bullet.xcor,bullet.ycor,0.5)
			#explosion_group.add(explosion)

			enemy_hit+=1
			#Update the score
			score_pen.clear()
			score += 10
			score_pen.write("Score:{}".format(score), align="left", font=("Arial", 14, "normal"))

		if enemy_hit>29:
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		
		if isCollision(player, enemy):
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		
	#Move the bullet
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)
	
	#Check to see if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"


delay = raw_input("Press enter to finsh.")