import pygame
import math
import numpy as np


pi_in_rad=math.pi
half_pi=pi_in_rad/2
pi_in_rad_twice=2*pi_in_rad

WHITE=(255,255,255)
RED=(255,0,0)

pygame.init()
font_size=30
font = pygame.font.Font(None, font_size)


#Bézier Curve Function for four control points
def bezier_curve(P0, P1, P2, P3, num_points=100):
    points = []
    for t in np.linspace(0, 1, num_points):
        B = (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3
        points.append(B)
    return points

#Function to handle multiple points (more than 4)
def bezier_from_points(points, num_points_per_segment=100):
    all_curve_points = []
    
    #Iterating over the points in segments of 4
    for i in range(0, len(points) - 3, 3):
        P0 = points[i]
        P1 = points[i + 1]
        P2 = points[i + 2]
        P3 = points[i + 3]
        
        #Generating the bezier curve for the current set of 4 points
        curve_points = bezier_curve(P0, P1, P2, P3, num_points=num_points_per_segment)
        all_curve_points.extend(curve_points)
    
    return all_curve_points



class ChainRetry:
    def __init__(self, origin, vertexCount, edgeSize, min_angle, vertex_radii):
        self.origin=origin
        self.vertexCount=vertexCount
        self.edgeSize=edgeSize
        self.min_angle=min_angle
        self.vertex_radii=vertex_radii

        self.movement_speed=8
        self.health=100

        self.initial_offset_vec=pygame.math.Vector2(1,0)*self.edgeSize

        #Creating the vertices.
        self.vertices=[pygame.math.Vector2(self.origin[0],self.origin[1])]
        for i in range(1, self.vertexCount):
            next_point=self.vertices[i-1].copy() + self.initial_offset_vec.copy()
            self.vertices.append(next_point)

        #Creating the angles for the edges between mouse+1st vertex, and the other edges between the adj vertices. Represents the direction in which the vertex will be moving.
        self.angles=[0.0]
        for i in range(1, self.vertexCount):
            self.angles.append(0.0)

    def draw_health_bar(self, screen):
        bar_width=200
        bar_height=20
        x=20
        y=20

        pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen,(100,100,100),(x,y,bar_width,bar_height))

        health_width=(self.health/100)*bar_width

        if self.health>30:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, bar_height))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, health_width, bar_height))

        health_text = font.render(f"Health: {self.health}%", True, WHITE)
        screen.blit(health_text, (x + bar_width + 10, y))

    def move_chain(self,mouse_pos):
        mouse_vec=pygame.math.Vector2(mouse_pos[0],mouse_pos[1])

        move_to_target_vec=mouse_vec-self.vertices[0]
        move_to_target_vec=move_to_target_vec.normalize()

        #Updating the angle in which the first vertex has moved.
        self.angles[0]=math.atan2(move_to_target_vec.y,move_to_target_vec.x)

        #Updating the first vertex position. The head is moved based on it's movement speed.
        self.vertices[0]+=move_to_target_vec*self.movement_speed

        #Updating the rest of the vertices. The other vertices move based on the edge length.
        for i in range(1, self.vertexCount):
            updated_edge_vec=self.vertices[i-1]-self.vertices[i]
            curr_angle=math.atan2(updated_edge_vec.y,updated_edge_vec.x)         #The angle at which the current point is expected to move.
            self.angles[i] = self.constrain_angle(curr_angle, self.angles[i - 1], self.min_angle)
            self.vertices[i]=self.vertices[i-1].copy()-pygame.math.Vector2(math.cos(self.angles[i]),math.sin(self.angles[i]))*self.edgeSize


            # if updated_edge_vec.magnitude()>0:
                # updated_edge_vec=updated_edge_vec.normalize()

            # self.vertices[i]=self.vertices[i-1].copy()-updated_edge_vec*self.edgeSize
    
    def update_position(self,x_change,y_change):
        for vertices in self.vertices:
            vertices.x+=x_change*self.movement_speed
            vertices.y+=y_change*self.movement_speed
        pass

    def constrain_angle(self,angle,anchor,constraint):
        diff = self.relative_angle_diff(angle, anchor)
        if abs(diff) <= constraint:
            return self.simplify_angle(angle)
        if diff > constraint:
            return self.simplify_angle(anchor - constraint)
        return self.simplify_angle(anchor + constraint)

    def relative_angle_diff(self, angle, anchor):
        angle = self.simplify_angle(angle + math.pi - anchor)
        anchor = math.pi
        return anchor - angle
    
    def simplify_angle(self, angle):
        while angle >= 2 * math.pi:
            angle -= 2 * math.pi
        while angle < 0:
            angle += 2 * math.pi
        return angle
    
    def check_collision_with_fish(self, fish):
        # for idx, vertex in enumerate(self.vertices):
        #     circle_center=vertex
        #     circle_radius=self.vertex_radii[idx]

        #     closest_x=max(fish.left, min(circle_center.x, fish.right))
        #     closest_y=max(fish.top, min(circle_center.y, fish.bottom))

        #     distance=pygame.math.Vector2(circle_center.x - closest_x, circle_center.y - closest_y).length()

        #     if distance <= circle_radius:
        #         return True
        
        head_vertex = self.vertices[0]
        head_rad=self.vertex_radii[0]

        closest_x=max(fish.left, min(head_vertex.x, fish.right))
        closest_y=max(fish.top, min(head_vertex.y, fish.bottom))
        distance=pygame.math.Vector2(head_vertex.x-closest_x,head_vertex.y-closest_y).magnitude()
        
        return distance<=head_rad

    def check_collision_with_bubble(self,bubble):
        head_vertex = self.vertices[0]
        distance = pygame.math.Vector2(head_vertex.x - bubble.x, head_vertex.y - bubble.y).magnitude()

        if distance <= bubble.radius + self.vertex_radii[0]:
            self.health -= int(bubble.radius * 0.5)
            if self.health < 0:
                self.health=0
            return True
        return False

    def display(self, screen):
        pygame.draw.lines(screen,WHITE,False,self.vertices,3)
        for idx,vertex in enumerate(self.vertices):
            pygame.draw.circle(screen,RED, vertex,self.vertex_radii[idx],0)

        head_vertex = self.vertices[0]
        head_radius = self.vertex_radii[0]
        head_angle = self.angles[0]

        eye_offset_distance = head_radius // 2
        eye_offset_angle = math.pi / 4


        left_eye_pos=(
        head_vertex.x+eye_offset_distance*math.cos(head_angle-eye_offset_angle),
        head_vertex.y+eye_offset_distance*math.sin(head_angle-eye_offset_angle),
        )
        right_eye_pos=(
            head_vertex.x+eye_offset_distance*math.cos(head_angle+eye_offset_angle),
            head_vertex.y+eye_offset_distance*math.sin(head_angle+eye_offset_angle),
        )

        eye_radius =max(2, head_radius // 5)  # Adjusting eye size based on head size
        pygame.draw.circle(screen, WHITE, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, WHITE, right_eye_pos, eye_radius)


        pupil_radius= max(1, eye_radius // 2)
        pupil_offset_distance =eye_radius // 2  #Adding some pupil offset to add some directionality.
        pupil_left_pos= (
            left_eye_pos[0]+pupil_offset_distance*math.cos(head_angle),
            left_eye_pos[1]+pupil_offset_distance*math.sin(head_angle),
        )
        pupil_right_pos=(
            right_eye_pos[0]+pupil_offset_distance*math.cos(head_angle),
            right_eye_pos[1]+pupil_offset_distance*math.sin(head_angle),
        )
        pygame.draw.circle(screen, (0, 0, 0), pupil_left_pos, pupil_radius)
        pygame.draw.circle(screen, (0, 0, 0), pupil_right_pos, pupil_radius)

        self.draw_health_bar(screen)

        # points=[]
        # for i in range(1, self.vertexCount):

        #     #Adding the right side
        #     x_pos=self.vertices[i].x + math.cos(self.angles[i]+half_pi)*self.vertex_radii[i]
        #     y_pos=self.vertices[i].y + math.cos(self.angles[i]+half_pi)*self.vertex_radii[i]
        #     points.append(np.array([x_pos,y_pos]))
            
        # for i in range(1,self.vertexCount):
        #     idx=self.vertexCount-i
        #     #Adding the right side
        #     x_pos=self.vertices[idx].x + math.cos(self.angles[idx]+half_pi)*self.vertex_radii[idx]
        #     y_pos=self.vertices[idx].y + math.cos(self.angles[idx]+half_pi)*self.vertex_radii[idx]
        #     points.append(np.array([x_pos,y_pos]))

        # # Get all the curve points from the list of points
        # curve_points = bezier_from_points(points, num_points_per_segment=100)

        # if len(curve_points) > 1:
        #     pygame.draw.aalines(screen, (255, 255, 255), False, curve_points, 2)
