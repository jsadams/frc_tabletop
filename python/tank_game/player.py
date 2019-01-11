import pygame
import player
import copy
from colors import *
import loader_utils

from pygame.math import Vector2


# the rect element is used to blit the sprite

class Frame(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=2):
        self.position= Vector2(x,y)
        self.heading= Vector2(0,0)
        #self.velocity= Vector2(0,0)
        self.rotation_rate=0
        self.set_heading_angle(angle)
        self.forward_speed=0
        self.side_speed=0

        self.dt=1
        self.verbosity=0
        #self.is_macanum=False
        self.is_macanum=True
        
    def set_heading_angle(self,theta):
        self.heading.from_polar([1,theta])
                       
    def get_heading_angle(self):
        return self.heading.as_polar()[1]
        
    def changespeed(self, a_x, a_y):
        if a_y !=0:
            self.change_forward_speed(a_y)
        elif a_x !=0:
            self.change_side_speed(a_x)        

    def change_forward_speed(self, dv):
        self.forward_speed+=dv

    def change_side_speed(self, dv):
        if self.is_macanum:
            self.side_speed+=dv

    def rotate(self,delta_angle):
        self.rotation_rate+=delta_angle
  
    def update_base(self):
        
   
        theta=self.get_heading_angle()

        velocity=Vector2(self.side_speed,self.forward_speed)
        velocity.rotate_ip(-theta)
        
        self.position = self.position+self.dt*velocity

        delta_angle=self.rotation_rate*self.dt
        self.heading.rotate_ip(delta_angle)

        if self.verbosity > 5:
            print "center=",self.position,
            print "delta_angle=",delta_angle,
            print "heading_angle=",self.get_heading_angle()

 
#####################################################################
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y,color=BLUE, angle=2):

        # Call the parent's constructor
        super(Player,self).__init__()

        self.verbosity=0
        

        width=15
        length=38

        if True:
            self.image = pygame.Surface((width,length), pygame.SRCALPHA)
            self.image.fill(color)
        else:
            picture = pygame.image.load('./data/playerShip1_orange.png')
            self.image=pygame.transform.scale(picture, (width,length))

        self.image_original=self.image
        self.rect_original=self.image_original.get_rect()
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
        self.frame=Frame(x,y,angle)
        # self.position= Vector2(x,y)
        # self.heading= Vector2(0,0)
        # #self.velocity= Vector2(0,0)
        # self.rotation_rate=0
        # self.set_heading_angle(angle)
        # self.forward_speed=0
        # self.side_speed=0

        self.dt=1

        # self.last_position=0
        # self.last_heading=0
        # self.last_rotation_rate=0

    def changespeed(self, a_x, a_y):
        if a_y !=0:
            self.frame.change_forward_speed(a_y)
        elif a_x !=0:
            self.frame.change_side_speed(a_x)        

        

    def update(self,all_sprites_list):

        backup_frame=copy.deepcopy(self.frame)
        self.update_base()
        
        for sprite in all_sprites_list:
            if self != sprite:
                if self.is_collided_with(sprite):
                    self.frame=copy.deepcopy(backup_frame)

        

    def store_starting_position(self):
        self.last_position=position
        self.last_heading=heading
        self.last_forward
        
    def update_base(self):

   
        # theta=self.get_heading_angle()

        # velocity=Vector2(self.side_speed,self.forward_speed)
        # velocity.rotate_ip(-theta)
        
        # self.frame.position = self.frame.position+self.dt*velocity

        # delta_angle=self.rotation_rate*self.dt
        # self.frame.heading.rotate_ip(delta_angle)

        # if self.verbosity > 5:
        #     print "center=",self.frame.position,
        #     print "delta_angle=",delta_angle,
        #     print "heading_angle=",self.get_heading_angle()


        
        self.frame.update_base()
        self.update_rect_heading_and_position()  

    def update_rect_heading_and_position(self):
        angle= self.frame.get_heading_angle()
        rect_orig=self.image_original.get_rect()
        
        self.image = pygame.transform.rotate(self.image_original, angle)
        ### get the center from the original image
        self.rect = self.image.get_rect(center=rect_orig.center)

        #now translate the whole thing
        self.rect.move_ip(self.frame.position.x,self.frame.position.y)

    def rotate(self,delta_angle):
        #self.rotation_rate+=delta_angle
        self.frame.rotate(delta_angle)
        
        
    def is_collided_with(self, sprite):
        is_collided=self.rect.colliderect(sprite.rect)
        return is_collided
