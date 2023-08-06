class Border:

    def __init__(self, l: bool = False, r: bool = False, t: bool = False, b: bool = False):
        """
        Элемент границы.

        :param l: должна ли граница соединяться слева
        :param r: должна ли граница соединяться справа
        :param t: должна ли граница соединяться сверху
        :param b: должна ли граница соединяться снизу
        """
        self.left = l
        self.right = r
        self.top = t
        self.bottom = b

    def __int__(self):
        i = 0
        if self.left:
            i += 1
        if self.right:
            i += 2
        if self.top:
            i += 4
        if self.bottom:
            i += 8
        return i

    def __eq__(self, other):
        if not isinstance(other, Border):
            return False
        return int(self) == int(other)

    def __str__(self):
        i = int(self)
        if i == 0:
            ch = ' '
        elif i == 1:
            ch = '╴'
        elif i == 2:
            ch = '╶'
        elif i == 3:
            ch = '─'
        elif i == 4:
            ch = '╵'
        elif i == 5:
            ch = '┘'
        elif i == 6:
            ch = '└'
        elif i == 7:
            ch = '┴'
        elif i == 8:
            ch = '╷'
        elif i == 9:
            ch = '┐'
        elif i == 10:
            ch = '┌'
        elif i == 11:
            ch = '┬'
        elif i == 12:
            ch = '│'
        elif i == 13:
            ch = '┤'
        elif i == 14:
            ch = '├'
        elif i == 15:
            ch = '┼'
        else:
            ch = ''
        return ch

    def __repr__(self):
        return "<Border '{}'>".format(str(self))

    def __add__(self, other):
        if not isinstance(other, Border):
            raise TypeError("unsupported operand type(s) for +: 'Border' and '{}'".format(type(other)))

        l = self.left or other.left
        r = self.right or other.right
        t = self.top or other.top
        b = self.bottom or other.bottom
        return Border(l=l, r=r, t=t, b=b)

    def __sub__(self, other):
        if not isinstance(other, Border):
            raise TypeError("unsupported operand type(s) for -: 'Border' and '{}'".format(type(other)))

        l = (int(self) & 0b0001) > (int(other) & 0b0001)
        r = (int(self) & 0b0010) > (int(other) & 0b0010)
        t = (int(self) & 0b0100) > (int(other) & 0b0100)
        b = (int(self) & 0b1000) > (int(other) & 0b1000)
        return Border(l=l, r=r, t=t, b=b)

    def __copy__(self):
        return Border(l=self.left, r=self.right, t=self.top, b=self.bottom)
