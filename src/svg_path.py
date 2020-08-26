class Object(object):
    pass


def parse(path):
    state = Object()
    state.result = []
    state.index = 0
    state.command = None
    state.relative_coordinates = False
    state.first_point = None

    def build():
        if path[0] != 'M':
            raise ValueError('Path does not begin with an absolute move [m] but with [' + path[0] + ']')
        while state.index < len(path):
            read_command()

    def read_command():
        if path[state.index].isalpha():
            raw_command = path[state.index]
            state.index += 1
            state.command = raw_command.lower()
            state.relative_coordinates = raw_command.islower()
        elif state.command is None:
            raise ValueError('missing command character at index ' + str(state.index))
        interpret_command()

    def interpret_command():
        state.command_map[state.command]()

    def move():
        x = read_number()
        y = read_number()
        if not state.first_point:
            state.first_point = (x, y)
        state.result.append('move_' + mode() + '(' + str(x) + ',' + str(y) + ')')

    def curve():
        x1 = read_number()
        y1 = read_number()
        x2 = read_number()
        y2 = read_number()
        x = read_number()
        y = read_number()
        state.result.append('curve_' + mode() + '(' + str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2) + ',' + str(x) + ',' + str(y) + ')')

    def line():
        x = read_number()
        y = read_number()
        state.result.append('line_' + mode() + '(' + str(x) + ',' + str(y) + ')')

    def close():
        if not state.first_point:
            raise ValueError('First point not defined when closing path at index ' + str(state.index))
        state.result.append('line_' + mode() + '(' + str(state.first_point[0]) + ',' + str(state.first_point[1]) + ')')

    def read_number():
        skip_separators()
        result = ''
        while True:
            next_character = path[state.index]
            if next_character == '-' or next_character.isdigit() or next_character == '.':
                result += next_character
                state.index += 1
            else:
                break
        return float(result)

    def skip_separators():
        while True:
            next_character = path[state.index]
            if next_character == ',' or next_character == ' ':
                state.index += 1
            else:
                break

    def mode():
        return 'relative' if state.relative_coordinates else 'absolute'

    state.command_map = {
        'm': move,
        'c': curve,
        'l': line,
        'z': close
    }

    build()

    return state.result
