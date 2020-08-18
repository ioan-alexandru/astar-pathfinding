import pygame
import math
from queue import PriorityQueue

WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Visualization')

black = (0, 0, 0)  # walls
white = (255, 255, 255)  # cells
beige = (245, 245, 220)  # search
blue = (0, 0, 255)  # neighbors
yellow = (255, 255, 0)  # path from start to end
green = (0, 255, 0)  # end
orange = (255, 165, 0)  # start
grey = (220, 220, 220)  # grid


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].color == black:
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].color == black:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].color == black:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].color == black:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, otherNode):
        return False


def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1-x2)+abs(y1-y2)


def show_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = yellow
        draw()


def a_star(draw, grid, start, end):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            show_path(came_from, end, draw)
            end.color = green
            start.color = orange
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = blue
        draw()
        if current != start:
            current.color = beige
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(screen, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(screen, grey, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(screen, grey, (j*gap, 0), (j*gap, width))


def draw(screen, grid, rows, width):
    screen.fill(white)
    for row in grid:
        for node in row:
            node.draw(screen)
    draw_grid(screen, rows, width)
    pygame.display.update()


def get_cursor_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col


def main(screen, width):
    ROWS = 50
    grid = make_grid(50, WIDTH)
    start = None
    end = None

    run = True

    while run:
        draw(screen, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_cursor_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.color = orange
                elif not end and node != start:
                    end = node
                    end.color = green
                elif node != start and node != end:
                    node.color = black

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_cursor_position(pos, ROWS, width)
                node = grid[row][col]
                node.color = white
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: draw(screen, grid, ROWS, width),
                           grid, start, end)
                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(screen, WIDTH)
