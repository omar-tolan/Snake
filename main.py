import pygame
import time
import random
from pygame.locals import *
SIZE = 40


class game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        pygame.mixer.init()
        self.play_background_music()
        self.score = 0
        self.surface = pygame.display.set_mode((1520, 800))
        self.surface.fill((0, 0, 0))
        self.snake = snake(self.surface, 1)
        self.snake.draw_snake()
        self.apple = apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load(
            r"C:\Users\M.Adel\Desktop\ASU\CS workspace\Snake\resources\bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound(
                r"C:\Users\M.Adel\Desktop\ASU\CS workspace\Snake\resources\1_snake_game_resources_crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound(
                r"C:\Users\M.Adel\Desktop\ASU\CS workspace\Snake\resources\1_snake_game_resources_ding.mp3")

        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load(
            r"C:\Users\M.Adel\Desktop\ASU\CS workspace\Snake\resources\background.jpg")
        self.surface.blit(bg, (0, 0))

    def reset(self):
        self.snake = snake(self.surface, 1)
        self.apple = apple(self.surface)

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        game_over = font.render(
            f"GAME OVER: you scored {self.score}", True, (255, 255, 255))
        self.surface.blit(game_over, (750, 400))
        replay = font.render(f"Hit Enter to try again", True, (255, 255, 255))
        self.surface.blit(replay, (800, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def is_collision(self, xapple, yapple, xsnake, ysnake):
        if xsnake == xapple and ysnake == yapple:
            return True
        else:
            return False

    def outofbounds(self):
        if self.snake.x[0] == 1520 or self.snake.x[0] == 0 or self.snake.y[0] == 800 or self.snake.y[0] == 0:
            return True
        else:
            return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(score, (10, 10))

    def play(self):
        self.render_background()
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        if(self.is_collision(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0])):
            self.play_sound("ding")
            self.apple.move()
            self.snake.grow()
            self.score += 1
        for i in range(1, self.snake.length):
            if(self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]) or self.outofbounds()):
                self.play_sound('crash')
                raise "Collision"

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            time.sleep(0.2)


class apple:
    def __init__(self, parent_screen):
        self.x = SIZE * 5
        self.y = SIZE * 5
        self.image = pygame.image.load(
            r"C:\Users\M.Adel\Desktop\ASU\CS workspace\Snake\resources\apple.jpg").convert()
        self.parent_screen = parent_screen
        parent_screen.blit(self.image, (self.x, self.y))

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 37) * SIZE
        self.y = random.randint(0, 19) * SIZE


class snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            r"C:\Users\M.Adel\Desktop\ASU\CS workspace\Snake\resources\snakeblock.jpg").convert()
        self.parent_screen.blit(self.block, (0, 0))
        self.length = length
        self.x = [0] * length
        self.y = [0] * length
        self.dir = "right"

    def draw_snake(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.dir = "up"

    def move_down(self):
        self.dir = "down"

    def move_left(self):
        self.dir = "left"

    def move_right(self):
        self.dir = "right"

    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.dir == "right":
            self.x[0] += SIZE
            self.draw_snake()
        if self.dir == "left":
            self.x[0] -= SIZE
            self.draw_snake()
        if self.dir == "up":
            self.y[0] -= SIZE
            self.draw_snake()
        if self.dir == "down":
            self.y[0] += SIZE
            self.draw_snake()

    def grow(self):
        self.x.append(-1)
        self.y.append(-1)
        self.length += 1


if __name__ == "__main__":
    game = game()
    game.run()
