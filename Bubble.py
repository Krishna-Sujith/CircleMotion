import pygame
import random

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
BUBBLE_COLOR=(172,216,230) #Light blue color for the bubble.



class Bubble:
    def __init__(self):
        self.radius = random.randint(10, 30)
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = SCREEN_HEIGHT + self.radius  # Start below the screen
        self.zigzag_amount = random.randint(1, 3)  # Amount of zigzag steps
        self.direction = random.choice([1, -1])  # Direction of zigzag
        self.speed = random.uniform(0.5, 2)  # Upward speed of bubble
        self.zigzag_step_count = 0
        self.zigzag_speed = 0.5

    def move(self, x_change,y_change,player_speed):
        self.y -= self.speed
        
        if self.zigzag_step_count < self.zigzag_amount:
            self.x += self.direction * self.zigzag_speed
            self.zigzag_step_count += 1
        else:
            self.direction *= -1 
            self.zigzag_step_count = 0
        
        #Resetting the bubble when it goes out.
        if self.y < -self.radius:
            self.__init__()

        self.x+=x_change*player_speed
        self.y+=y_change*player_speed

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', (int(self.x), int(self.y)), self.radius, 2)
        pygame.draw.circle(screen, BUBBLE_COLOR, (int(self.x), int(self.y)), self.radius-2)
