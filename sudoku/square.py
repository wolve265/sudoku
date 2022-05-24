import pygame

from game import game

from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface
from typing import *


class Square(Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.row: int = self.groups()[0].id
        self.col: int = self.groups()[1].id
        self.hoovered: bool = False
        self.selected: bool = False
        self.locked: bool = False
        self.value: int = 0
        self.image: pygame.Surface = game.font.render(f'0', True, 'Black')
        self.full_rect = pygame.Rect((self.row*game.square_len, self.col*game.square_len), (game.square_len, game.square_len))
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def __repr__(self) -> str:
        return f'{super().__repr__()} | pos = ({self.row},{self.col})'

    def draw(self, surface: Surface) -> None:
        fill_color = 'White'
        if self.hoovered and self.selected:
            fill_color = 'cadetblue'
        elif self.selected:
            fill_color = 'cadetblue1'
        elif self.hoovered or self.locked:
            fill_color = 'Gray90'
        pygame.draw.rect(surface, fill_color, self.full_rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.update_hoovered()
        self.update_image()
        return super().update(*args, **kwargs)

    def update_hoovered(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.hoovered = self.full_rect.collidepoint(mouse_pos)

    def update_image(self) -> None:
        font_color = 'Gray20'
        if self.locked:
            font_color = 'Black'
        if self.value and (1 <= self.value <= 9):
            self.image: pygame.Surface = game.font.render(f'{self.value}', True, font_color)
        else:
            self.image: pygame.Surface = game.font.render(f'', True, font_color)

    def init_value(self, value: int) -> None:
        self.value = 0
        self.hoovered = False
        self.selected = False
        self.locked = False

        value = int(value)
        if value and (1 <= value <= 9):
            self.value = value
            self.locked = True

    def set_value(self, value: int) -> None:
        if self.locked:
            return
        self.value = value

    def clear_value(self) -> None:
        if self.locked:
            return
        self.value = 0

    def select(self) -> None:
        if self.locked:
            return
        self.selected = True

    def deselect(self) -> None:
        if self.locked:
            return
        self.selected = False
