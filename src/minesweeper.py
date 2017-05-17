from enum import Enum
import random


class GameState(Enum):
    """
    Permet de creer une enumeration de variable.
    Une variable qui est de type GameState peut prendre trois valeur wining, losing ou running.
    """
    wining = 1
    losing = 2
    running = 3

#  ###################
#  # Cells functions #
#  ###################


def make_cell():
    """
    :return: a initialised cell with all defaults params in a dict.
    :rtype: cell
    """
    return {'bomb': False,
            'flag': False,
            'nbombs_neighborhood': 0,
            'hidden': True}


def is_bomb(cell):
    """
    :param cell: a cell of a minesweeper's grid
    :type cell: cell
    :return:
       * ``True`` if cell contains a bomb
       * ``False`` otherwise
    :rtype: bool
    """
    return cell['bomb']


def is_flaged(cell):
    """
    :param cell: a cell of a minesweeper's grid
    :type cell: cell
    :return:
       * ``True`` if cell is marked as containing a hypothetic bomb
       * ``False`` otherwise
    :rtype: bool
    """
    return cell['flag']


def is_revealed(cell):
    """
    :param cell: a cell of a minesweeper's grid
    :type cell: cell
    :return:
       * ``True`` if cell is revealed
       * ``False`` otherwise
    :rtype: bool
    """
    return not cell['hidden']


def number_of_bombs_in_neighborhood(cell):
    """
    :param cell: a cell of a minesweeper's grid
    :type cell: cell
    :return: the number of bomb in the cell's neighborhood
    :rtype: int
    """
    return cell['nbombs_neighborhood']


def reveal(cell):
    """
    :param cell: a cell of a minesweeper's grid, raise YetRevealedException if the cell is yet reveal
    :type cell: cell
    :return: None
    :rtype: NoneType
    """
    if cell['hidden']:
        cell['hidden'] = False
    else:
        raise YetRevealedException("The cell is yet discoverd")


def set_flag(cell):
    """
    :param cell: a cell of a minesweeper's grid
    :type cell: cell
    :return: None
    :rtype: NoneType
    """
    if not is_revealed(cell):
        cell['flag'] = True


def unset_flag(cell):
    """
    :param cell: a cell of a minesweeper's grid
    :type cell: cell
    :return: None
    :rtype: NoneType
    """
    if not is_revealed(cell):
        cell['flag'] = False


#  ##############
#  # Exceptions #
#  ##############


class YetRevealedException(Exception):
    pass


#  ###################
#  # Game Management #
#  ###################


def make_grid(width, height, nbombs):
    """
    return a minesweeper grid of size width*height cells
    with nbombs bombs.
    :param width: horizontal size of game
    :type width: int
    :param height:  vertical size of game
    :type height: int
    :param nbombs:  number of bombs
    :type nbombs: int
    :return: a fresh grid of  width*height cells
    :rtype: list of list of cells
    """
    if width < 3 or height < 3 or nbombs <= 0 or nbombs > width * height:
        raise ValueError()
    # Maniere courte avec les listes en comprehension
    # grid = [[make_cell() for y in range(width)] for x in range(height)]

    # Maniere plus longue et plus lente.
    grid = []
    for x in range(height):
        grid.append([])
        for y in range(width):
            grid[x].append(make_cell())

    # Maniere courte avec les listes en comprehension
    # coords = [(x, y) for y in range(width) for x in range(height)]

    # Maniere plus longue et plus lente.
    coords = []
    for x in range(height):
        for y in range(width):
            coords.append((x, y))

    # On mélange la liste des toutes les coordonnées pour tirer au hasard les n première coordonnées.
    # Cela permet d'obtenir des coordonnées aléatoire pour les bombes.
    random.shuffle(coords)

    for i in range(nbombs):
        # On place les bombes
        x, y = coords[i]
        grid[x][y]['bomb'] = True
        # On averti les voisins qu'ils ont une bombes de plus dans le voisinage.
        for xn in range(max(0, x - 1), min(height - 1, x + 1) + 1):
            for yn in range(max(0, y - 1), min(width - 1, y + 1) + 1):
                grid[xn][yn]['nbombs_neighborhood'] += 1
    return grid


def make_game(width=30, height=20, nbombs=99):
    """
    return a minesweeper game  of size width*height cells
    with nbombs bombs.
    :param width: [optional] horizontal size of game (default = 30)
    :type width: int
    :param height: [optional] vertical size of game (default = 20)
    :type height: int
    :param nbombs: [optional] number of bombs (default = 99)
    :type nbombs: int
    :return: a fresh grid of  width*height cells
    :UC: 0 < width, height and 0 <= nbombs <= width*height
    """
    return {'width': width,
            'height': height,
            'nbombs': nbombs,
            'grid': make_grid(width, height, nbombs),
            'state': GameState.running,
            'reveal_cells': width * height - nbombs}


def get_height(game):
    """
    :param game: a minesweeper game
    :type game: game
    :return: height of the grid in game
    :rtype: int
    """
    return game['height']


def get_width(game):
    """
    :param game: a minesweeper game
    :type game: game
    :return: width of the grid in game
    :rtype: int
    """
    return game['width']


def get_state(game):
    """
    :param game: a minesweeper game
    :type game: game
    :return: state of the game
    :rtype: GameState
    """
    return game['state']


def get_cell(game, x, y):
    """
    :param game: a minesweeper game
    :type game: game
    :param x: x-coordinate of a cell
    :type x: int
    :param y: y-coordinate of a cell
    :type y: int
    :return: the cell of coordinates (x,y) in the game's grid
    :type: cell
    :UC: 0 <= x < height of game and O <= y < width of game
    """
    return game['grid'][x][y]


def recursive_reveal(game, x, y):
    """
    Edit the (x,y) cell of the game grid recursively to discover hidden cell.
    :param game: a minesweeper game
    :type game: game
    :param x: x-coordinate of a cell
    :type x: int
    :param y: y-coordinate of a cell
    :type y: int
    :return: None
    :rtype: NoneType
    :UC: 0 <= x < height of game and O <= y < width of game
    """
    cell = get_cell(game, x, y)
    height = get_height(game)
    width = get_width(game)
    if not is_revealed(cell):
        reveal(cell)
        game['reveal_cells'] -= 1
    if not number_of_bombs_in_neighborhood(cell) and not is_bomb(cell):
        for xn in range(max(0, x - 1), min(height - 1, x + 1) + 1):
            for yn in range(max(0, y - 1), min(width - 1, y + 1) + 1):
                if not is_revealed(get_cell(game, xn, yn)):
                    recursive_reveal(game, xn, yn)


def reveal_cell(game, x, y):
    """
    Reveal the (x,y) cell of the game grid.
    :param game: a minesweeper game
    :type game: game
    :param x: x-coordinate of a cell
    :type x: int
    :param y: y-coordinate of a cell
    :type y: int
    :return: None
    :rtype: NoneType
    :UC: 0 <= x < height of game and O <= y < width of game
    """

    cell = get_cell(game, x, y)
    if is_flaged(cell):
        return

    if is_bomb(cell):
        game['state'] = GameState.losing
        reveal_all_bombs(game)
        return

    recursive_reveal(game, x, y)

    if not game['reveal_cells']:
        game['state'] = GameState.wining


def reveal_all_bombs(game):
    """
    :param game: reveal all bombs in the grid
    :type game: game
    :return: None
    :rtype: NoneType
    """
    for line in game['grid']:
        for cell in line:
            if is_bomb(cell):
                reveal(cell)
