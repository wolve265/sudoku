import csv
import pygame
import sys

from enum import Enum, auto
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Group, Sprite
from pygame.surface import Surface
from random import randint
from typing import *


SCALE = 10


class State(Enum):
    START_SCREEN = auto()
    GAME = auto()
    END_SCREEN = auto()


class StartButton(Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image: pygame.Surface = font.render(f'Start Game', True, 'Black', 'Gray60')
        self.rect = self.image.get_rect(center=screen.get_rect().center)


class StartScreen(Group):
    def __init__(self) -> None:
        self.button = StartButton()
        super().__init__(self.button)

    def draw(self, surface: Surface) -> List[Rect]:
        screen.fill('White')
        return super().draw(surface)

    def actions(self, event: pygame.event.Event) -> None:
        global state
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.button.rect.collidepoint(event.pos):
                state = State.GAME
                game.init()


class RestartButton(Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image: pygame.Surface = font.render(f'Restart Game', True, 'Black', 'Gray60')
        self.rect = self.image.get_rect(center=screen.get_rect().center)


class CongratulationsText(Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image: pygame.Surface = font.render(f'Congratulations', True, 'Black', 'Gray60')
        self.rect = self.image.get_rect(centerx=screen.get_rect().centerx, top=0)


class EndScreen(Group):
    def __init__(self) -> None:
        self.button = RestartButton()
        self.congratulations = CongratulationsText()
        super().__init__(self.button, self.congratulations)

    def draw(self, surface: Surface) -> List[Rect]:
        screen.fill('White')
        return super().draw(surface)

    def actions(self, event: pygame.event.Event) -> None:
        global state
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.button.rect.collidepoint(event.pos):
                state = State.GAME
                game.init()


class Square(Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.row: int = self.groups()[0].id
        self.col: int = self.groups()[1].id
        self.hoovered: bool = False
        self.selected: bool = False
        self.locked: bool = False
        self.value: int = 0
        self.image: pygame.Surface = font.render(f'0', True, 'Black')
        self.bg_rect = pygame.Rect((self.row*SQUARE_LEN, self.col*SQUARE_LEN), (SQUARE_LEN, SQUARE_LEN))
        self.rect = self.image.get_rect(center=self.bg_rect.center)

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
        pygame.draw.rect(surface, fill_color, self.bg_rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.update_hoovered()
        self.update_image()
        return super().update(*args, **kwargs)

    def update_hoovered(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.hoovered = self.bg_rect.collidepoint(mouse_pos)

    def update_image(self) -> None:
        font_color = 'Gray20'
        if self.locked:
            font_color = 'Black'
        if self.value and (1 <= self.value <= 9):
            self.image: pygame.Surface = font.render(f'{self.value}', True, font_color)
        else:
            self.image: pygame.Surface = font.render(f'', True, font_color)

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


class Row(Group):
    def __init__(self, id, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.id = id

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.id}'

    def draw(self, surface: Surface) -> None:
        if self.id % 3 == 0:
            pygame.draw.line(surface, 'Black', (0, self.id*SQUARE_LEN), (9*SQUARE_LEN, self.id*SQUARE_LEN), 2)
        else:
            pygame.draw.line(surface, 'Black', (0, self.id*SQUARE_LEN), (9*SQUARE_LEN, self.id*SQUARE_LEN), 1)


class Col(Group):
    def __init__(self, id, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.id = id

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.id}'

    def draw(self, surface: Surface) -> None:
        if self.id % 3 == 0:
            pygame.draw.line(surface, 'Black', (self.id*SQUARE_LEN, 0), (self.id*SQUARE_LEN, 9*SQUARE_LEN), 2)
        else:
            pygame.draw.line(surface, 'Black', (self.id*SQUARE_LEN, 0), (self.id*SQUARE_LEN, 9*SQUARE_LEN), 1)


class BigSquare(Group):
    def __init__(self, id, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.id = id

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.id}'


class Sudoku(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.bg_rect = pygame.Rect((0, 0), (9*SQUARE_LEN, 9*SQUARE_LEN))

    def draw_border(self, surface: Surface) -> None:
        pygame.draw.line(surface, 'Black', self.bg_rect.topleft, self.bg_rect.topright, 6)
        pygame.draw.line(surface, 'Black', self.bg_rect.topleft, self.bg_rect.bottomleft, 6)
        pygame.draw.line(surface, 'Black', self.bg_rect.bottomleft, self.bg_rect.bottomright, 10)
        pygame.draw.line(surface, 'Black', self.bg_rect.topright, self.bg_rect.bottomright, 10)

    def draw(self, surface: Surface) -> List[Rect]:
        for square in self.sprites():
            square.draw(surface)
        self.draw_border(surface)
        return super().draw(surface)


class Game:
    def __init__(self) -> None:
        self.sudoku: Sudoku = Sudoku()
        self.rows: list[Row] = []
        self.cols: list[Col] = []
        self.big_squares: list[BigSquare] = []
        self.squares: list[Square] = []
        for i in range(9):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
            self.big_squares.append(BigSquare(i))
        for x in range(9):
            for y in range(9):
                self.squares.append(Square(self.rows[y], self.cols[x], self.big_squares[int(x/3)+int(y/3)*3], self.sudoku))

    def draw(self, surface: Surface) -> None:
        self.sudoku.draw(surface)
        for row in self.rows:
            row.draw(surface)
        for col in self.cols:
            col.draw(surface)

    def actions(self, event: pygame.event.Event) -> None:
        global state
        if self.end():
            state = State.END_SCREEN
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                selected_square = self.get_selected_square()
                pressed_square = self.get_collide_square(event.pos)
                if pressed_square and selected_square == pressed_square:
                    pressed_square.deselect()
                else:
                    if selected_square:
                        selected_square.deselect()
                    if pressed_square:
                        pressed_square.select()
            elif event.button == pygame.BUTTON_RIGHT:
                if (square := self.get_selected_square()):
                    square.deselect()
        elif event.type == pygame.KEYDOWN:
            if (pygame.K_1 <= event.key <= pygame.K_9) and (square := self.get_selected_square()):
                value = int(chr(event.key))
                if self.value_valid(value):
                    square.set_value(value)
                square.deselect()
            elif event.key == pygame.K_DELETE and (square := self.get_selected_square()):
                square.clear_value()
                square.deselect()
            elif event.key == pygame.K_r:
                game.init()

    def update(self) -> None:
        self.sudoku.update()

    def get_collide_square(self, pos: tuple[int]) -> Square | None:
        for square in self.squares:
            if square.rect.collidepoint(pos):
                return square
        return None

    def get_selected_square(self) -> Square | None:
        for square in self.squares:
            if square.selected:
                return square
        return None

    def value_valid(self, value: int) -> bool:
        selected_square = self.get_selected_square()
        forbidden_values = set()
        for group in selected_square.groups():
            if type(group) == Sudoku:
                continue
            for sprite in group.sprites():
                forbidden_values.add(sprite.value)
        if value in forbidden_values:
            return False
        return True

    def init(self) -> None:
        with open('data.csv', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            rows = [row for row in csv_reader]
            row = rows[randint(0, 999)]
            values = row[0]
        for value, square in zip(values, self.squares):
            square.init_value(value)

    def end(self) -> bool:
        for square in self.squares:
            if not square.value:
                return False
        return True

SQUARE_LEN = 8*SCALE
pygame.init()
pygame.display.set_caption('Sudoku')
if pygame.display.Info().current_h > 9*SQUARE_LEN:
    screen = pygame.display.set_mode((9*SQUARE_LEN, 9*SQUARE_LEN))
else:
    raise pygame.error('Window is too large')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 10*SCALE)

state = State.START_SCREEN
start_screen = StartScreen()
game = Game()
end_screen = EndScreen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif state == State.START_SCREEN:
            start_screen.actions(event)
        elif state == State.GAME:
            game.actions(event)
        elif state == State.END_SCREEN:
            end_screen.actions(event)

    if state == State.START_SCREEN:
        start_screen.update()
        start_screen.draw(screen)
    elif state == State.GAME:
        game.update()
        game.draw(screen)
    elif state == State.END_SCREEN:
        end_screen.update()
        end_screen.draw(screen)

    pygame.display.update()
    clock.tick(60)
