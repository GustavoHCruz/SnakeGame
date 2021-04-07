import pygame
import time
import random

class Window:
    width = 1920
    height = 1080

class Game:
    def start(self):
        self.pixel_width = 10
        self.pixel_height = 10
        self.score = 1
        self.game_close = False
        self.game_over = False
        self.foods = round(window.width/250)

class Snake:
    def start(self):
        self.head = [round((window.width/2) / 10) * 10, round((window.height/2) / 10) * 10]
        self.body = []
        self.score = 1
        self.speed = 20

    def move(self, x, y):
        x = (self.head[0] + x * game.pixel_width)%window.width
        y = (self.head[1] + y * game.pixel_width)%window.height
        self.head = [x, y]

    def position(self):
        self.body.append(self.head)
        if (len(self.body) > self.score):
            self.body.pop(0)

    def scored(self):
        self.score += 1
        if (self.score % 5 == 0):
            self.speed += 1

    def print(self):
        for part in self.body:
            pygame.draw.rect(display, colors['blue'], [part[0], part[1], game.pixel_width, game.pixel_width])

class Food:
    def genereate(self):
        while True:
            counter = 0
            x = round(random.randrange(0, window.width - game.pixel_width) / 10) * 10
            y = round(random.randrange(0, window.height - game.pixel_height) / 10) * 10
            for part in snake.body:
                if [x,y] != part:
                    counter += 1
            if counter == len(snake.body):
                return [x,y]

    def start(self):
        self.position = []
        for i in range(0,game.foods):
            self.position.append(self.genereate())

    def scored(self, index):
        self.position.pop(index)
        self.position.append(self.genereate())

    def print(self):
        for food in self.position:
            pygame.draw.rect(display, colors['green'], [food[0], food[1], 10, 10])

def score(score):
    source = fonts['score'].render('Score: ' + str(score), True, colors['yellow'])
    display.blit(source, [0, 0])

def message(msg, color):
    source = fonts['message'].render(msg, True, color)
    text_rect = source.get_rect(center=(window.width/2,window.height/2))
    display.blit(source, text_rect)

def speed():
    source = fonts['speed'].render('Speed: ' + str(snake.speed), True, colors['yellow'])
    text_rect = source.get_rect()
    display.blit(source, [window.width-text_rect[2], 0])

def gameLoop():
    game.start()
    snake.start()
    food.start()
    mov = [0, 0]

    last_key = pygame.K_q
    while not game.game_close:
        while game.game_over == True:
            display.fill(colors['black'])
            message("You Lost! Press Q-Quit or P-Play Again", colors['red'])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game.game_close = True
                        game.game_over = False
                    if event.key == pygame.K_p or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_close = True
                game.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_key != pygame.K_RIGHT:
                    mov = [-1, 0]
                    last_key = pygame.K_LEFT
                    break
                elif event.key == pygame.K_RIGHT and last_key != pygame.K_LEFT:
                    mov = [1, 0]
                    last_key = pygame.K_RIGHT
                    break
                elif event.key == pygame.K_UP and last_key != pygame.K_DOWN:
                    mov = [0, -1]
                    last_key = pygame.K_UP
                    break
                elif event.key == pygame.K_DOWN and last_key != pygame.K_UP:
                    mov = [0, 1]
                    last_key = pygame.K_DOWN
                    break
        
        snake.move(mov[0], mov[1])

        # if snake.head[0] >= window.width or snake.head[0] < 0 or snake.head[1] >= window.height or snake.head[1] < 0:
        #     game.game_over = True

        display.fill(colors['black'])
        food.print()

        snake.position()

        for part in snake.body[:-1]:
            if part == snake.head:
                game.game_over = True

        snake.print()
        score(snake.score)
        speed()

        pygame.display.update()

        for i in range(0,game.foods):
            if(snake.head[0] == food.position[i][0] and snake.head[1] == food.position[i][1]):
                food.scored(i)
                snake.scored()

        clock.tick(snake.speed)

    pygame.quit()
    quit()

pygame.init()

colors = {'black':(0,0,0), 'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'yellow':(255,255,102), 'white':(255,255,255)}
fonts = {'message':pygame.font.SysFont('bahnschrift', 25), 'score':pygame.font.SysFont('bahnschrift', 35), 'speed':pygame.font.SysFont('bahnschrift', 30)}

window = Window()

display = pygame.display.set_mode((window.width, window.height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake = Snake()
food = Food()
game = Game()

gameLoop()