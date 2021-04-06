import os
import sys
from random import randint

import numpy
import pygame

from cells import Cell

from variables import *


class SpriteGroup(pygame.sprite.Group):
    def update(self, game):
        pygame.sprite.Group.update(self, game)

    def render(self, screen):
        self.draw(screen)


class CellsFieldImage(pygame.Surface):
    def __init__(self):
        super().__init__((window_width, window_height))
        self.color = (140, 140, 140)
        self.fill(self.color)
        self.grey_square = pygame.Surface((10, 10))
        self.grey_square.fill(self.color)

    def move(self, start_x, start_y, end_x, end_y, image):
        self.delete(start_x, start_y)
        self.add(image, end_x, end_y)

    def add(self, image, x, y):
        self.blit(image, pygame.Rect(x * 10, y * 10, 10, 10))

    def delete(self, x, y):
        self.blit(self.grey_square, pygame.Rect(x * 10, y * 10, 10, 10))


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 1000
        self.energy_field = numpy.array([[{'photosynthesis': 5} for i in range(90)] for j in range(
            60)])
        self.cells_field = numpy.array([[None for i in range(window_width // 10)] for j in range(
            window_height // 10)])
        self.cells_field_image = CellsFieldImage()
        self.cells_group = SpriteGroup()

        # self.previous_cells_field = self.cells_field
        # self.generate_cells()
        # for i in range(40):
        #     self.cells_field[i][i + 1] = Cell((i, i + 1), self)
        self.cells_field[10][9] = Cell((10, 9), self)
        self.cells_field[9][10] = Cell((9, 10), self)
        # self.cells_field[10][10] = Cell((10, 10), self)
        # self.cells_field[11][10] = Cell((11, 10), self)
        # self.cells_field[10][11] = Cell((10, 11), self)
        # self.cells_field[11][11] = Cell((11, 11), self)
        self.dead_cells_group = SpriteGroup()

        # for i in range(0, 2):
        #     self.cells_field[10][10 + (-1) ** i] = Cell((10, 10 + (-1) ** i), self)
        # for i in range(0, 2):
        #     self.cells_field[10 + (-1) ** i][10] = Cell((10 + (-1) ** i, 10), self)

    def generate_cells(self):
        for i in range(window_height // 10):
            for j in range(window_width // 10):
                if randint(0, 1):
                    self.cells_field[i][j] = Cell((i, j), self)

    def run(self):
        import variables
        from interface_logic import window
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    os._exit(1)
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [sprite for sprite in self.cells_group if sprite.rect.collidepoint(pos)]
                    if clicked_sprites:
                        window.fill_genome_field(clicked_sprites[0])
                        print("clicked")
            with stop_lock:
                if variables.stop:
                    continue
            self.screen.blit(self.cells_field_image, (0, 0))
            self.draw()
            self.update()
            # self.previous_cells_field = self.cells_field

            self.clock.tick(self.fps)
            pygame.display.flip()

    def update(self):

        for cell in self.cells_group:
            cell.update(self)

    def draw(self):
        pass
