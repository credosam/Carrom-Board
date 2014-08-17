import pygame, sys, os, random
from pygame.locals import *
import time, pdb
from striker import *
from coin import *

boardBoundary = pygame.Color(92,51,25)
boardColor = pygame.Color(211,195,141)
holeColor = pygame.Color(0,0,0)
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0, 255, 0)

screen_width=700
screen_height=700
boundary_width=40
hole_rad=25
red_rad=15
rect_width=30
arc_rad=50
arcx=210
arcy=440

friction = 0.01
all_sprite_list = pygame.sprite.Group()
all_coin_list = pygame.sprite.Group()
# class Player(self):
# 	def __init__(self):

		
class Carrom():
	def __init__(self,width=screen_width,height=screen_height,caption='Carrom Board',coin_num = 19):
		pygame.init()
		self.width, self.height = width, height
		self.coin_num = coin_num
		self.carromBoard = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(caption)	
		self.striker = Striker(self.carromBoard)
		self.coins = [0]*coin_num
		for i in range (0,coin_num):
			if i==0:
				curr = True
			else:
				curr = False
			if i%2 == 0:
				temp = True
			else:
				temp = False
			self.coins[i] = Coin(self.carromBoard,temp,curr)
			self.coins[i].position(i)
			all_coin_list.add(self.coins[i])
			all_sprite_list.add(self.coins[i])
		all_sprite_list.add(self.striker)	
		self.run()
		
	def run(self):
		self.drawBoard(self.carromBoard)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if self.striker.state == 3:
				pos = pygame.mouse.get_pos()
				pygame.draw.line(self.carromBoard, pygame.Color(0, 255, 0), (self.striker.rect.centerx,self.striker.rect.centery),(pygame.mouse.get_pos()),5)
				self.striker.velx = (pos[0]-self.striker.rect.centerx)*0.1*(-1)
				self.striker.vely = (pos[1]-self.striker.rect.centery)*0.1*(-1)
				self.striker.state = 0
			if event.type == MOUSEBUTTONDOWN and self.striker.state == 2:
				self.striker.state = 3			
			if self.striker.state == 2:
				pygame.draw.line(self.carromBoard, pygame.Color(0, 255, 0), (self.striker.rect.centerx,self.striker.rect.centery),(pygame.mouse.get_pos()),5)	
			if event.type == MOUSEBUTTONDOWN and self.striker.state == 1:
				self.striker.state = 2				
			if self.striker.state == 1: 
				self.striker.strikepos()
			if event.type == MOUSEBUTTONDOWN and self.striker.state == 0:
				self.striker.state = 1

		all_sprite_list.draw(self.carromBoard)
		for disk1 in all_sprite_list:
		 	for disk2 in all_sprite_list:
		 		if disk1 != disk2 and (not disk1.have_collided or not disk2.have_collided):
		 			self.collide_coin(disk1,disk2)
		self.striker.update_striker()
		for disk in all_sprite_list:
			self.goToHoles(disk)
		for i in range (0,self.coin_num):
			self.coins[i].update_coin()
		for disk1 in all_sprite_list:
			disk1.have_collided = False
		pygame.display.update()
		return True

	def collide_coin(self,disk1,disk2):
		if pygame.sprite.collide_circle(disk1, disk2):
			disk2.have_collided = True
		 	disk1.have_collided = True
			c1x = disk1.rect.centerx
			c1y = disk1.rect.centery
			c2x = disk2.rect.centerx
			c2y = disk2.rect.centery
			if((((c2x-c1x)*(c2x-c1x))+((c2y-c1y)*(c2y-c1y)))<(4*coinRad*coinRad)):
				if c2x>c1x:
					c2x = c2x + coinRad
				else :
					c1x = c1x + coinRad																	
				if c2y>c1y:
					c2y = c2y + coinRad
				else :
					c1y = c1y + coinRad
			if c1x != c2x:
				m = (c2y-c1y)/(c2x-c1x)
				tempx1=(((disk2.velx)*(m*m))-(disk1.vely*m)+disk1.velx+(disk2.vely*m))/((m*m)+1)
				tempx2=(((disk1.velx)*(m*m))-(disk2.vely*m)+(disk2.velx)+(disk1.vely*m))/((m*m)+1)
				tempy1=((disk2.velx*m)+(disk1.vely*(m*m))-(disk1.velx*m)+disk2.vely)/((m*m)+1)
				tempy2=((disk1.velx*m)+(disk2.vely*(m*m))-(disk2.velx*m)+disk1.vely)/((m*m)+1)
				disk1.velx = tempx1
				disk1.vely = tempy1
				disk2.velx = tempx2
				disk2.vely = tempy2
			else:
				tempy1 = disk1.vely
				disk1.vely = disk2.vely
				disk2.vely = tempy1


	def drawBoard(self, board):

		# for boundary and boundary lines
		
		i=0
		r=51
		g=25
		b=0
		for i in range(0, boundary_width):
			# boardBoundary = pygame.Color(r,g,b)
			pygame.draw.rect(board, pygame.Color(r, g, b), (i,i,screen_width-(2*i),i) )
			pygame.draw.rect(board, pygame.Color(r, g, b), (i,i,i,screen_height-(2*i)) )
			pygame.draw.rect(board, pygame.Color(r, g, b), (screen_width-(2*i),i,i,screen_height-(2*i)))
			pygame.draw.rect(board, pygame.Color(r, g, b), (i,screen_height-(2*i),screen_width-(2*i),i))
			r = r+2
			g = g+1

		# for main board on which game is played
		pygame.draw.rect(board, boardColor, (boundary_width,boundary_width,screen_width-(2*boundary_width),screen_width-(2*boundary_width)))

		# for the four holes which are coins final destination
		pygame.draw.circle(board, holeColor, (boundary_width+hole_rad-hole_rad/2,boundary_width+hole_rad-hole_rad/2),hole_rad,0)
		pygame.draw.circle(board, holeColor, (boundary_width+hole_rad-hole_rad/2,screen_width-boundary_width-hole_rad+hole_rad/2),hole_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width-boundary_width-hole_rad+hole_rad/2,boundary_width+hole_rad-hole_rad/2),hole_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width-boundary_width-hole_rad+hole_rad/2,screen_width-boundary_width-hole_rad+hole_rad/2),hole_rad,0)

		# for the circles which is the starting point of the coins
		pygame.draw.circle(board, holeColor, (screen_width/2,screen_width/2),screen_width/10,2)
		pygame.draw.circle(board, holeColor, (screen_width/2,screen_width/2),screen_width/15,2)

		# for the four places from which the player plays the game
		pygame.draw.rect(board, holeColor, (boundary_width+screen_width/6,screen_width/6,screen_width-(2*boundary_width+2*screen_width/6),rect_width), 2)
		pygame.draw.circle(board, redColor, (boundary_width+screen_width/6,screen_width/6 + red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, (boundary_width+screen_width/6,screen_width/6 + red_rad), red_rad,2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - boundary_width,screen_width/6 + red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - boundary_width,screen_width/6 + red_rad), red_rad,2)

		pygame.draw.rect(board, holeColor, (screen_width/6,boundary_width+screen_width/6,rect_width,screen_width-(2*boundary_width+2*screen_width/6)), 2)
		pygame.draw.circle(board, redColor, (screen_width/6 + red_rad,boundary_width+screen_width/6), red_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width/6 + red_rad,boundary_width+screen_width/6), red_rad,2)
		pygame.draw.circle(board, redColor, (screen_width/6 + red_rad,(5*screen_width)/6 - boundary_width), red_rad,0)
		pygame.draw.circle(board, holeColor, (screen_width/6 + red_rad,(5*screen_width)/6 - boundary_width), red_rad,2)

		pygame.draw.rect(board, holeColor, (boundary_width+screen_width/6,(5*screen_width)/6 -rect_width,screen_width-(2*boundary_width+2*screen_width/6),rect_width), 2)
		pygame.draw.circle(board, redColor, (boundary_width+screen_width/6,(5*screen_width)/6 - red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, (boundary_width+screen_width/6,(5*screen_width)/6 - red_rad), red_rad,2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - boundary_width,(5*screen_width)/6 - red_rad), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - boundary_width,(5*screen_width)/6 - red_rad), red_rad,2)

		pygame.draw.rect(board, holeColor, ((5*screen_width)/6 -rect_width,boundary_width+screen_width/6,rect_width,screen_width-(2*boundary_width+2*screen_width/6)), 2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - red_rad,boundary_width+screen_width/6), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - red_rad,boundary_width+screen_width/6), red_rad,2)
		pygame.draw.circle(board, redColor, ((5*screen_width)/6 - red_rad,(5*screen_width)/6 - boundary_width), red_rad,0)
		pygame.draw.circle(board, holeColor, ((5*screen_width)/6 - red_rad,(5*screen_width)/6 - boundary_width), red_rad,2)

		# for the four diagonal design

		pygame.draw.line(board, holeColor, ((7*screen_width/6)/10,(7*screen_width/6)/10), (screen_width/3,screen_width/3), 2)
		pygame.draw.arc(board, holeColor, (arcx,arcx,arc_rad,arc_rad), 0, 6.28,2 )

		pygame.draw.line(board, holeColor, ((7*screen_width/6)/10,screen_width-(7*screen_width/6)/10), (screen_width/3,(2*screen_width)/3), 2)
		pygame.draw.arc(board, holeColor, (arcx,arcy,arc_rad,arc_rad), 0, 6.28,2 )

		pygame.draw.line(board, holeColor, (screen_width-(7*screen_width/6)/10,screen_width-(7*screen_width/6)/10), ((2*screen_width)/3,(2*screen_width)/3), 2)
		pygame.draw.arc(board, holeColor, (arcy,arcy,arc_rad,arc_rad), 0, 6.28,2 )

		pygame.draw.line(board, holeColor, (screen_width-(7*screen_width/6)/10,(7*screen_width/6)/10), ((2*screen_width)/3,screen_width/3), 2)
		pygame.draw.arc(board, holeColor, (arcy,arcx,arc_rad,arc_rad), 0, 6.28,2 )

	def goToHoles(self,disk):
		if((disk.rect.centerx <= boundary_width+hole_rad and disk.rect.centery<=boundary_width+hole_rad) or (disk.rect.centerx >= screen_width-boundary_width-hole_rad and disk.rect.centery<=boundary_width+hole_rad) or (disk.rect.centerx >= screen_width-boundary_width-hole_rad and disk.rect.centery>=screen_width-boundary_width-hole_rad) or (disk.rect.centerx >= boundary_width+hole_rad and disk.rect.centery>=screen_width-boundary_width-hole_rad)) :
			if disk != self.striker:
				all_sprite_list.remove(disk)
				all_coin_list.remove(disk)
			else:
				self.striker.strikepos()
				self.striker.velx=0
				self.striker.vely=0
def main():
    game = Carrom()
    while game.run():
        pass

if __name__ == '__main__':
    main()
# fpsClock.tick(30)