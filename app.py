import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

class Object:
    def __init__(self):
        self.vertices = []
        self.edge_points = []
    def add_vertex(self, x, y):
        self.vertices.append((x, y))
        print(f"Vertex added: ({x}, {y})")
    def find_edge_points(self):
        num_vertices = len(self.vertices)
        for i in range(num_vertices):
            start_vertex = self.vertices[i]
            end_vertex = self.vertices[(i + 1) % num_vertices]  # Wrap around to the first vertex
            if start_vertex[0] < start_vertex[1]:
                m = (end_vertex[1] - start_vertex[1]) / (end_vertex[0] - start_vertex[0])
                b = start_vertex[1] - m * start_vertex[0]
                for x in range(start_vertex[0], end_vertex[0] + 1):
                    y = int(m * x + b)
                    self.edge_points.append((x, y))
            else:
                m = (end_vertex[1] - start_vertex[1]) / (end_vertex[0] - start_vertex[0])
                b = start_vertex[1] - m * start_vertex[0]
                for x in range(end_vertex[0], start_vertex[0] + 1):
                    y = int(m * x + b)
                    self.edge_points.append((x, y))

    def draw_object(self):
        for i in range(len(self.vertices)):
            start_vertex = self.vertices[i]
            end_vertex = self.vertices[(i + 1) % len(self.vertices)]  # Wrap around to the first vertex
            pygame.draw.line(screen, (255, 255, 255), start_vertex, end_vertex, 2)


object = Object()
run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balance Equillibrium Finder")
while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 10)
                object.add_vertex(*event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                object.find_edge_points()
                object.draw_object()


    pygame.display.flip()

pygame.quit()