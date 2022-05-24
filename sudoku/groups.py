import pygame

from game import game

from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *


class Row(Group):
    def __init__(self, id, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.id = id

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.id}'

    def draw(self, surface: Surface) -> None:
        if self.id % 3 == 0:
            pygame.draw.line(surface, 'Black', (0, self.id*game.square_len), (9*game.square_len, self.id*game.square_len), 2)
        else:
            pygame.draw.line(surface, 'Black', (0, self.id*game.square_len), (9*game.square_len, self.id*game.square_len), 1)


class Col(Group):
    def __init__(self, id, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.id = id

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.id}'

    def draw(self, surface: Surface) -> None:
        if self.id % 3 == 0:
            pygame.draw.line(surface, 'Black', (self.id*game.square_len, 0), (self.id*game.square_len, 9*game.square_len), 2)
        else:
            pygame.draw.line(surface, 'Black', (self.id*game.square_len, 0), (self.id*game.square_len, 9*game.square_len), 1)


class BigSquare(Group):
    def __init__(self, id, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.id = id

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.id}'


class Diagram(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.full_rect = pygame.Rect((0, 0), (9*game.square_len, 9*game.square_len))

    def draw_border(self, surface: Surface) -> None:
        pygame.draw.line(surface, 'Black', self.full_rect.topleft, self.full_rect.topright, 6)
        pygame.draw.line(surface, 'Black', self.full_rect.topleft, self.full_rect.bottomleft, 6)
        pygame.draw.line(surface, 'Black', self.full_rect.bottomleft, self.full_rect.bottomright, 10)
        pygame.draw.line(surface, 'Black', self.full_rect.topright, self.full_rect.bottomright, 10)

    def draw(self, surface: Surface) -> List[Rect]:
        for square in self.sprites():
            square.draw(surface)
        self.draw_border(surface)
        return super().draw(surface)
