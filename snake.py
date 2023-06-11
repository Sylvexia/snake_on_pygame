import pygame
import sys
import random
from dataclasses import dataclass


@dataclass
class ColorSet:
    snake = (0, 255, 0)
    grid_even = (3, 0, 46)
    grid_odd = (1, 0, 87)
    food = (255, 0, 0)
    text = (255, 255, 255)


@dataclass
class Dir:
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)


@dataclass
class Playground:
    col_size = 32
    row_size = 24
    width = 800
    height = 600


class Snake():
    def __init__(self):
        col_size = Playground.col_size
        row_size = Playground.row_size
        self.color = ColorSet.snake
        self.length = 1
        self.direction = random.choice([Dir.up, Dir.down, Dir.left, Dir.right])
        self.positions = [((col_size/2), (row_size/2))]
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, dir):
        if self.length > 1 and (dir[0]*-1, dir[1]*-1) == self.direction:
            return
        else:
            self.direction = dir

    def update(self):
        col_size = Playground.col_size
        row_size = Playground.row_size

        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+x)) % col_size, (cur[1]+y) % row_size)
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        col_size = Playground.col_size
        row_size = Playground.row_size

        self.length = 1
        self.positions = [((col_size/2), (row_size/2))]
        self.direction = random.choice([Dir.up, Dir.down, Dir.left, Dir.right])
        self.score = 0

    def draw(self, surface):
        col_size = Playground.col_size
        row_size = Playground.row_size

        grid_width = Playground.width/col_size
        grid_height = Playground.height/row_size
        
        for p in self.positions:
            r = pygame.Rect((p[0]*grid_width, p[1]*grid_height),
                            (grid_width, grid_height))
            pygame.draw.rect(surface, self.color, r)

    def get_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(Dir.up)
                elif event.key == pygame.K_DOWN:
                    self.turn(Dir.down)
                elif event.key == pygame.K_LEFT:
                    self.turn(Dir.left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(Dir.right)


class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = ColorSet.food
        self.randomize_position()

    def randomize_position(self):
        col_size = Playground.col_size
        row_size = Playground.row_size

        self.position = (random.randint(0, col_size-1),
                         random.randint(0, row_size-1))

    def draw(self, surface):
        col_size = Playground.col_size
        row_size = Playground.row_size

        grid_width = Playground.width/col_size
        grid_height = Playground.height/row_size
        
        r = pygame.Rect(
            (self.position[0]*grid_width, self.position[1]*grid_height), (grid_width, grid_height))
        pygame.draw.rect(surface, self.color, r)


def drawGrid(surface):
    col_size = Playground.col_size
    row_size = Playground.row_size

    grid_width = Playground.width/col_size
    grid_height = Playground.height/row_size
    for y in range(0, int(row_size)):
        for x in range(0, int(col_size)):
            if (x+y) % 2 == 0:
                even_rect = pygame.Rect(
                    (x*grid_width, y*grid_height), (grid_width+1, grid_height+1))
                pygame.draw.rect(surface, ColorSet.grid_even, even_rect)
            else:
                even_rect = pygame.Rect(
                    (x*grid_width, y*grid_height), (grid_width+1, grid_height+1))
                pygame.draw.rect(surface, ColorSet.grid_odd, even_rect)

def snake_game(screen):
    
    clock = pygame.time.Clock()

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    myfont = pygame.font.Font('Minecraft.ttf', 16)

    drawGrid(surface)


    while (True):

        events = pygame.event.get()

        snake.get_input(events)
        snake.update()

        if len(snake.positions) > 2 and snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        drawGrid(surface)
        snake.draw(surface)
        food.draw(surface)
        text = myfont.render(f"Score: {snake.score}", 1, ColorSet.text)
        surface.blit(text, (5, 10))

        for event in events:
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.transform.scale(surface, event.dict['size'])

                Playground.width = event.dict['size'][0]
                Playground.height = event.dict['size'][1]

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.blit(surface, (0, 0))

        pygame.display.update()
        clock.tick(10+snake.score*0.5)


if __name__ == "__main__":
    pygame.init()
    snake_game(pygame.display.set_mode((Playground.width, Playground.height), pygame.RESIZABLE))
