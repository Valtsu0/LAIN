import sys


class Lain:
    def __init__(self, program):
        self.variables = {}
        self.index = 0
        self.program = program

    def run(self):
        while True:
            if len(self.program) <= self.index:
                break
            raw_line = self.program[self.index].replace('\n', '')
            if raw_line == '' or ';' not in raw_line:
                print(raw_line)
                self.index += 1
                continue
            raw_line = raw_line.replace(';', ' ; ')
            line_temp = raw_line.split(' ')

            in_string = False
            string = ''
            line = []
            for i in line_temp:
                if in_string:
                    if i[-1] == '"':
                        string += i
                        in_string = False
                        line.append(string)
                    else:
                        string += i + ' '
                elif i == '':
                    pass
                elif i[0] == '"':
                    if i[-1] == '"' and len(i) > 1:
                        line.append(i)
                        continue
                    in_string = True
                    string = i + ' '
                else:
                    line.append(i)
            if line[0][0] == ':':
                pass
            elif line[0] == 'goto':
                if not line[1].isnumeric():
                    if line[1][0] != '"':
                        line[1] = self.variables[line[1]]
                    if line[1][0] == '"':
                        destination = -1
                        for i in range(len(self.program)):
                            j = self.program[i].replace(';', ' ; ')
                            j = j.split(' ')
                            if j[0][0] == ':':
                                if j[0][1:] == line[1][1:-1]:
                                    destination = i
                                    break
                        if destination == -1:
                            self.index += 1
                            continue
                        else:
                            self.index = destination
                            continue
                self.index = int(line[1])
                continue

            elif line[0] == 'line':
                if not line[1].isnumeric():
                    line[1] = self.variables[line[1]]
                if not line[2].isnumeric():
                    if line[2][0] == '"':
                        line[2] = line[2][1:-1]
                    else:
                        line[2] = self.variables[line[2]]

                self.program[int(line[1])] = str(line[2])

            elif line[0] != ';':
                value = ''
                if line[1] == ';':
                    value = input()
                elif line[1] == '=':
                    numeric = True
                    if not line[2].isnumeric():
                        if line[2][0] == '"':
                            line[2] = line[2][1:-1]
                        else:
                            line[2] = self.variables[line[2]]
                        if not str(line[2]).isnumeric():
                            numeric = False

                    if line[3] == ';':
                        value = line[2]
                    else:
                        if not line[4].isnumeric():
                            if line[4][0] == '"':
                                line[4] = line[4][1:-1]
                            else:
                                line[4] = self.variables[line[4]]
                        if not str(line[4]).isnumeric():
                            numeric = False

                        if line[3] == '+':
                            if numeric:
                                value = int(line[2]) + int(line[4])
                            else:
                                value = str(line[2]) + str(line[4])
                        elif line[3] == '-':
                            value = int(line[2]) - int(line[4])
                        elif line[3] == 'min':
                            value = min(int(line[2]), int(line[4]))
                        elif line[3] == 'max':
                            value = max(int(line[2]), int(line[4]))
                self.variables[line[0]] = value

            self.index += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide a filename')
        sys.exit()
    try:
        with open(sys.argv[1], 'r') as f:
            program = [line for line in f]
    except IOError:
        print(f'File not found or unreadable: {sys.argv[1]}')
        sys.exit(1)
    lain = Lain(program)
    lain.run()
