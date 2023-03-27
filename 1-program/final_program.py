import math
from PIL import Image

class GraphicsEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[(0, 0, 0) for x in range(self.width)] for y in range(self.height)]
        self.points = []
        self.edges = []

    def set_color(self, color):
        """Set the current color to use for drawing."""
        self.current_color = color

    def add_point(self, x, y):
        self.points.append((x, y))

    def add_edge(self, start, end):
        self.edges.append((start, end))

    def draw_line(self, start, end, color):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while x1 != x2 or y1 != y2:
            self.canvas[y1][x1] = color
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        self.canvas[y1][x1] = color

    def draw_circle(self, center, radius, color):
        x0, y0 = center
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.canvas[y0 + y][x0 + x] = color
            self.canvas[y0 + x][x0 + y] = color
            self.canvas[y0 - x][x0 + y] = color
            self.canvas[y0 - y][x0 + x] = color
            self.canvas[y0 - y][x0 - x] = color
            self.canvas[y0 - x][x0 - y] = color
            self.canvas[y0 + x][x0 - y] = color
            self.canvas[y0 + y][x0 - x] = color

            y += 1
            err += 1 + 2*y
            if 2*(err - x) + 1 > 0:
                x -= 1
                err += 1 - 2*x

    def draw_bezier_curve(self, p0, p1, p2, p3, color):
        steps = 20
        for i in range(steps):
            t = i / steps
            x = ((1-t)**3)*p0[0] + 3*((1-t)**2)*t*p1[0] + 3*(1-t)*(t**2)*p2[0] + (t**3)*p3[0]
            y = ((1-t)**3)*p0[1] + 3*((1-t)**2)*t*p1[1] + 3*(1-t)*(t**2)*p2[1] + (t**3)*p3[1]
            self.canvas[round(y)][round(x)] = color

    def draw_hermite_curve(self, x0, y0, x1, y1, rx0, ry0, rx1, ry1, color):
        steps = 100
        for i in range(steps):
            t = i / steps
            h1 = 2*(t**3) - 3*(t**2) + 1
            h2 = -2*(t**3) + 3*(t**2)
            h3 = (t**3) - 2*(t**2) + t
            h4 = (t**3) - (t**2)

            x = h1*x0 + h2*x1 + h3*rx0 + h4*rx1
            y = h1*y0 + h2*y1 + h3*ry0 + h4*ry1
            self.canvas[round(y)][round(x)] = color

    def rotate(self, angle):
        # Convert angle from degrees to radians
        angle = math.radians(angle)

        # Generate rotation matrix
        rotation_matrix = [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ]

        # Apply rotation matrix to edges
        self.transform(rotation_matrix)

    def transform(self, matrix):
        new_edges = []
        for edge in self.edges:
            # Convert edge coordinates to homogeneous coordinates
            p0 = [edge[0][0], edge[0][1], 0, 1]
            p1 = [edge[1][0], edge[1][1], 0, 1]

            # Apply transformation matrix to edge
            p0t = [sum([p0[j]*matrix[i][j] for j in range(4)]) for i in range(4)]
            p1t = [sum([p1[j]*matrix[i][j] for j in range(4)]) for i in range(4)]

            # Convert transformed coordinates back to Cartesian coordinates
            p0t = (p0t[0]/p0t[3], p0t[1]/p0t[3])
            p1t = (p1t[0]/p1t[3], p1t[1]/p1t[3])

            new_edges.append((p0t, p1t))

        self.edges = new_edges

    def dilation(self, factor):
        dilation_matrix = [
            [factor, 0, 0],
            [0, factor, 0],
            [0, 0, 1]
        ]
        self.transform(dilation_matrix)

    def translation(self, dx, dy):
        translation_matrix = [
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ]
        self.transform(translation_matrix)

    def parse(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                command = line.strip().lower()
                if command == "line":
                    x0, y0, x1, y1 = map(int, file.readline().split())
                    self.draw_line((x0, y0), (x1, y1))
                elif command == "circle":
                    cx, cy, r = map(int, file.readline().split())
                    self.draw_circle(cx, cy, r)
                elif command == "hermite":
                    p0, p1, r0, r1, *color = map(int, file.readline().split())
                    self.draw_hermite_curve(p0, p1, r0, r1, tuple(color))
                elif command == "bezier":
                    x0, y0, x1, y1, x2, y2, x3, y3, *color = map(int, file.readline().split())
                    self.draw_bezier_curve(x0, y0, x1, y1, x2, y2, x3, y3, tuple(color))

    def save_image(self, filename):
        image = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        pixels = image.load()
        for i in range(self.height):
            for j in range(self.width):
                pixels[j, i] = self.canvas[i][j]
        image.save(filename, "PNG")

# Create a new GraphicsEngine object with canvas size 500x500
g = GraphicsEngine(500, 500)

# Set the color to yellow
g.set_color((255, 255, 0))

# Draw the face (a circle)
g.draw_circle((250, 250), 200, (255, 255, 0))

# Set the color to black
g.set_color((0, 0, 0))

# Draw the left eye (a circle)
g.draw_circle((150, 175), 25, (255, 255, 0))

# Draw the right eye (a circle)
g.draw_circle((350, 175), 25, (255, 255, 0))

# Draw the mouth (a Bezier curve)
g.draw_hermite_curve(150, 350, 350, 350, 250, 250, 250, -250, (255, 255, 0))

# Save the image as "smiley.png"
g.save_image("smiley.png")