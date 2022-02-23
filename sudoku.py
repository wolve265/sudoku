import pygame
import sys

from itertools import product


class Square:
    def __init__(self, id, pos, value=None) -> None:
        self.id: int = id
        self.pos: tuple[int] = pos
        self.value: int = value
        self.surf: pygame.Surface = font.render(f'', True, 'Black')
        self.rect: pygame.Rect = pygame.Rect(self.pos, (80,80))
        self.selected = False
        self.set_value(value)

    def __repr__(self) -> str:
        return f'{self.id}. {self.__class__.__name__}[{int(self.id/9)}, {int(self.id%9)}] = {self.value} at pos {self.rect.center}'

    def select(self) -> None:
        self.selected = True

    def deselect(self) -> None:
        self.selected = False

    def set_value(self, value: int) -> None:
        # if value is None: # for debug purposes
        if value is None or not (1 <= value <= 9):
            return
        self.value = value
        self.surf = font.render(f'{self.value}', True, 'Black')

    def clear_value(self) -> None:
        self.value = None
        self.surf = font.render(f'', True, 'Black')


class Mesh:
    def __init__(self) -> None:
        self.square_list: list[Square] = []
        for i, (y, x) in enumerate(product(range(9), range(9))):
            pos = (80*x, 80*y)
            # self.square_list.append(Square(i, pos, i)) # for debug purposes
            self.square_list.append(Square(i, pos))

    def blit(self) -> None:
        for square in self.square_list:
            if square.selected:
                pygame.draw.rect(screen, 'Gray', square.rect)
            else:
                pygame.draw.rect(screen, 'White', square.rect)
            pygame.draw.rect(screen, 'Black', square.rect, 2)
            pygame.draw.rect(screen, 'Black', screen.get_rect(), 5)
            screen.blit(square.surf, square.rect)

    def get_collide_square(self, pos: tuple[int]) -> Square | None:
        for square in self.square_list:
            if square.rect.collidepoint(pos):
                return square
        return None

    def get_selected_square(self) -> Square | None:
        for square in self.square_list:
            if square.selected:
                return square
        return None

    def get_forbidden_values(self) -> list:
        forbidden_values = []
        sel_square = self.get_selected_square()
        # vertical
        for id in range(sel_square.id % 9, 81, 9):
            if (value:=self.square_list[id].value) is not None:
                forbidden_values.append(value)
        # horizontal
        beg_id = sel_square.id - sel_square.id % 9
        for id in range(beg_id, beg_id+9):
            if (value:=self.square_list[id].value) is not None:
                forbidden_values.append(value)
        # big square
        beg_id = sel_square.id - sel_square.id % 3
        beg_id -= (sel_square.id - sel_square.id % 9) % 27
        for id in range(beg_id, beg_id+3):
            if (value:=self.square_list[id].value) is not None:
                forbidden_values.append(value)
        beg_id += 9
        for id in range(beg_id, beg_id+3):
            if (value:=self.square_list[id].value) is not None:
                forbidden_values.append(value)
        beg_id += 9
        for id in range(beg_id, beg_id+3):
            if (value:=self.square_list[id].value) is not None:
                forbidden_values.append(value)
        return forbidden_values

    def value_valid(self, value: int) -> bool:
        if value in self.get_forbidden_values():
            return False
        return True



pygame.init()
pygame.display.set_caption('Sudoku')
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)

mesh = Mesh()
# print(mesh.square_list)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if (square := mesh.get_selected_square()):
                square.deselect()
            if (square := mesh.get_collide_square(event.pos)):
                square.select()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            if (square := mesh.get_selected_square()):
                square.clear_value()
                square.deselect()
        elif event.type == pygame.KEYDOWN:
            if (pygame.K_1 <= event.key <= pygame.K_9) and (square := mesh.get_selected_square()):
                value = int(chr(event.key))
                if mesh.value_valid(value):
                    square.set_value(value)
                square.deselect()
            elif event.key == pygame.K_DELETE and (square := mesh.get_selected_square()):
                square.clear_value()
                square.deselect()

    mesh.blit()

    pygame.display.update()
    clock.tick(60)
