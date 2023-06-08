import pygame
import sys
import random
from dataclasses import dataclass

@dataclass
class ColorSet:
    snake = (0,255,0)
    grid_even = (3,0,46)
    grid_odd = (1,0,87)
    food = (255,0,0)
    text = (255,255,255)
    
@dataclass
class Dir:
    up = (0,-1)
    down = (0,1)
    left = (-1,0)
    right = (1,0)
    
class Snake():
    def __init__(self):
        self.length = 1
        self.direction = random.choice([Dir.up, Dir.down, Dir.left, Dir.right])
        self.positions = [((col_size/2), (row_size/2))]
        self.color = ColorSet.snake
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, dir):
        if self.length > 1 and (dir[0]*-1, dir[1]*-1) == self.direction:
            return
        else:
            self.direction = dir

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+x))%col_size, (cur[1]+y)%row_size)
        self.positions.insert(0,new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((col_size/2), (row_size/2))]
        self.direction = random.choice([Dir.up, Dir.down, Dir.left, Dir.right])
        self.score = 0

    def draw(self,surface):
        grid_width = screen_width/col_size
        grid_height = screen_height/row_size
        for p in self.positions:
            r = pygame.Rect((p[0]*grid_width, p[1]*grid_height), (grid_width,grid_height))
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
        self.position = (0,0)
        self.color = ColorSet.food
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, col_size-1), random.randint(0, row_size-1))

    def draw(self, surface):
        grid_width = screen_width/col_size
        grid_height = screen_height/row_size
        r = pygame.Rect((self.position[0]*grid_width, self.position[1]*grid_height), (grid_width,grid_height))
        pygame.draw.rect(surface, self.color, r)

def drawGrid(surface):
    grid_width = screen_width/col_size
    grid_height = screen_height/row_size
    for y in range(0, int(row_size)):
        for x in range(0, int(col_size)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*grid_width, y*grid_height), (grid_width,grid_height))
                pygame.draw.rect(surface, ColorSet.grid_even, r)
            else:
                rr = pygame.Rect((x*grid_width, y*grid_height), (grid_width,grid_height))
                pygame.draw.rect(surface, ColorSet.grid_odd, rr)

screen_width = 640
screen_height = 480
col_size = 32
row_size = 24

def main():
    global screen_width
    global screen_height 

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, 32)
    
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    
    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",16)
    
    drawGrid(surface)

    while (True):
        
        events = pygame.event.get()
                        
        snake.get_input(events)
        
        snake.move()
        
        if len(snake.positions) > 2 and snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
            
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                surface = pygame.transform.scale(surface,event.dict['size'])
                # get ratio
                
                screen_width = event.dict['size'][0]
                screen_height = event.dict['size'][1]
                
                print(event.dict['size'])
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
        drawGrid(surface)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render(f"Score: {snake.score}", 1, ColorSet.text)
        screen.blit(text, (5,10))
        
        pygame.display.update()
        clock.tick(10+snake.score*0.5)

main()