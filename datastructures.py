import random
class Literal:
    def __init__(self, name):
        self.name = str(name)
    def __repr__(self):
        return '<' + self.name + '>'
    def __mod__(self, other):
        return self.name == other
    def __hash__(self):
        return hash(self.name) ^ hash("literal")
    def __eq__(self, other):
        if isinstance(other, Literal):
            return other.name == self.name
        return False


class Queue(list):
    """Self-shuffling list"""
    def __init__(self):
        self.i = 0
        self.c = 0
    def append(self, element):
        # print("Adding", element)
        super().append(element)
        self.i += 1
        self.c += 1
        if self.i > self.c and len(self)>2:
            # print("Shuffled")
            random.shuffle(self)
            self.i = 0
    def pop(self):
        self.c -= 1
        self.i += 1
        if self.i > self.c and len(self)>2:
            # print("Shuffled")
            random.shuffle(self)
            self.i = 0
        return super().pop()
