from random import uniform
from math import pi, sqrt, e
import pyxel


def calc_delta(y: float, omega: float = 0.4) -> int:
    coeff = uniform(-1, 1)
    mu = -0.03 * y + 1
    temp_val = (1 / (omega * sqrt(2 * pi))) * e ** (-0.5 * ((coeff - mu) / omega) ** 2)
    temp_val = 2 * temp_val - 1
    return round(temp_val)


class Automaton:
    def __init__(self, start_x: int, field_x: int = 20, field_y: int = 20):
        self.field = [[0 for i in range(field_x)].copy() for i in range(field_y)]
        self.start_x = start_x
        self.field_x = field_x
        self.field_y = field_y

    def iterate(self) -> None:
        new_field = [
            [0 for i in range(self.field_x)].copy() for i in range(self.field_y)
        ]
        new_field[0][self.start_x] = 1
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x] == 1:
                    x_delta = min(max(x + calc_delta(y), 0), self.field_x - 1)
                    y_delta = min(self.field_y - 1, y + 1)
                    new_field[y_delta][x_delta] = 1
        self.field = new_field


class App:
    def __init__(self):
        pyxel.init(26, 26)
        self.automaton = Automaton(15)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.automaton.iterate()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, 26, 26, 1)
        pyxel.rect(3, 3, 20, 20, 3)
        field = self.automaton.field
        for y in range(len(field)):
            for x in range(len(field[y])):
                if field[y][x] == 1:
                    pyxel.rect(x + 3, y + 3, 1, 1, 6)


def main():
    App()


if __name__ == "__main__":
    main()
