from dataclasses import dataclass, field
from math import sqrt


@dataclass
class Length:
    dx: int
    dy: int
    size: float = field(init=False)

    def __set_size(self):
        self.size = sqrt(self.dx ** 2 + self.dy ** 2)

    def __post_init__(self):
        self.__set_size()
