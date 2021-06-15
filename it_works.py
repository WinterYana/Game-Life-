import pygame
import copy


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[[(column, line)] for column in range(width)] for line in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 27

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        for line in self.board:
            for square in line:
                if square[1][0] <= mouse_pos[0] < square[1][0] + self.cell_size and \
                        square[1][1] <= mouse_pos[1] < square[1][1] + self.cell_size:
                    return square[0]
        return None

    def on_click(self, cell_coords):
        global development
        if cell_coords is not None and not development:
            self.board[cell_coords[1]][cell_coords[0]][2] = 0 if self.board[cell_coords[1]][cell_coords[0]][2] == 1 else 1

    def render(self, screen):
        global development
        coords = [self.left, self.top]
        screen.fill((0, 0, 0))
        for line in range(self.height):
            coords[0] = self.left
            for column in range(self.width):
                if len(self.board[line][column]) == 1:
                    self.board[line][column].append(coords.copy())
                    self.board[line][column].append(0)
                pygame.draw.rect(screen, (255, 255, 255), (coords[0], coords[1], self.cell_size, self.cell_size), 1)
                coords[0] += self.cell_size
            coords[1] += self.cell_size
        if development:
            self.board = copy.deepcopy(Life(self.board, self.width, self.height).new_generation(screen))
            #print(self.board)
        self.draw(screen)

    def draw(self, screen):
        for line in range(self.height):
            for column in range(self.width):
                if self.board[line][column][2] == 1:
                    pygame.draw.rect(screen, (25, 255, 25), (self.board[line][column][1][0] + 2,
                                                             self.board[line][column][1][1] + 2,
                                                             self.cell_size - 2, self.cell_size - 2))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (self.board[line][column][1][0] + 2,
                                                             self.board[line][column][1][1] + 2,
                                                             self.cell_size - 2, self.cell_size - 2))


class Life(Board):
    def __init__(self, board, width, height):
        super().__init__(width, height)
        self.width = width
        self.height = height
        self.board = board

    def new_generation(self, screen):
        new_field = copy.deepcopy(self.board)
        for line in range(self.height):
            for column in range(self.width):
                neighbors = self.number_of_neighbors(line, column)
                if self.board[line][column][2] == 0 and neighbors == 3:
                    new_field[line][column][2] = 1
                elif self.board[line][column][2] == 1 and (neighbors == 2 or neighbors == 3):
                    new_field[line][column][2] = 1
                else:
                    new_field[line][column][2] = 0
        self.board = copy.deepcopy(new_field)
        return new_field

    def number_of_neighbors(self, line, column):
        num_of_neighbors = 0
        for neig_line in range(line - 1, line + 2):
            if 0 > neig_line:
                neig_line = self.height - 1
            elif neig_line == self.height:
                neig_line = 0
            for neig_column in range(column - 1, column + 2):
                if 0 > neig_column:
                    neig_column = self.width - 1
                elif neig_column == self.width:
                    neig_column = 0
                if not (neig_line == line and neig_column == column) and self.board[neig_line][neig_column][2] == 1:
                    num_of_neighbors += 1
        return num_of_neighbors


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pygame')
    board_size = 800
    size = width, height = board_size, board_size
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    board = Board(28, 28)
    running = True
    development = False
    fps = 20

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not development:
                board.get_click(event.pos)
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                development = not development
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and development:
                if fps < 105:
                    fps += 4
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and development:
                if fps > 5:
                    fps -= 4
        clock.tick(fps)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
