import math
from PIL import Image

class Canvas:
    def __init__(self, width, height, bg_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.edge_list = []

    def set_pixel(self, x, y, color=(0, 0, 0)):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.pixels[x, y] = color

    def draw_line(self, x0, y0, x1, y1, color=(0, 0, 0)):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        if x0 < x1:
            sx = 1
        else:
            sx = -1
        if y0 < y1:
            sy = 1
        else:
            sy = -1

        err = dx - dy

        while True:
            self.set_pixel(x0, y0, color)

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

    def draw_circle(self, xc, yc, r, color=(0, 0, 0)):
        x = r
        y = 0
        err = 0

        while x >= y:
            self.set_pixel(xc + x, yc + y, color)
            self.set_pixel(xc + y, yc + x, color)
            self.set_pixel(xc - y, yc + x, color)
            self.set_pixel(xc - x, yc + y, color)
            self.set_pixel(xc - x, yc - y, color)
            self.set_pixel(xc - y, yc - x, color)
            self.set_pixel(xc + y, yc - x, color)
            self.set_pixel(xc + x, yc - y, color)

            y += 1
            err += 1 + 2*y

            if 2*(err - x) + 1 > 0:
                x -= 1
                err += 1 - 2*x

    def draw_bezier_curve(self, p0, p1, p2, p3, color=(0, 0, 0)):
        for t in range(0, 101):
            t = t / 100.0
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            self.set_pixel(int(round(x)), int(round(y)), color)

   