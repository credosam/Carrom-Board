import pygame, sys, os, random
from pygame.locals import *
import time, pdb

boardBoundary = pygame.Color(143,100,55)
boardColor = pygame.Color(211,184,141)
holeColor = pygame.Color(0,0,0)
redColor = pygame.Color(255,0,0)
whiteColor = pygame.Color(255,255,255)
blueColor = pygame.Color(0,0,255)
pinkColor = pygame.Color(176,48,96)
coinRad = 20
coinVelx = 0
coinVely = 0
screen_width = 700
screen_height = 700
boundary_width = 40
friction = 0.01


class Coin(pygame.sprite.Sprite):
	def __init__(self,board,is_white = "False", is_queen = "False"):
		pygame.sprite.Sprite.__init__(self)
		self.is_white = is_white
		self.is_queen = is_queen
		self.have_collided = False
		self.draw()
		self.velx = coinVelx
		self.vely = coinVely
		self.screen_height = screen_height
		self.screen_width = screen_width

	def draw(self):
		self.image = pygame.Surface([coinRad,coinRad])
		self.image.fill(boardColor)
		self.image.set_colorkey(boardColor)
		if self.is_queen:
			pygame.draw.circle(self.image,pinkColor,(coinRad/2,coinRad/2),coinRad/2,0)
		elif self.is_white:
			pygame.draw.circle(self.image,whiteColor,(coinRad/2,coinRad/2),coinRad/2,0)
		else:
			pygame.draw.circle(self.image,holeColor,(coinRad/2,coinRad/2),coinRad/2,0)
		pygame.draw.circle(self.image,holeColor,(coinRad/2,coinRad/2),coinRad/2,2)
		self.rect = self.image.get_rect()
		self.radius = coinRad/2
		self.rect.x = random.randrange(35,540)
		self.rect.y = random.randrange(35,540)

	def position(self,i):
		if(i==0):
			self.rect.x = self.screen_width/2-coinRad/2
			self.rect.y = self.screen_height/2-coinRad/2

		elif(i==1):
			self.rect.x = self.screen_width/2-coinRad/2
			self.rect.y = self.screen_height/2-3*coinRad/2
		elif(i==2):
			self.rect.x = self.screen_width/2 + (coinRad/2)
			self.rect.y = self.screen_height/2 -2*coinRad/2
		elif(i==3):
			self.rect.x = self.screen_width/2 +(coinRad/2)
			self.rect.y = self.screen_height/2
		elif(i==4):
			self.rect.x = self.screen_width/2 - (coinRad/2)
			self.rect.y = self.screen_height/2 + coinRad/2
		elif(i==5):
			self.rect.x = self.screen_width/2 - 3*(coinRad/2)
			self.rect.y = self.screen_height/2
		elif(i==6):
			self.rect.x = self.screen_width/2 -3*(coinRad/2)
			self.rect.y = self.screen_height/2 - 2*coinRad/2
		elif(i==7):
			self.rect.x = self.screen_width/2 - 5*(coinRad/2)
			self.rect.y = self.screen_height/2 - coinRad/2
		elif(i==8):
			self.rect.x = self.screen_width/2 - 5*(coinRad/2)
			self.rect.y = self.screen_height/2 - 3*coinRad/2
		elif(i==9):
			self.rect.x = self.screen_width/2 - 3*(coinRad/2)
			self.rect.y = self.screen_height/2 - 4*coinRad/2
		elif(i==10):
			self.rect.x = self.screen_width/2 - (coinRad/2)
			self.rect.y = self.screen_height/2 - 5*coinRad/2
		elif(i==11):
			self.rect.x = self.screen_width/2 + (coinRad/2)
			self.rect.y = self.screen_height/2 - 4*coinRad/2
		elif(i==12):
			self.rect.x = self.screen_width/2 + 3*(coinRad/2)
			self.rect.y = self.screen_height/2 - 3*coinRad/2
		elif(i==13):
			self.rect.x = self.screen_width/2 + 3*(coinRad/2)
			self.rect.y = self.screen_height/2 - coinRad/2
		elif(i==14):
			self.rect.x = self.screen_width/2 + 3*(coinRad/2)
			self.rect.y = self.screen_height/2 + coinRad/2
		elif(i==15):
			self.rect.x = self.screen_width/2 + (coinRad/2)
			self.rect.y = self.screen_height/2 + 2*coinRad/2
		elif(i==16):
			self.rect.x = self.screen_width/2 - (coinRad/2)
			self.rect.y = self.screen_height/2 + 3*coinRad/2
		elif(i==17):
			self.rect.x = self.screen_width/2 - 3*(coinRad/2)
			self.rect.y = self.screen_height/2 + 2*coinRad/2
		elif(i==18):
			self.rect.x = self.screen_width/2 - 5*(coinRad/2)
			self.rect.y = self.screen_height/2 + coinRad/2
    

	def update_coin(self):
		self.rect.x = self.rect.x + self.velx 
		self.rect.y = self.rect.y + self.vely
		if(self.rect.x > screen_width-boundary_width -coinRad):
			self.velx = -1*self.velx
			self.rect.x = screen_width-boundary_width-coinRad
		if(self.rect.x < boundary_width):
			self.velx = -1*self.velx
			self.rect.x = boundary_width
		if(self.rect.y > screen_width-boundary_width-coinRad):
			self.vely = -1*self.vely
			self.rect.y = screen_width-boundary_width-coinRad
		if(self.rect.y < boundary_width):
			self.vely = -1*self.vely
			self.rect.y = boundary_width

		if(abs(self.velx)<0.5*friction):
			self.velx = 0
		else:
			self.velx = self.velx - friction*self.velx
		
		if(abs(self.vely)<0.5*friction):
			self.vely = 0
		else:
			self.vely = self.vely - friction*self.vely


