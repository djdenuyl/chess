from utils.direction import Direction
from utils.length import Length


def get_vector(frm: 'Tile', to: 'Tile') -> tuple[Direction, Length]:
    """ get the vector containing the direction and length of the movement of the piece"""
    x = -1 if (dx := to.x_int - frm.x_int) < 0 else 1 if dx > 0 else 0
    y = -1 if (dy := to.y - frm.y) < 0 else 1 if dy > 0 else 0

    return Direction((x, y)), Length(dx, dy)
