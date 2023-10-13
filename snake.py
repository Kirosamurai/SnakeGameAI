import pygame
from settings import *
from copy import deepcopy
from random import randrange


class Square:
    def __init__(self, pos, surface, is_apple=False):
        self.pos = pos
        self.surface = surface
        self.is_apple = is_apple
        self.is_tail = False
        self.dir = [-1, 0]  # [x, y] Direction

    def draw(self, clr=SNAKE_CLR):
        x, y = self.pos[0], self.pos[1]
        ss = SQUARE_SIZE

        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))

        if self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))

        if self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))

        if self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))

        if self.is_apple:
            pygame.draw.rect(self.surface, clr, (x * ss, y * ss, ss, ss))

    def move(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    def hitting_wall(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.is_dead = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)

        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos, self.surface))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True

        self.path = []
        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

    def draw(self):
        self.apple.draw(APPLE_CLR)
        self.head.draw(HEAD_CLR)
        for sqr in self.squares[1:]:
            if self.is_virtual_snake:
                sqr.draw(VIRTUAL_SNAKE_CLR)
            else:
                sqr.draw()

    def set_direction(self, direction):
        if direction == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Set snake direction using keyboard
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.set_direction('left')

            elif keys[pygame.K_RIGHT]:
                self.set_direction('right')

            elif keys[pygame.K_UP]:
                self.set_direction('up')

            elif keys[pygame.K_DOWN]:
                self.set_direction('down')

    def move(self):
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.move([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.move(sqr.dir)
        self.moves_without_eating += 1

    def add_square(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]  # Tail before adding new square

        direction = tail.dir
        if direction == [1, 0]:
            self.squares.append(Square([tail.pos[0] - 1, tail.pos[1]], self.surface))
        if direction == [-1, 0]:
            self.squares.append(Square([tail.pos[0] + 1, tail.pos[1]], self.surface))
        if direction == [0, 1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] - 1], self.surface))
        if direction == [0, -1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] + 1], self.surface))

        self.squares[-1].dir = direction
        self.squares[-1].is_tail = True  # Tail after adding new square

    def reset(self):
        self.__init__(self.surface)

    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    def generate_apple(self):
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)
        if not self.is_position_free(self.apple.pos):
            self.generate_apple()

    def eating_apple(self):
        if self.head.pos == self.apple.pos and not self.is_virtual_snake and not self.won_game:
            self.generate_apple()
            self.moves_without_eating = 0
            self.score += 1
            return True

    def go_to(self, position):  # Set head direction to target position
        if self.head.pos[0] - 1 == position[0]:
            self.set_direction('left')
        if self.head.pos[0] + 1 == position[0]:
            self.set_direction('right')
        if self.head.pos[1] - 1 == position[1]:
            self.set_direction('up')
        if self.head.pos[1] + 1 == position[1]:
            self.set_direction('down')

    def is_position_free(self, position):
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.squares:
            if sqr.pos == position:
                return False
        return True
    
    def update(self):
        self.handle_events()

        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])

        self.draw()
        self.move()

        if self.score == ROWS * ROWS - INITIAL_SNAKE_LENGTH:  # If snake wins the game
            self.won_game = True

            print("Snake won the game after {} moves"
                  .format(self.total_moves))

            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            return 1

        self.total_moves += 1

        if self.hitting_self() or self.head.hitting_wall():
            print("Snake is dead, trying again..")
            self.is_dead = True
            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            self.reset()

        if self.moves_without_eating == MAX_MOVES_WITHOUT_EATING:
            self.is_dead = True
            print("Snake got stuck, trying again..")
            self.reset()

        if self.eating_apple():
            self.add_square()



    # Breadth First Search Algorithm
    def bfs(self, s, e):  # Find shortest path between (start_position, end_position)
        q = [s]  # Queue
        visited = {tuple(pos): False for pos in GRID}

        visited[s] = True

        # Prev is used to find the parent node of each node to create a feasible path
        prev = {tuple(pos): None for pos in GRID}

        while q:  # While queue is not empty
            node = q.pop(0)
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = e  # Starting from end node, we will find the parent node of each node

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == s:
                path.append(e)
                return path
            path.insert(0, p_node)

        return []  # Path not available

    def create_virtual_snake(self):  # Creates a copy of snake (same size, same position, etc..)
        v_snake = Snake(self.surface)
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_square()

        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = deepcopy(self.squares[i].pos)
            sqr.dir = deepcopy(self.squares[i].dir)

        v_snake.dir = deepcopy(self.dir)
        v_snake.turns = deepcopy(self.turns)
        v_snake.apple.pos = deepcopy(self.apple.pos)
        v_snake.apple.is_apple = True
        v_snake.is_virtual_snake = True

        return v_snake

    def set_path(self):
        v_snake = self.create_virtual_snake()
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))

        return path_1
