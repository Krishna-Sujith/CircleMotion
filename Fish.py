import pygame
import random

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
FISH_COLOR=(255, 102, 0)      #orange
TAIL_COLOR=(255, 0, 0)        #red.
FIN_COLOR=(200,0,0)


class Fish:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)  
        self.speed = speed

        self.score=self.speed-1

        #Fish moves straight or in zigzag.
        self.direction = random.choice(["straight", "zigzag"])  
        self.zigzag_toggle = True 
        self.zigzag_step = random.randint(20, 50)  

    def update_pos_player_based(self, x_change, y_change,player_speed):
        self.rect.x+=x_change*player_speed
        self.rect.y+=y_change*player_speed

    def move(self, x_change,y_change,player_speed):
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

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0  
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH  
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0  

        self.update_pos_player_based(x_change,y_change,player_speed)

    def draw(self, screen):
        # pygame.draw.rect(screen, FISH_COLOR, self.rect)
        body_width = int(self.rect.width * 1.2)
        body_height = int(self.rect.height * 1.2)
        body_center = self.rect.center

        #Drawing the fish body as an ellipse.
        pygame.draw.ellipse(screen, FISH_COLOR, pygame.Rect(body_center[0] - body_width // 2, body_center[1] - body_height // 2, body_width, body_height))

        #Drawing fish tail, reduced the size a bit.
        tail_width = body_width // 6  
        tail_height = body_height // 4
        tail_points = [
            (body_center[0] - body_width // 2, body_center[1] - tail_height),
            (body_center[0] - body_width // 2 - tail_width, body_center[1]),
            (body_center[0] - body_width // 2, body_center[1] + tail_height),
        ]
        pygame.draw.polygon(screen, FISH_COLOR, tail_points)

        upper_fin_points = [
            (body_center[0] - body_width // 4, body_center[1] - body_height // 2),
            (body_center[0], body_center[1] - body_height // 1.5),  
            (body_center[0] + body_width // 4, body_center[1] - body_height // 2),
        ]
        
        lower_fin_points = [
            (body_center[0] - body_width // 4, body_center[1] + body_height // 2),
            (body_center[0], body_center[1] + body_height // 1.5), 
            (body_center[0] + body_width // 4, body_center[1] + body_height // 2), 
        ]
        
        #Drawing fins
        pygame.draw.polygon(screen, FIN_COLOR, upper_fin_points)
        pygame.draw.polygon(screen, FIN_COLOR, lower_fin_points)

        #Drawing the eyes.
        eye_radius = body_width // 15 
        eye_x = body_center[0] + body_width // 4 
        eye_y = body_center[1] - body_height // 8 
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), eye_radius)
