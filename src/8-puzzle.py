closed_nodes = set()

BLANK = "b"


class State:
    """
    Classe que representa um estado do tabuleiro. O estado possúi a posição de todos os
    números em uma matriz 3x3, como possúi o índice (x,y) do espaço vazio para realizar seu movimento.
    """

    def __init__(self, board: list[list]):
        self.father: State = None
        self.nodes: list[State] = []
        self.board: list[list[int]] = board
        # Cálculo da Heurística do tabuleiro atual
        self.weight: int = self.distance() + self.heuristic()
        self.blank_index = [
            (index, row.index(BLANK))
            for index, row in enumerate(self.board)
            if BLANK in row
        ][0]

    def __str__(self):
        return "\n".join(
            [" ".join([str(x if x != BLANK else " ") for x in x]) for x in self.board]
        )

    def __gt__(self, other):
        return self.weight > other.weight

    def distance(self):
        """
        Gera a heurística para o Algoritmo Guloso, onde é calculada a distância entre cada
        número no tabuleiro para seu local desejado.
        """
        goal_states = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

        total: int = 0
        for r_index, row in enumerate(self.board):
            for c_index, value in enumerate(row):
                if value == BLANK:
                    continue
                vertical = abs(c_index - goal_states[value - 1][1])
                horizontal = abs(r_index - goal_states[value - 1][0])
                total += horizontal + vertical
        return total

    def heuristic(self):
        """
        Gera a heurística para o Algoritmo A*, onde é calculado a quantia de números que não
        estão no local desejada.
        """
        goal_states: list[tuple[int, int]] = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2),
            (2, 1),
            (2, 0),
            (1, 0),
        ]
        total: int = 0
        for r_index, row in enumerate(self.board):
            for c_index, value in enumerate(row):
                if value == BLANK:
                    continue
                goal: tuple = goal_states[value - 1]
                if goal[0] != r_index or goal[1] != c_index:
                    total += 1
        return total

    def is_final(self):
        """
        Verifica se o tabuleiro faz a seguinte formação:
        1 2 3
        8   4
        5 6 7
        """
        return self.board == [[1, 2, 3], [8, BLANK, 4], [7, 6, 5]]

    def valid_moves(self):
        """
        Retorna a lista de movimentos válidos para o espaço vazio, considerando que é possível
        o movimento para cima, para baixo, para a esquerda e para a direita, contanto que não
        esteja fora do tabuleiro.
        """
        valid_moves: list[tuple] = []
        if self.blank_index[0] > 0:
            valid_moves.append((self.blank_index[0] - 1, self.blank_index[1]))
        if self.blank_index[0] < 2:
            valid_moves.append((self.blank_index[0] + 1, self.blank_index[1]))
        if self.blank_index[1] > 0:
            valid_moves.append((self.blank_index[0], self.blank_index[1] - 1))
        if self.blank_index[1] < 2:
            valid_moves.append((self.blank_index[0], self.blank_index[1] + 1))
        return valid_moves

    def copy_board(self):
        """
        Retorna um copia dos valores do tabuleiro atual.
        """
        return [[y for y in x] for x in self.board]

    def step(self):
        """
        Gera todos os estados possíveis a partir do estado atual, considerando os estados
        criados na função `valid_moves`.
        """
        for move in self.valid_moves():
            new_board = self.copy_board()
            new_board[self.blank_index[0]][self.blank_index[1]] = new_board[move[0]][
                move[1]
            ]
            new_board[move[0]][move[1]] = BLANK

            new_state = State(new_board)
            new_state.father = self
            self.nodes.append(new_state)
        self.nodes.sort()


def greed_algorithm(state: State):
    """
    Função recursiva que bussca a solução do problema. Busca o estado final
    a partir dos caminhos de menor custo e retorna a referência para o estado final.
    """
    if str(state.board) in closed_nodes:
        return None
    closed_nodes.add(str(state.board))

    if state.is_final():
        return state
    state.step()
    for node in state.nodes:
        result = greed_algorithm(node)
        if result:
            return result
    return None


def main():
    board = [[1, 2, 3], [BLANK, 6, 4], [8, 7, 5]]
    initial = State(board)
    final: State = greed_algorithm(initial)
    solution: list[State] = []

    # Converte a stack da solução em uma fila para impressão do resultado
    while final:
        solution.insert(0, final)
        final = final.father
    for state in solution:
        print("--Estado:")
        print(state)
    print("Resolvido em:", len(solution))


if __name__ == "__main__":
    main()
