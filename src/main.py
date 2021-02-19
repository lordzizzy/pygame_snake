import pygame
import sys
import random

from typing import List, Tuple

screen_width = 480
screen_height = 480
gridsize = 20
grid_width = screen_width // gridsize
grid_height = screen_height // gridsize

assert (
    screen_height % 20 == 0 and screen_width % 20 == 0
), f"screen width or height must be multiple of gridsize {gridsize}"

GridPos = Tuple[int, int]

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


class Snake:
    def __init__(self) -> None:
        self.reset()

    def head_pos(self) -> GridPos:
        return self.positions[0]

    def turn(self, dir: GridPos) -> None:
        if self.length > 1 and (dir[0] * -1, dir[1] * -1) == self.direction:
            return
        else:
            self.direction = dir

    def move(self) -> None:
        cur = self.head_pos()
        dx, dy = self.direction
        new = (
            (cur[0] + (dx * gridsize)) % screen_width,
            (cur[1] + (dy * gridsize)) % screen_height,
        )
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self) -> None:
        self.length = 1
        self.positions: List[GridPos] = [(screen_width // 2, screen_height // 2)]
        self.direction = random.choice((up, down, left, right))
        self.color = pygame.Color(17, 24, 47)
        self.score = 0

    def draw(self, surface: pygame.Surface) -> None:
        for x, y in self.positions:
            r = pygame.Rect((x, y), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


class Food:
    def __init__(self) -> None:
        self.position: GridPos = (0, 0)
        self.color = pygame.Color(223, 163, 49)
        self.randomize_pos()

    def randomize_pos(self) -> None:
        self.position = (
            random.randint(0, grid_width - 1) * gridsize,
            random.randint(0, grid_height - 1) * gridsize,
        )

    def draw(self, surface: pygame.Surface) -> None:
        r = pygame.Rect(self.position, (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


def draw_grid(surface: pygame.Surface) -> None:
    for row in range(grid_height):
        for col in range(grid_width):
            color = (93, 216, 228) if (row + col) % 2 == 0 else (84, 194, 205)
            r = pygame.Rect((col * gridsize, row * gridsize), (gridsize, gridsize))
            pygame.draw.rect(surface, color, r)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 16)

    while True:
        clock.tick(10)
        snake.handle_keys()
        draw_grid(surface)
        snake.move()
        if snake.head_pos() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_pos()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render(f"Score {snake.score}", 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()


main()