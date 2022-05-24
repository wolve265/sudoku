import pygame

from game import game, GameState

from sudoku_test import StartScreen, Sudoku, EndScreen


class App:

    def __init__(self) -> None:
        self.start_screen = StartScreen()
        self.sudoku = Sudoku()
        self.end_screen = EndScreen()

    def run(self) -> None:
        while game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.quit()
                elif game.state == GameState.START_SCREEN:
                    self.start_screen.actions(event)
                elif game.state == GameState.NEW_GAME:
                    self.sudoku.init()
                    game.solve()
                elif game.state == GameState.SOLVING:
                    self.sudoku.actions(event)
                elif game.state == GameState.END_SCREEN:
                    self.end_screen.actions(event)

            if game.state == GameState.START_SCREEN:
                self.start_screen.update()
                self.start_screen.draw(game.screen)
            elif game.state == GameState.SOLVING:
                self.sudoku.update()
                self.sudoku.draw(game.screen)
            elif game.state == GameState.END_SCREEN:
                self.end_screen.update()
                self.end_screen.draw(game.screen)

            pygame.display.update()
            game.clock.tick(60)

        game.post_quit()


if __name__ == '__main__':
    app = App()
    app.run()
