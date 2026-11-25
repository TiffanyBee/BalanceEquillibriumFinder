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
            bottom = max(y for _, y in self.vertices)   # lowest point on screen (y grows downward)
            # triangle fulcrum with its tip at the bottom of the shape
            tip = (cx, bottom)
            left = (cx - 20, bottom + 40)
            right = (cx + 20, bottom + 40)
            pygame.draw.polygon(screen, (255, 0, 0), [tip, left, right])

clock = pygame.time.Clock()
object = Object()
run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balance Equillibrium Finder")
while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 :
                object.add_vertex(*event.pos)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                object.closed = True
                object.polygon_centroid_coord = object.calculate_centroid_coord()

    screen.fill((0, 0, 0))
    object.draw_object()
    object.draw_balance()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()