import pygame
from pygame.rect import Rect
from pygame import Surface

class Cell:
    def __init__(self, x, y, width, height):
        self.surroundingMines: int = 0
        self.isMine: bool = False
        self.isFlagged: bool = False
        self.rect: Rect = pygame.Rect((x, y, width, height))
        self.surface: Surface = pygame.Surface((width - 1, height - 1))
        self.displayNum: bool = False
        self.pos = (x // width, y // height)