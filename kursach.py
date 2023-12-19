from random import uniform, randint
from math import pi, sqrt, e
import pyxel


def calc_delta(
    y: float,
    wind_fac: float = -1,
    mpx: float = -0.2,
    omega: float = 0.5,
    offset: float = 1.5,
) -> int:
    coeff = uniform(-1, 1)
    mu = wind_fac * y + offset
    temp_val = (1 / (omega * sqrt(2 * pi))) * e ** (mpx * ((coeff - mu) / omega) ** 2)
    max_val = (1 / (omega * sqrt(2 * pi))) * e ** (mpx * ((mu - mu) / omega) ** 2)
    temp_val = 2 * temp_val / max_val - 1
    return round(temp_val)


class Automaton:
    wind = -5

    def __init__(self, start_x: list[int], field_x: int = 256, field_y: int = 256):
        self.field = [[0 for i in range(field_x)].copy() for i in range(field_y)]
        self.start_x = start_x
        self.field_x = field_x
        self.field_y = field_y

    def iterate(self) -> None:
        new_field = [
            [0 for i in range(self.field_x)].copy() for i in range(self.field_y)
        ]
        for i in self.start_x:
            new_field[0][i] = 1
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x] == 1:
                    flag = 10
                    while flag > 0:
                        x_temp = x + calc_delta(
                            y / self.field_y,
                            wind_fac=self.wind,
                            omega=1,
                            mpx=-0.2,
                            offset=-2.5,
                        )
                        x_delta = min(
                            max(x_temp, 0),
                            self.field_x - 1,
                        )
                        y_temp = y + calc_delta(
                            y / self.field_y,
                            wind_fac=1.2,
                            omega=0.75,
                            mpx=-0.2,
                            offset=-1,
                        )
                        y_delta = min(
                            max(y_temp, 0),
                            self.field_y - 1,
                        )
                        if new_field[y_delta][x_delta] == 0:
                            flag = 0
                        else:
                            flag -= 1
                    new_field[y_delta][x_delta] = 1
        self.field = new_field


class App:
    size = 400

    def __init__(self):
        pyxel.init(self.size + 4, self.size + 4)
        self.automaton = Automaton(
            start_x=[i for i in range(int(self.size * 0.9), int(self.size * 0.92))],
            field_x=self.size,
            field_y=self.size,
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        self.automaton.iterate()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, self.size + 4, self.size + 4, 1)
        pyxel.rect(2, 2, self.size, self.size, 3)
        field = self.automaton.field
        for y in range(self.automaton.field_y):
            for x in range(self.automaton.field_x):
                if field[y][x] == 1:
                    pyxel.rect(x + 2, y + 2, 1, 1, 10)


def main():
    App()


if __name__ == "__main__":
    main()
