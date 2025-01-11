import pygame
import math
pi_rad=math.pi

pygame.init()
font_size=30
font = pygame.font.Font(None, font_size)
colors = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (0, 255, 255),    # Cyan
    (255, 0, 255),    # Magenta
    (255, 165, 0),    # Orange
    (128, 0, 128),    # Purple
    (255, 192, 203),  # Pink
    (165, 42, 42),    # Brown
    (128, 128, 128),  # Gray
    (0, 255, 0),      # Lime
    (128, 128, 0),    # Olive
    (0, 128, 128),    # Teal
    (0, 0, 128),      # Navy
    (128, 0, 0),      # Maroon
    (255, 215, 0),    # Gold
    (255, 127, 80),   # Coral
    (64, 224, 208),   # Turquoise
    (238, 130, 238),  # Violet
]

class Chain:
    def __init__(self, origin, jointCount, linkSize,angleConstraint):
        self.origin=origin
        self.jointCount=jointCount
        self.linkSize=linkSize
        self.angleConstraint=angleConstraint

        self.animation_speed=8

        self.joints=[pygame.math.Vector2(self.origin[0],self.origin[1])]
        # print('originally, points: ')
        self.angles=[0]
        self.x_axis_vector=pygame.math.Vector2(0,1)

        for i in range(1, self.jointCount):
            next_point=self.joints[i-1].copy()
            next_point.y+=self.linkSize
            self.joints.append(next_point)
            self.angles.append(0)
            # print('the new point is at: ',next_point.x, ',',next_point.y)
        # print('joints are at: ',self.joints)

    def move_head(self, mouse_pos):
        # print('joints are at: ',self.joints)
        mouse_vec=pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
        orig_head_pos=self.joints[0].copy()
        direction_to_move=mouse_vec-orig_head_pos
        self.angles[0]=math.radians(direction_to_move.angle_to(self.x_axis_vector))

        # print('new location update',self.joints[0], ' and the new thing: ', self.joints[0]+direction_to_move.normalize()*8)
        self.joints[0]+=direction_to_move.normalize()*self.animation_speed
        # print('original head_pos: ',orig_head_pos, ' and the after part: ',self.joints[0])
        # print('direction_to_move: ',direction_to_move.normalize()*8)

        for i in range(1,self.jointCount):
            edge_vec = self.joints[i] - self.joints[i - 1]
            curr_angle = edge_vec.angle_to(pygame.math.Vector2(0, -1)) * (math.pi / 180)  # Angle in radians
            self.angles[i] = self.constrain_angle(curr_angle, self.angles[i - 1], self.angleConstraint)

            # Set the joint's position based on the angle
            self.joints[i] = self.joints[i - 1] - pygame.math.Vector2(
                math.cos(self.angles[i]), math.sin(self.angles[i])
            ) * self.linkSize
            # print('at 0th', self.joints[i-1])
            # print('at 1th', self.joints[i])
            # edge_vec=self.joints[i]-self.joints[i-1]
            # print('edge_vec diff', edge_vec)
            # curr_angle=math.radians(edge_vec.angle_to(self.x_axis_vector))

            # self.angles[i]=self.constrainAngle(curr_angle,self.angles[i-1],self.angleConstraint)
            # self.joints[i]=self.joints[i-1].copy()-pygame.math.Vector2(math.cos(self.angles[i]),math.sin(self.angles[i]))*self.linkSize
            # if edge_vec.magnitude()!=0:
                # self.joints[i]-=edge_vec.normalize()*self.linkSize
            

        pass

    def display(self,screen):
        for i in range(0,self.jointCount-1):
            start_point=self.joints[i]
            end_point=self.joints[i+1]
            # if i==0:
            #     self.debug_print(f'{end_point.x}, {end_point.y}',end_point,screen,i)
            pygame.draw.line(screen,colors[i],start_point,end_point,5)
            # self.debug_print(f'{start_point.x}, {start_point.y}',start_point,screen,i)
        pass
    
    def debug_print(self, msg, top_left_vec,screen,i):
        if i==0:
            text_surface = font.render(msg, True, 'red')
        else:
            text_surface = font.render(msg, True, 'green')
        screen.blit(text_surface, (top_left_vec.x,top_left_vec.y))
        pass

    def constrain_angle(self,angle, anchor, constraint):
        diff = self.relative_angle_diff(angle, anchor)
        if abs(diff) <= constraint:
            return self.simplify_angle(angle)
        if diff > constraint:
            return self.simplify_angle(anchor - constraint)
        return self.simplify_angle(anchor + constraint)

    def relative_angle_diff(self,angle, anchor):
        angle = self.simplify_angle(angle + math.pi - anchor)
        anchor = math.pi
        return anchor - angle

    def simplify_angle(self,angle):
        while angle >= 2 * math.pi:
            angle -= 2 * math.pi
        while angle < 0:
            angle += 2 * math.pi
        return angle
