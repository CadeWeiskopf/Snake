from operator import truediv
from tkinter import Y
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random
from tkinter import messagebox

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [[(GRIDSIZE / 2) - 1, (GRIDSIZE / 2) - 1]]
        trail = []
        self.head = self.positions[0]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 255, 0)

    def getHeadPosition(self):
        return self.positions[0]

    def turn(self, direction):
        xDirection, yDirection = direction
        if len(self.positions) == 1 or [self.positions[0][0] + xDirection, self.positions[0][1] + yDirection] != self.positions[1]:
            self.direction = direction

    def moveTrail(self):
        moveX, moveY = self.direction
        oldPosition = [self.positions[0][0], self.positions[0][1]]

        self.positions[0][0] += moveX
        if self.positions[0][0] < 0:
            self.positions[0][0] = GRIDSIZE - 1
        elif self.positions[0][0] > GRIDSIZE - 1:
            self.positions[0][0] = 0

        self.positions[0][1] += moveY
        if self.positions[0][1] < 0:
            self.positions[0][1] = GRIDSIZE - 1
        elif self.positions[0][1] > GRIDSIZE - 1:
            self.positions[0][1] = 0

        tail = self.positions[1 : ]
        if self.positions[0] in tail:
            global gameOver
            gameOver = True
            return

        #head moves-- part behind head moves to head old position
        # part behind part moves to old part position
        # repeated until last part is moved
        for i in range(1, len(self.positions)):
            temp = [self.positions[i][0], self.positions[i][1]]
            self.positions[i][0] = oldPosition[0]
            self.positions[i][1] = oldPosition[1]
            oldPosition = temp

    def move(self):
        moveX, moveY = self.direction
        for pos in self.positions:
            pos[0] += moveX
            if pos[0] < 0:
                pos[0] = GRIDSIZE - 1
            elif pos[0] > GRIDSIZE - 1:
                pos[0] = 0

            pos[1] += moveY
            if pos[1] < 0:
                pos[1] = GRIDSIZE - 1
            elif pos[1] > GRIDSIZE - 1:
                pos[1] = 0
    
    def eatApple(self):
        tailX, tailY = self.positions[len(self.positions) - 1]
        dirX, dirY = self.direction
        newTail = [tailX - dirX, tailY - dirY]
        self.positions.append(newTail)

class Apple(object):
    def __init__(self, snake):
        self.x = random.randint(1, GRIDSIZE - 1)
        self.y = random.randint(1, GRIDSIZE - 1)
        #self.y = GRIDSIZE - 1
        validSpawn = False
        while validSpawn == False:
            for pos in snake.positions:
                if pos[0] == self.x and pos[1] == self.y:
                    validSpawn = False
                else:
                    validSpawn = True
            self.x = random.randint(1, GRIDSIZE - 1)
            self.y = random.randint(1, GRIDSIZE - 1)

    def setNewPosition(self, snake):
        self.x = random.randint(1, GRIDSIZE - 1)
        self.y = random.randint(1, GRIDSIZE - 1)
        #self.y = GRIDSIZE - 1
        validSpawn = False
        while validSpawn == False:
            for pos in snake.positions:
                if pos[0] == self.x and pos[1] == self.y:
                    validSpawn = False
                else:
                    validSpawn = True
            self.x = random.randint(1, GRIDSIZE - 1)
            self.y = random.randint(1, GRIDSIZE - 1)

def drawGame(surface, snake, apple):
    for y in range(0, int(GRIDSIZE)):
        for x in range(0, int(GRIDSIZE)):
            if apple.x == x and apple.y == y:
                pygame.draw.rect(surface, (255, 0, 0), r)
                if snake.head[0] + 1 == apple.x and snake.head[1] == apple.y:
                    snake.eatApple()
                    apple.setNewPosition(snake)

            #else:
            rBorder = pygame.Rect((x * GRID_WIDTH, y * GRID_HEIGHT), (GRID_WIDTH, GRID_HEIGHT))
            r = pygame.Rect((x * GRID_WIDTH, y * GRID_HEIGHT), (GRID_WIDTH-1, GRID_HEIGHT-1))
            snakeSpot = False
            index = 0
            for snakeX, snakeY in snake.positions:
                if snakeX == x and snakeY == y:
                    if index == 0:
                        pygame.draw.rect(surface, (0, 0, 0), rBorder)
                        pygame.draw.rect(surface, (0, 255, 255), r)
                    else:
                        pygame.draw.rect(surface, (0, 0, 0), rBorder)
                        pygame.draw.rect(surface, (0, 255, 0), r)
                    snakeSpot = True
                    break
                index += 1

            if snakeSpot == False:
                if (x + y) % 2 == 0:
                    pygame.draw.rect(surface, (0, 0, 0), rBorder)
                    pygame.draw.rect(surface, (128, 128, 128), r)
                else:
                    pygame.draw.rect(surface, (0, 0, 0), rBorder)
                    pygame.draw.rect(surface, (47, 79, 79), r)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

gameOver = False

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size()).convert()
    #drawGrid(surface)

    snake = Snake()
    apple = Apple(snake)

    drawGame(surface, snake, apple)

    score = 0
    running = True
    while running:
        clock.tick(10)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        drawGame(surface, snake, apple)

        if gameOver:
            print('Game Over')
            messagebox.showinfo(title='Game Over', message='The game will close now...')
            break

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    snake.turn(UP)
                elif event.key == K_DOWN:
                    snake.turn(DOWN)
                elif event.key == K_LEFT:
                    snake.turn(LEFT)
                elif event.key == K_RIGHT:
                    snake.turn(RIGHT)
            elif event.type == QUIT:
                running = False

        snake.moveTrail()
        #apple = Apple(snake)

if __name__ == '__main__':
    main()