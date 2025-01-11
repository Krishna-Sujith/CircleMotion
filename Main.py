import pygame
import numpy as np
# from Chain import *
from ChainRetry import *
from Fish import *

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
FPS=30

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Procedurally Animated")

# basic_chain=ChainRetry([40,10],20,20,math.pi//8)
basic_chain=ChainRetry([40,10],14,15, math.pi/8, vertex_radii=[25,30,35,30,30,25,20,15,8,7,7,6,5,5])

clock=pygame.time.Clock()

backgroundColor=(51, 204, 255)

def debug_print(screen,vector_pos, text=None):
    vector_info=None
    if text is None:
        vector_info = f"Vector: ({vector_pos.x:.2f}, {vector_pos.y:.2f})"
    else:
        vector_info=text
    text_surface = font.render(vector_info, True, 'black')
    screen.blit(text_surface, vector_pos)
    pass

score=0
bounded_rectangle=pygame.rect.Rect(SCREEN_WIDTH//5,SCREEN_HEIGHT//5,(3*SCREEN_WIDTH)//5, (3*SCREEN_HEIGHT)//5)

fishes_list = [Fish(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 40, 20, random.randint(2, 5)) for _ in range(5)]


camera_x, camera_y=0,0
screen_center_x,screen_center_y=SCREEN_WIDTH//2, SCREEN_HEIGHT//2

player_head=basic_chain.vertices[0]

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            break

    if running==False:
        break

    screen.fill(backgroundColor)

    mouse_pos=pygame.mouse.get_pos()
    basic_chain.move_chain(mouse_pos)

    # head_x,head_y=basic_chain.vertices[0].x,basic_chain.vertices[0].y
    # camera_x=head_x-screen_center_x
    # camera_y=head_y-screen_center_y

    # for fish in fishes_list:
    #     # fish.move(x_change,y_change)
    #     fish.rect.x+=camera_x
    #     fish.rect.y+=camera_y
    #     fish.move(0,0)
    #     fish.draw(screen)

    #     fish.rect.x+=camera_x
    #     fish.rect.y+=camera_y

    basic_chain.display(screen)


    ####### THE BOUNDED RECTANGLE CAMERA #################
    head_vector_pos=basic_chain.vertices[0]
    x_change=0
    y_change=0
    if not bounded_rectangle.collidepoint(head_vector_pos.x, head_vector_pos.y):
        # debug_print(screen, head_vector_pos)
        x_point=head_vector_pos.x
        y_point=head_vector_pos.y
        
        if x_point<bounded_rectangle.left:
            x_change=1
        elif x_point>bounded_rectangle.right:
            x_change=-1

        if y_point<bounded_rectangle.top:
            y_change=1
        elif y_point>bounded_rectangle.bottom:
            y_change=-1
    ########################################################
    
    #Printing the score.
    debug_print(screen,pygame.math.Vector2(0,0),f"Score: {score}")

    #Updating the position of the player.
    basic_chain.update_position(x_change,y_change)
    for fish in fishes_list:
        fish.move(x_change,y_change)
        fish.draw(screen)

    for fish in fishes_list:
        fish_rect=fish.rect
        if basic_chain.check_collision_with_fish(fish_rect):
            score+=fish.score
            fishes_list.remove(fish)

            new_fish=Fish(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 40, 20, random.randint(2,5))
            fishes_list.append(new_fish)


    pygame.display.flip()
    clock.tick(FPS)


