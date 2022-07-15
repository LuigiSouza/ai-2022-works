#!/usr/bin/env python

closed_nodes: set[tuple[int, int, bool]] = set()


class State:
    """
    Classe que representa um node do problema. O node corresponde a um estado do problema o
    qual possúi as informações de missionários e canibais no lado esquerdo do rio, a posição
    atual do barco, a lista de nodes filhos (estados possíveis a partir do atual) e o nó pai.
    """

    boat_to_string = ["MargemEsq", "MargemDir"]
    """
    Variáveis de instância. O barco na posição 0 corresponde ao lado esquerdo do rio e o 1 ao o lado direito.
    """

    legal_movements: list[tuple[int, int]] = []
    """
    Lista com todos os movimentos válidos do barco.
    """

    def __init__(
        self,
        missionaries_l: int,
        canibals_l: int,
        game_size: int = 3,
        boat_size: int = 2,
        boat_pos: bool = 1,
    ):
        self.missionaries_l = missionaries_l
        self.canibals_l = canibals_l
        self.game_size = game_size
        self.boat_size = boat_size
        self.boat_pos = boat_pos
        self.father: State = None
        self.nodes: list[State] = []
        self.__gerenerate_legal_movements()

    def __gerenerate_legal_movements(self):
        """
        Gera a lista de movimentos válidos do barco, onde cada movimento é uma tupla com o número
        de missionários e canibais que serão movidos. É necessário no mínimo uma pessoa conduzindo o barco
        para se realizar o movimento, e pode-se gerar livres combinações de missionários e canibais.
        """
        movements = set()
        for m in range(self.boat_size):
            for c in range(self.boat_size - m):
                movements.add((m + 1, c))
        for c in range(self.boat_size):
            for m in range(self.boat_size - c):
                movements.add((m, c + 1))
        self.legal_movements = list(movements)

    def __is_valid(self):
        """
        Verifica se o estado atual é válido. Os lados não podem ter valores negativos, nem
        o número de canibais de um lado deve ser superior ao de missionários neste caso haja
        mais que zero missionários.
        """
        if (
            self.missionaries_l < 0
            or self.canibals_l < 0
            or self.missionaries_l > self.game_size
            or self.canibals_l > self.game_size
        ):
            return False
        if (
            self.missionaries_l != 0
            and self.canibals_l != self.missionaries_l != self.game_size
        ):
            return False
        return True

    def is_final(self):
        """
        Verifica se o lado esquerdo do rio está cheio de missionários e canibais.
        """
        missionaries_r = self.game_size - self.missionaries_l
        canibals_r = self.game_size - self.canibals_l

        right_empty = missionaries_r == canibals_r == 0
        left_full = self.missionaries_l == self.canibals_l == self.game_size

        return right_empty and left_full

    def step(self):
        """
        Gera todos os possíveis estados filhos do estado atual, se estes forem válidos e não
        estiverem fechados (já terem sido acessados anteriormente).
        """

        # Caso o barco esteja no lado esquerdo, será diminuido o número de canibais ou missionários
        # para atravessar para o lado direito. Caso contrário, será adicionado.
        side_to_move = 2 * self.boat_pos - 1
        for movement in self.legal_movements:
            # Gera todos os possíveis movimentos de um estado
            missionaries_l = self.missionaries_l + side_to_move * movement[0]
            canibals_l = self.canibals_l + side_to_move * movement[1]
            boat_pos = not self.boat_pos
            # Verifica se o novo node já foi visitado
            node_key = (missionaries_l, canibals_l, boat_pos)
            if node_key in closed_nodes:
                continue

            node = State(
                missionaries_l,
                canibals_l,
                self.game_size,
                self.boat_size,
                boat_pos,
            )

            if node.__is_valid():
                closed_nodes.add(node_key)
                node.father = self
                self.nodes.append(node)

    def __str__(self):
        return f"Estado<{self.missionaries_l},{self.canibals_l},{self.boat_to_string[self.boat_pos]}>"


def main():
    game_size = 3
    boat_size = 2
    queue = [State(0, 0, game_size, boat_size, 1)]
    solution: list[State] = []

    # Computar o resultado
    for state in queue:
        if state.is_final():
            # Se a solução foi encontrada, é feito o backtracking para se adicionar à solução.
            solution.append(state)
            while state.father:
                solution.insert(0, state.father)
                state = state.father
            break
        # Adiciona os filhos gerados a lista de estados a ser percorrida.
        state.step()
        queue.extend(state.nodes)

    for state in solution:
        print(state)


if __name__ == "__main__":
    main()
