import pygame

from enum import Enum, auto


class GameState(Enum):
    START_SCREEN = auto()
    NEW_GAME = auto()
    SOLVING = auto()
    END_SCREEN = auto()


class Game:

    name = 'Sudoku'
    scale = 10
    square_len = 80

    def __init__(self) -> None:
        self.running = True
        pygame.init()
        pygame.display.set_caption(self.name)
        if pygame.display.Info().current_h > 9*self.square_len:
            self.screen = pygame.display.set_mode((9*self.square_len, 9*self.square_len))
        else:
            raise pygame.error('Window is too large')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 10*self.scale)
        self.state = GameState.START_SCREEN

    def start(self) -> None:
        self.state = GameState.START_SCREEN

    def new(self) -> None:
        self.state = GameState.NEW_GAME

    def solve(self) -> None:
        self.state = GameState.SOLVING

    def end(self) -> None:
        self.state = GameState.END_SCREEN

    def quit(self) -> None:
        self.running = False

    @staticmethod
    def post_quit() -> None:
        pygame.quit()


game = Game()
