import minesweeper as ms
import sys
import config


def launch(width, height, bombs):
    """
    launch the game
    :param width: width of the game
    :type width: int
    :param height: height of the game
    :type height: int
    :param bombs: number of bombs
    :type bombs: int
    """
    game = ms.make_game(width, height, bombs)
    state = ms.get_state(game)
    while state == ms.GameState.running:
        try:
            display_game(game)
            play(game)
            state = ms.get_state(game)
        except KeyboardInterrupt:
            sys.exit()
    display_game(game)
    if state == ms.GameState.losing:
        print("You lose!")
    elif state == ms.GameState.wining:
        print("You win!")
    else:
        print("an unexpected error has occured")


def play(game):
    """
    require action to the player and execute it
    :param game: game
    :type game: a minesweeper game
    :return: None
    :rtype: NoneType
    :UC: none
    """
    action = keyboard_input(game)
    x = action[0]
    y = action[1]
    a = action[2]
    if a == 'R':
        ms.reveal_cell(game, x, y)
    elif a == 'S':
        cell = ms.get_cell(game, x, y)
        ms.set_flag(cell)
    elif a == 'U':
        cell = ms.get_cell(game, x, y)
        ms.unset_flag(cell)


def keyboard_input(game):
    """
    :param game: game
    :type game: a minesweeper game
    :return: the player input action
    :rtype: tuple of the action (posX, posY, action)
    :UC: none
    """
    try:
        data_in = input("Your play x,y,C with x=line, y=row, C=(R)eval,(S)et flag,(U)nset flag): ")
        ldata = data_in.split(',')
        x = int(ldata[0])
        y = int(ldata[1])
        c = ldata[2].upper()
        if x < 0 or x >= ms.get_height(game) \
                or y < 0 or y >= ms.get_width(game)\
                or c not in ['R', 'S', 'U']:
            raise ValueError
        return (x, y, c)
    except IndexError:
        print ('There must be two numbers and one letter separated by a comma (,)')
        keyboard_input(game)
    except TypeError:
        print ('There must be two numbers and one letter separated by a comma (,)')
        keyboard_input(game)
    except ValueError:
        print ("x and y must be integers and c must be R or S or U")
        keyboard_input(game)


def display_game(game):
    """
    display the game in stdout
    :param game: game
    :type game: a minesweeper game
    :return: None
    :rType: NoneType
    :UC: none
    """
    height = ms.get_height(game)
    width = ms.get_width(game)
    display_line = "+---" * width
    display_line += "+"
    to_print = " "
    for i in range(width - 1):
        to_print += "   " + str(i)
    to_print += "   " + str(width - 1) + '\n'
    for h in range(height):
        to_print += "  " + display_line + '\n'
        to_print += str(h)
        for l in range(width):
            character = " "
            cell = ms.get_cell(game, h, l)
            if ms.is_revealed(cell):
                if ms.is_bomb(cell):
                    character = "B"
                else:
                    character = ms.number_of_bombs_in_neighborhood(cell)
            elif ms.is_flaged(cell):
                    character = "?"
            to_print += " | " + str(character)
        to_print += " |\n"
    to_print += "  " + display_line + "\n"
    print(to_print)


if __name__ == '__main__':
    try:
        config_file = sys.argv[1]
    except IndexError:
        launch(10, 10, 10)
    else:
        h, w, b = config.rescue_basic_config(config_file)
        launch(w, h, b)
