import pygame
import random

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
FISH_COLOR = (255, 102, 0)


class Fish:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)  
        self.speed = speed

        self.score=self.speed-1

        #Fish moves straight or in zigzag.
        self.direction = random.choice(["straight", "zigzag"])  
        self.zigzag_toggle = True 
        self.zigzag_step = random.randint(20, 50)  

    def update_pos_player_based(self, x_change, y_change):
        self.rect.x+=x_change*self.speed
        self.rect.y+=y_change*self.speed

    def move(self, x_change,y_change):
        if self.direction == "straight":
            self.rect.y += self.speed
        elif self.direction == "zigzag":
            if self.zigzag_toggle:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
            

            self.rect.y += self.speed

            self.zigzag_step -= 1
            if self.zigzag_step <= 0:
                self.zigzag_toggle = not self.zigzag_toggle
                self.zigzag_step = random.randint(20, 50)
              
        #Handling the case when fish tries to go outside the borders of the screen.
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0  
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH  
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0  

        self.update_pos_player_based(x_change,y_change)

    def draw(self, screen):
        pygame.draw.rect(screen, FISH_COLOR, self.rect)
