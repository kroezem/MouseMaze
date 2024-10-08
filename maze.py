import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Surface(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Maze:
    def __init__(self, map_file, size=50, stroke=2):
        ascii_map = [line.rstrip('\n') for line in open(map_file, 'r')]

        self.walls = pygame.sprite.Group()
        self.start = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()

        for row, line in enumerate(ascii_map):
            for col, cell in enumerate(line):
                x = col * size // 4
                y = row * size // 2
                try:
                    if cell == 'o':
                        if line[col + 1:col + 4] == '---':
                            self.walls.add(Surface(x, y, size, stroke, WHITE))
                        if ascii_map[row + 1][col] == '|':
                            self.walls.add(Surface(x, y, stroke, size, WHITE))
                        if ascii_map[row + 1][col + 2] == 'G':
                            self.goal.add(Surface(x + stroke, y + stroke, size - stroke, size - stroke, GREEN))
                        if ascii_map[row + 1][col + 2] == 'S':
                            self.start.add(Surface(x + stroke, y + stroke, size - stroke, size - stroke, RED))
                except IndexError:
                    pass

    def draw(self, screen):
        self.walls.draw(screen)
        self.start.draw(screen)
        self.goal.draw(screen)
