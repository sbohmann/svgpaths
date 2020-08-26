class Object(object):
    pass

def parse(path):
    state = Object()
    state.result = []
    state.index = 0
    state.command = None

    def build():
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
        state.result.append('move_absolute(' + str(x) + ',' + str(y) + ')')

    def curve():
        x1 = read_number()
        y1 = read_number()
        x2 = read_number()
        y2 = read_number()
        x = read_number()
        y = read_number()
        state.result.append('move_absolute(' + str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2) + ',' + str(x) + ',' + str(y) + ')')

    def read_number():
        skip_comma()
        result = ''
        while True:
            next_character = path[state.index]
            if next_character == '-' or next_character.isdigit() or next_character == '.':
                result += next_character
                state.index += 1
            else:
                break
        return float(result)

    def skip_comma():
        if path[state.index] == ',':
            state.index += 1

    state.command_map = {
        'm': move,
        'c': curve
    }

    build()