import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

class Object:
    def __init__(self):
        self.vertices = []
        # self.edge_points = []
        self.polygon_centroid_coord = [0, 0]
        self.closed = False

    def add_vertex(self, x, y):
        self.vertices.append((x, y))
        print(f"Vertex added: ({x}, {y})")
    """
    def find_edge_points(self):
        num_vertices = len(self.vertices)
        for i in range(num_vertices):
            start_vertex = self.vertices[i]
            end_vertex = self.vertices[(i + 1) % num_vertices]  # Wrap around to the first vertex


            if end_vertex[0] == start_vertex[0]: # special case for vertical line
                for y in range(min(start_vertex[1], end_vertex[1]), max(start_vertex[1], end_vertex[1]) + 1):
                    self.edge_points.append((start_vertex[0], y))

            m = (end_vertex[1] - start_vertex[1]) / (end_vertex[0] - start_vertex[0])
            b = start_vertex[1] - m * start_vertex[0]
            for x in range(start_vertex[0], end_vertex[0] + 1):
                y = int(m * x + b)
                self.edge_points.append((x, y))
    """
    def draw_object(self):
        if not self.closed:
            for vertex in self.vertices:
                pygame.draw.circle(screen, (255, 255, 255), vertex, 5)
        if self.closed:
            for i in range(len(self.vertices)):
                start_vertex = self.vertices[i]
                end_vertex = self.vertices[(i + 1) % len(self.vertices)]  # Wrap around to the first vertex
                pygame.draw.line(screen, (255, 255, 255), start_vertex, end_vertex, 2)

    def calculate_centroid_coord(self):
        if not self.vertices:
            return (0, 0)
        # Calculate Polygon Centroid
        A = 0
        for i in range(len(self.vertices)):
            x0, y0 = self.vertices[i]
            x1, y1 = self.vertices[(i + 1) % len(self.vertices)]  # Wrap around to the first vertex
            A += (x0 * y1 - x1 * y0)
        A *= .5

        C_x = 0
        C_y = 0

        for i in range(len(self.vertices)):
            x0, y0 = self.vertices[i]
            x1, y1 = self.vertices[(i + 1) % len(self.vertices)]  # Wrap around to the first vertex
            C_x += (x0 + x1) * (x0 * y1 - x1 * y0)
            C_y += (y0 + y1) * (x0 * y1 - x1 * y0)
        C_x /= (6 * A)
        C_y /= (6 * A)

        self.polygon_centroid_coord = [C_x, C_y]
        return [C_x, C_y]

    def draw_balance(self):
        if self.closed and self.polygon_centroid_coord:
            cx = int(self.polygon_centroid_coord[0])
            # triangle fulcrum with its tip at the bottom of the shape
            # find connection point at specific x

            # two lowest vertices on screen (largest y)
            bottom_vertex1, bottom_vertex2 = sorted(self.vertices, key=lambda v: v[1], reverse=True)[:2]

            # find y that corresponds with cx
            if bottom_vertex1[0] == bottom_vertex2[0]:
                bottom = max(bottom_vertex1[1], bottom_vertex2[1])
            else:
                m = (bottom_vertex1[1] - bottom_vertex2[1]) / (bottom_vertex1[0] - bottom_vertex2[0])
                b = bottom_vertex1[1] - m * bottom_vertex1[0]
                bottom = m*cx + b + 3
                

            tip = (cx, bottom)
            left = (cx - 20, bottom + 40)
            right = (cx + 20, bottom + 40)
            pygame.draw.polygon(screen, (255, 0, 0), [tip, left, right])


class Guesser:
    def __init__(self):
        self.guessing = False
        self.guessed = False
        self.guesses = 0
        self.guess = 0

    def draw_guessing(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.guessing:
            bottom_vertex1, bottom_vertex2 = sorted(object.vertices, key=lambda v: v[1], reverse=True)[:2]

            if bottom_vertex1[0] < bottom_vertex2[0]:
                left_vertex, right_vertex = bottom_vertex1, bottom_vertex2
            else:
                left_vertex, right_vertex = bottom_vertex2, bottom_vertex1


            if right_vertex[0] == left_vertex[0]:
                    bottom = max(right_vertex[1], left_vertex[1])
            else:
                if mouse_x < left_vertex[0]:
                    mouse_x = left_vertex[0]
                elif mouse_x > right_vertex[0]:
                    mouse_x = right_vertex[0]

                m = (bottom_vertex1[1] - bottom_vertex2[1]) / (bottom_vertex1[0] - bottom_vertex2[0])
                b = bottom_vertex1[1] - m * bottom_vertex1[0]
                bottom = m * mouse_x + b + 2

            tip = (mouse_x, bottom)
            left = (mouse_x - 20, bottom + 40)
            right = (mouse_x + 20, bottom + 40)
            pygame.draw.polygon(screen, (100, 0, 0), [tip, left, right])

    def draw_guessed(self):
        mouse_x = self.guess
        if self.guessed:
            bottom_vertex1, bottom_vertex2 = sorted(object.vertices, key=lambda v: v[1], reverse=True)[:2]

            if bottom_vertex1[0] < bottom_vertex2[0]:
                left_vertex, right_vertex = bottom_vertex1, bottom_vertex2
            else:
                left_vertex, right_vertex = bottom_vertex2, bottom_vertex1
            
            if right_vertex[0] == left_vertex[0]:
                bottom = max(right_vertex[1], left_vertex[1])
            else:
                if mouse_x < left_vertex[0]:
                    mouse_x = left_vertex[0]
                elif mouse_x > right_vertex[0]:
                    mouse_x = right_vertex[0]
            
                m = (bottom_vertex1[1] - bottom_vertex2[1]) / (bottom_vertex1[0] - bottom_vertex2[0])
                b = bottom_vertex1[1] - m * bottom_vertex1[0]
                bottom = m * mouse_x + b + 2
            
            tip = (mouse_x, bottom)
            left = (mouse_x - 20, bottom + 40)
            right = (mouse_x + 20, bottom + 40)
            pygame.draw.polygon(screen, (100, 0, 0), [tip, left, right])
            

            



clock = pygame.time.Clock()
object = Object()
guesser = Guesser()
run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balance Equillibrium Finder")
while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not object.closed:
                object.add_vertex(*event.pos)
            elif event.button == 1 and guesser.guessing:
                guesser.guessing = False
                guesser.guessed = True
                guesser.guess = pygame.mouse.get_pos()[0]


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                object.closed = True
                object.polygon_centroid_coord = object.calculate_centroid_coord()
            if event.key == pygame.K_g and object.closed:
                guesser.guessing = True
                guesser.guesses += 1

    screen.fill((0, 0, 0))
    object.draw_object()
    object.draw_balance()
    guesser.draw_guessing()
    guesser.draw_guessed()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()