import copy


class MItem:
    # TODO Умное создание

    def __init__(self, pars):
        match pars:
            case (int(c), list(v)):
                self.counts = c
                self.vars = v
            case (int(c), str(v)):
                self.counts = c
                self.vars = [v]
            case int(c):
                self.counts = c
                self.vars = []
            case list(v):
                self.counts = 1
                self.vars = v
            case str(v):
                self.counts = 1
                self.vars = [v]
            case _:
                raise Exception("Wrong data")

    def __add__(self, other):
        if sorted(self.vars) == sorted(other.vars):
            return MItem((self.counts + other.counts, self.vars))
        else:
            return MIsum([self, other])

    def __mul__(self, other):
        if not isinstance(self.vars + other.vars, list):
            raise Exception("WESDASD")
        return MItem((self.counts*other.counts, self.vars + other.vars))

    def __str__(self):
        if self.counts == 0:
            return str(0)
        elif self.counts == 1 and self.vars:

            return ''.join(self.vars)
        elif self.counts == -1 and self.vars:
            return '- ' + ''.join(self.vars)
        else:
            return f"{self.counts} {''.join(self.vars)}"


class MIsum:
    def __init__(self, params):
        self.items: list = []
        # TODO переделать
        match params:
            case list(i):
                self.items = i
            case _:
                if isinstance(params, MItem):
                    self.items = [params]
                else:
                    raise Exception("Wrong MIsum format")

    def __str__(self):
        return ' + '.join(map(str, self))

    def __getitem__(self, index):
        return self.items[index]

    def append(self, value: MItem):
        self.items.append(value)

    def pop(self, index):
        self.items.pop(index)

    def remove(self, value):
        self.items.remove(value)

    def __setitem__(self, key, value: MItem):
        self.items[key] = value

    def __iter__(self):
        return iter(self.items)

    def __add__(self, second):
        if isinstance(second, MItem):
            second = MIsum(second)

        res = self.items.copy()
        for i_s, s in enumerate(second, 0):
            if s.counts == 0:
                continue
            for i_r, r in enumerate(res, 0):
                if isinstance(s+r, MItem):
                    res[i_r] = s+r
                    break
            else:
                res.append(s)
        for i in res:
            if i.counts == 0:
                res.remove(i)
        return MIsum(res) if len(res) != 0 else MIsum(MItem(0))


class Matrix:
    def __init__(self, table: list[list]):
        m_table = []
        for row in table:
            l = []
            for i in row:
                if isinstance(i, MIsum):
                    l.append(i)
                elif isinstance(i, MItem):
                    l.append(i)
                else:
                    l.append(MItem(i))
            m_table.append(l)
        self.matrix = m_table
        self.shape = (len(m_table), len(m_table[0]))

    def __str__(self):
        return '\n'.join([' | '.join(map(str, x)) for x in self.matrix])

    def __getitem__(self, index):
        return self.matrix[index]

    def __mul__(matrix_1, matrix_2):
        if matrix_1.shape[1] != matrix_2.shape[0]:
            raise Exception("Unacceptable matrices sizes")
        res_matrix = []
        for row in range(matrix_1.shape[0]):
            result = []
            for col in range(matrix_2.shape[1]):
                item = MIsum(MItem(0))
                for r in range(matrix_1.shape[1]):
                    item += matrix_1[row][r] * matrix_2[r][col]
                result.append(item)
            res_matrix.append(result)
        return Matrix(res_matrix)

    def __add__(matrix_1, matrix_2):
        if matrix_1.shape != matrix_2.shape:
            raise Exception("Unacceptable matrices sizes")
        s_matrix = []
        for row in range(matrix_1.shape[0]):
            s_matrix.append([matrix_1[row][x] + matrix_2[row][x] for x in range(matrix_1.shape[1])])
        return Matrix(s_matrix)


def I(shape=1):
    m = []
    for i in range(shape):
        m.append([0]*i + [1] + [0]*(shape-i-1))
    return Matrix(m)


def sum_many(items: list[MItem]):
    res = ''
    dct = dict()
    for item in items:
        key = tuple(sorted(item.vars))
        if key in dct.keys():
            dct[key] += item.counts
        else:
            dct[key] = item.counts

    for k, v in dct.items():
        if v == 0:
            continue
        if v > 0:
            res += f"+ {v}{''.join(k)}"
        elif v < 0:
            res += f"- {abs(v)}{''.join(k)}"
    if res[:2] == '+ ':
        res = res[2:]
    return res if res != '' else '0'


def sm(items):
    return str(sum(map(lambda x: x.counts, items)))